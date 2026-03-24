"""
Property Analysis Module

Provides data models and analysis tools for Yucatan real estate properties.
Uses Claude AI for intelligent valuation and investment scoring.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class PropertyType(Enum):
    COLONIAL_HOME = "colonial_home"
    MODERN_HOUSE = "modern_house"
    CONDO = "condo"
    LAND = "land"
    COMMERCIAL = "commercial"
    HACIENDA = "hacienda"
    BEACH_PROPERTY = "beach_property"


class InvestmentStrategy(Enum):
    LONG_TERM_RENTAL = "long_term_rental"
    SHORT_TERM_VACATION = "short_term_vacation"
    FIX_AND_FLIP = "fix_and_flip"
    BUY_AND_HOLD = "buy_and_hold"
    DEVELOPMENT = "development"


@dataclass
class PropertyListing:
    address: str
    city: str
    price_mxn: float
    property_type: PropertyType
    size_m2: float
    bedrooms: int = 0
    bathrooms: int = 0
    year_built: Optional[int] = None
    description: str = ""
    features: list = field(default_factory=list)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    listed_date: datetime = field(default_factory=datetime.now)

    @property
    def price_usd(self) -> float:
        MXN_TO_USD = 0.058
        return self.price_mxn * MXN_TO_USD

    @property
    def price_per_m2_mxn(self) -> float:
        if self.size_m2 > 0:
            return self.price_mxn / self.size_m2
        return 0


@dataclass
class InvestmentAnalysis:
    property_listing: PropertyListing
    investment_score: float
    estimated_value_mxn: float
    value_assessment: str
    monthly_rental_estimate_mxn: float
    annual_roi_percent: float
    risk_factors: list = field(default_factory=list)
    growth_forecast: str = ""
    recommendation: str = ""
    ai_analysis: str = ""


MARKET_AVERAGES = {
    "merida": {
        "centro": {"avg_price_m2": 25000, "rental_yield": 0.06},
        "norte": {"avg_price_m2": 22000, "rental_yield": 0.055},
        "altabrisa": {"avg_price_m2": 28000, "rental_yield": 0.05},
        "general": {"avg_price_m2": 18000, "rental_yield": 0.055},
    },
    "valladolid": {
        "centro": {"avg_price_m2": 15000, "rental_yield": 0.07},
        "general": {"avg_price_m2": 10000, "rental_yield": 0.065},
    },
    "tulum": {
        "centro": {"avg_price_m2": 45000, "rental_yield": 0.08},
        "beach": {"avg_price_m2": 65000, "rental_yield": 0.09},
        "general": {"avg_price_m2": 35000, "rental_yield": 0.075},
    },
    "playa_del_carmen": {
        "centro": {"avg_price_m2": 35000, "rental_yield": 0.07},
        "playacar": {"avg_price_m2": 40000, "rental_yield": 0.065},
        "general": {"avg_price_m2": 30000, "rental_yield": 0.07},
    },
    "progreso": {
        "beach": {"avg_price_m2": 20000, "rental_yield": 0.06},
        "general": {"avg_price_m2": 12000, "rental_yield": 0.055},
    },
    "izamal": {
        "centro": {"avg_price_m2": 8000, "rental_yield": 0.065},
        "general": {"avg_price_m2": 5000, "rental_yield": 0.06},
    },
}


def estimate_property_value(listing, zone="general"):
    city_key = listing.city.lower().replace(" ", "_")
    city_data = MARKET_AVERAGES.get(city_key, {})
    zone_data = city_data.get(zone, city_data.get("general", {}))
    avg_price_m2 = zone_data.get("avg_price_m2", 15000)
    estimated_value = listing.size_m2 * avg_price_m2

    if listing.property_type == PropertyType.COLONIAL_HOME:
        estimated_value *= 1.15
    elif listing.property_type == PropertyType.HACIENDA:
        estimated_value *= 1.30
    elif listing.property_type == PropertyType.BEACH_PROPERTY:
        estimated_value *= 1.25

    return estimated_value


def calculate_rental_roi(listing, zone="general", occupancy_rate=0.70):
    city_key = listing.city.lower().replace(" ", "_")
    city_data = MARKET_AVERAGES.get(city_key, {})
    zone_data = city_data.get(zone, city_data.get("general", {}))
    rental_yield = zone_data.get("rental_yield", 0.06)

    annual_rental = listing.price_mxn * rental_yield
    monthly_rental = annual_rental / 12
    effective_annual = annual_rental * occupancy_rate
    effective_monthly = monthly_rental * occupancy_rate
    annual_expenses = listing.price_mxn * 0.02
    net_annual = effective_annual - annual_expenses
    net_roi = (net_annual / listing.price_mxn) * 100

    return {
        "gross_monthly_rental_mxn": monthly_rental,
        "effective_monthly_rental_mxn": effective_monthly,
        "gross_annual_rental_mxn": annual_rental,
        "effective_annual_rental_mxn": effective_annual,
        "estimated_annual_expenses_mxn": annual_expenses,
        "net_annual_income_mxn": net_annual,
        "net_roi_percent": net_roi,
        "occupancy_rate": occupancy_rate,
    }
