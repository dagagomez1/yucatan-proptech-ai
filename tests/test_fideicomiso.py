"""Tests for the fideicomiso guidance engine."""

import pytest
from src.fideicomiso import (
    check_fideicomiso_requirement,
    get_fideicomiso_steps,
    BuyerType,
    PropertyZone,
    YUCATAN_ZONES,
)


def test_restricted_zone_requires_fideicomiso():
    result = check_fideicomiso_requirement("Progreso", BuyerType.FOREIGN_INDIVIDUAL)
    assert result.required is True
    assert "restricted zone" in result.reason.lower()


def test_unrestricted_zone_no_fideicomiso():
    result = check_fideicomiso_requirement("Merida", BuyerType.FOREIGN_INDIVIDUAL)
    assert result.required is False
    assert result.alternative is not None


def test_mexican_national_no_fideicomiso():
    result = check_fideicomiso_requirement("Tulum", BuyerType.MEXICAN_NATIONAL)
    assert result.required is False


def test_unknown_location_defaults_to_required():
    result = check_fideicomiso_requirement("Unknown City", BuyerType.FOREIGN_INDIVIDUAL)
    assert result.required is True
    assert "not found" in result.reason.lower()


def test_fideicomiso_steps_complete():
    steps = get_fideicomiso_steps()
    assert len(steps) == 6
    assert steps[0].order == 1
    assert steps[-1].order == 6


def test_fideicomiso_steps_have_documents():
    steps = get_fideicomiso_steps()
    for step in steps:
        assert len(step.required_documents) > 0


def test_coastal_cities_are_restricted():
    coastal = ["progreso", "tulum", "cancun", "playa_del_carmen"]
    for city in coastal:
        assert YUCATAN_ZONES[city] == PropertyZone.RESTRICTED


def test_interior_cities_are_unrestricted():
    interior = ["merida", "valladolid", "izamal"]
    for city in interior:
        assert YUCATAN_ZONES[city] == PropertyZone.UNRESTRICTED
