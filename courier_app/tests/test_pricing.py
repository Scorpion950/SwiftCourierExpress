"""Pricing utility tests."""

from app.utils.pricing import suggest_charge


def test_suggest_charge_standard():
    assert suggest_charge(2, "Standard") == 200.0


def test_suggest_charge_express():
    assert suggest_charge(2, "Express") == 300.0


def test_suggest_charge_international():
    assert suggest_charge(2, "International") == 600.0
