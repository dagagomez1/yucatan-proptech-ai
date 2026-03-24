"""
Yucatan PropTech AI - FastAPI Backend

REST API for the Yucatan real estate investment platform.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.ai_agent import YucatanPropertyAgent
from src.fideicomiso import (
    check_fideicomiso_requirement,
    get_fideicomiso_steps,
    BuyerType,
    FIDEICOMISO_BANKS,
)
from src.property_analyzer import (
    PropertyListing,
    PropertyType,
    estimate_property_value,
    calculate_rental_roi,
)

app = FastAPI(
    title="Yucatan PropTech AI",
    description="AI-powered real estate investment platform for Yucatan Peninsula",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        try:
            _agent = YucatanPropertyAgent()
        except ValueError:
            raise HTTPException(status_code=500, detail="API key not configured")
    return _agent


class FideicomisoCheckRequest(BaseModel):
    location: str
    buyer_type: str = "foreign_individual"


class PropertyAnalysisRequest(BaseModel):
    address: str
    city: str
    price_mxn: float = Field(..., gt=0)
    property_type: str = "modern_house"
    size_m2: float = Field(default=0, ge=0)
    zone: str = "general"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


@app.get("/")
async def root():
    return {"name": "Yucatan PropTech AI", "version": "0.1.0", "status": "running"}


@app.post("/api/fideicomiso/check")
async def check_fideicomiso(request: FideicomisoCheckRequest):
    try:
        buyer_type = BuyerType(request.buyer_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer_type")
    result = check_fideicomiso_requirement(request.location, buyer_type)
    return {
        "required": result.required,
        "reason": result.reason,
        "alternative": result.alternative,
        "estimated_setup_cost_usd": result.estimated_setup_cost_usd,
        "annual_fee_usd": result.annual_fee_usd,
        "setup_time_weeks": result.setup_time_weeks,
    }


@app.get("/api/fideicomiso/steps")
async def get_steps():
    steps = get_fideicomiso_steps()
    return [{"order": s.order, "title": s.title, "description": s.description,
             "estimated_days": s.estimated_days, "required_documents": s.required_documents,
             "tips": s.tips} for s in steps]


@app.get("/api/fideicomiso/banks")
async def get_banks():
    return FIDEICOMISO_BANKS


@app.post("/api/property/analyze")
async def analyze_property(request: PropertyAnalysisRequest):
    try:
        prop_type = PropertyType(request.property_type)
    except ValueError:
        prop_type = PropertyType.MODERN_HOUSE
    listing = PropertyListing(
        address=request.address, city=request.city,
        price_mxn=request.price_mxn, property_type=prop_type,
        size_m2=request.size_m2,
    )
    estimated_value = estimate_property_value(listing, request.zone)
    rental_roi = calculate_rental_roi(listing, request.zone)
    value_diff = ((listing.price_mxn - estimated_value) / estimated_value) * 100
    assessment = "undervalued" if value_diff < -10 else "overvalued" if value_diff > 10 else "fair"
    return {
        "listing": {"address": listing.address, "city": listing.city,
                     "price_mxn": listing.price_mxn, "price_usd": listing.price_usd},
        "analysis": {"estimated_value_mxn": estimated_value,
                      "value_assessment": assessment,
                      "value_difference_percent": round(value_diff, 1)},
        "rental_projections": rental_roi,
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    agent = get_agent()
    response = agent.market_query(request.message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
