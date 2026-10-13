"""Shared validation helpers for user input."""

from wtforms import ValidationError


def validate_phone(form, field):
    """Ensure the value contains exactly ten digits."""
    value = field.data.strip() if field.data else ""
    if len(value) != 10 or not value.isdigit():
        raise ValidationError("Phone number must contain exactly 10 digits.")


def validate_positive_weight(form, field):
    """Ensure weight is positive."""
    if field.data is None or field.data <= 0:
        raise ValidationError("Weight must be greater than 0.")


def validate_non_negative_price(form, field):
    """Ensure price is zero or above."""
    if field.data is None or field.data < 0:
        raise ValidationError("Price cannot be negative.")
