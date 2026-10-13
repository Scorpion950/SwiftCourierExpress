"""Pricing helpers for shipment charge suggestions."""


def suggest_charge(weight_kg, service_type):
    """Return the suggested charge based on weight and service type."""
    base = 100 + float(weight_kg) * 50
    if service_type == "Express":
        base *= 1.5
    elif service_type == "International":
        base *= 3
    return round(float(base), 2)
