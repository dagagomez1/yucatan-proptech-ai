"""
Fideicomiso (Bank Trust) Guidance Engine

Provides structured knowledge about the Mexican fideicomiso process
for foreign property buyers in the Yucatan Peninsula restricted zone.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PropertyZone(Enum):
    RESTRICTED = "restricted"
    UNRESTRICTED = "unrestricted"


class BuyerType(Enum):
    MEXICAN_NATIONAL = "mexican_national"
    FOREIGN_INDIVIDUAL = "foreign_individual"
    FOREIGN_CORPORATION = "foreign_corporation"


@dataclass
class FideicomisoRequirement:
    required: bool
    reason: str
    alternative: Optional[str] = None
    estimated_setup_cost_usd: float = 0
    annual_fee_usd: float = 0
    setup_time_weeks: int = 0


@dataclass
class FideicomisoStep:
    order: int
    title: str
    description: str
    estimated_days: int
    required_documents: list = field(default_factory=list)
    tips: list = field(default_factory=list)


YUCATAN_ZONES = {
    "progreso": PropertyZone.RESTRICTED,
    "celestun": PropertyZone.RESTRICTED,
    "sisal": PropertyZone.RESTRICTED,
    "telchac": PropertyZone.RESTRICTED,
    "dzilam": PropertyZone.RESTRICTED,
    "rio_lagartos": PropertyZone.RESTRICTED,
    "san_felipe": PropertyZone.RESTRICTED,
    "tulum": PropertyZone.RESTRICTED,
    "playa_del_carmen": PropertyZone.RESTRICTED,
    "cancun": PropertyZone.RESTRICTED,
    "puerto_morelos": PropertyZone.RESTRICTED,
    "isla_mujeres": PropertyZone.RESTRICTED,
    "merida": PropertyZone.UNRESTRICTED,
    "valladolid": PropertyZone.UNRESTRICTED,
    "izamal": PropertyZone.UNRESTRICTED,
    "ticul": PropertyZone.UNRESTRICTED,
    "motul": PropertyZone.UNRESTRICTED,
    "oxkutzcab": PropertyZone.UNRESTRICTED,
}

FIDEICOMISO_BANKS = [
    {
        "name": "Scotiabank Mexico",
        "setup_fee_usd": 1500,
        "annual_fee_usd": 500,
        "offices_yucatan": ["Merida", "Cancun", "Playa del Carmen"],
        "notes": "One of the most popular choices for foreign buyers"
    },
    {
        "name": "BBVA Mexico (Bancomer)",
        "setup_fee_usd": 1800,
        "annual_fee_usd": 600,
        "offices_yucatan": ["Merida", "Cancun", "Valladolid"],
        "notes": "Large network, reliable service"
    },
    {
        "name": "Banorte",
        "setup_fee_usd": 1400,
        "annual_fee_usd": 450,
        "offices_yucatan": ["Merida", "Cancun"],
        "notes": "Mexican-owned bank, competitive rates"
    },
    {
        "name": "HSBC Mexico",
        "setup_fee_usd": 2000,
        "annual_fee_usd": 700,
        "offices_yucatan": ["Merida", "Cancun", "Playa del Carmen"],
        "notes": "International bank, good for expats"
    },
]


def check_fideicomiso_requirement(location: str, buyer_type: BuyerType) -> FideicomisoRequirement:
    location_key = location.lower().replace(" ", "_")
    zone = YUCATAN_ZONES.get(location_key)

    if buyer_type == BuyerType.MEXICAN_NATIONAL:
        return FideicomisoRequirement(
            required=False,
            reason="Mexican nationals can purchase property directly in any zone.",
        )

    if zone == PropertyZone.RESTRICTED:
        return FideicomisoRequirement(
            required=True,
            reason=(
                f"{location.title()} is in Mexico's restricted zone (within 50km of "
                "the coast). Foreign nationals must use a fideicomiso (bank trust) "
                "to hold property title."
            ),
            estimated_setup_cost_usd=1500,
            annual_fee_usd=500,
            setup_time_weeks=6,
        )

    if zone == PropertyZone.UNRESTRICTED:
        return FideicomisoRequirement(
            required=False,
            reason=(
                f"{location.title()} is in Mexico's unrestricted zone. Foreign nationals "
                "can purchase property directly through a Mexican corporation (SA de CV) "
                "or may still opt for a fideicomiso for additional legal protection."
            ),
            alternative=(
                "Form a Mexican corporation (SA de CV) to hold the property. "
                "This is often simpler and cheaper than a fideicomiso for "
                "unrestricted zone properties."
            ),
            estimated_setup_cost_usd=1000,
            annual_fee_usd=300,
            setup_time_weeks=4,
        )

    return FideicomisoRequirement(
        required=True,
        reason=(
            f"Location '{location}' not found in database. As a precaution, "
            "a fideicomiso is recommended. Consult a notario publico to confirm "
            "the zone classification."
        ),
        estimated_setup_cost_usd=1500,
        annual_fee_usd=500,
        setup_time_weeks=6,
    )


def get_fideicomiso_steps() -> list:
    return [
        FideicomisoStep(
            order=1,
            title="Obtain Mexican RFC (Tax ID)",
            description="Apply for a Registro Federal de Contribuyentes at SAT.",
            estimated_days=5,
            required_documents=["Valid passport", "Proof of address", "Immigration document"],
            tips=["Schedule appointment online at sat.gob.mx"],
        ),
        FideicomisoStep(
            order=2,
            title="Obtain SRE Permit",
            description="Apply for permit from Secretaria de Relaciones Exteriores.",
            estimated_days=15,
            required_documents=["Application form", "Passport copy", "Property details", "Fee payment"],
            tips=["Your notario publico can handle this application"],
        ),
        FideicomisoStep(
            order=3,
            title="Select Trustee Bank",
            description="Choose an authorized Mexican bank to serve as trustee.",
            estimated_days=7,
            required_documents=["Bank application", "Passport", "RFC", "SRE permit", "Proof of funds"],
            tips=["Scotiabank and BBVA are popular in Yucatan", "Negotiate fees"],
        ),
        FideicomisoStep(
            order=4,
            title="Property Due Diligence",
            description="Conduct thorough due diligence including title search and lien check.",
            estimated_days=14,
            required_documents=["Property title", "Certificate of no liens", "Tax receipts", "Survey"],
            tips=["ALWAYS verify the seller is the legal owner", "Check for ejido land status"],
        ),
        FideicomisoStep(
            order=5,
            title="Sign Fideicomiso Agreement",
            description="Sign the trust agreement before a notario publico.",
            estimated_days=3,
            required_documents=["All previous documents", "Purchase agreement", "Bank trust agreement"],
            tips=["Have an independent translator if needed", "Initial term is 50 years, renewable"],
        ),
        FideicomisoStep(
            order=6,
            title="Registration and Title Transfer",
            description="Register the fideicomiso with the Public Registry of Property.",
            estimated_days=30,
            required_documents=["Signed fideicomiso agreement", "All supporting documents", "Fee payments"],
            tips=["Budget for closing costs: 5-8% of property value"],
        ),
    ]
