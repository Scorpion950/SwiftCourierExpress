"""Business logic for company settings management."""

from app.extensions import db
from app.models.settings import Settings

DEFAULT_SETTINGS = {
    "company_name": "SwiftCourier Express",
    "tagline": "Fast. Safe. Reliable.",
    "address": "123 Cargo Street, Colombo 03",
    "phone": "9876543210",
    "email": "contact@swiftcourier.com",
}


def get_settings():
    """Return the active company settings row or a default row."""
    settings = db.session.query(Settings).first()
    if settings is None:
        settings = Settings(**DEFAULT_SETTINGS)
        db.session.add(settings)
        db.session.commit()
    return settings


def save_settings(data):
    """Update or create the one settings row."""
    settings = db.session.query(Settings).first()
    if settings is None:
        settings = Settings()
        db.session.add(settings)

    settings.company_name = data.get("company_name") or DEFAULT_SETTINGS["company_name"]
    settings.tagline = data.get("tagline") or DEFAULT_SETTINGS["tagline"]
    settings.address = data.get("address") or DEFAULT_SETTINGS["address"]
    settings.phone = data.get("phone") or DEFAULT_SETTINGS["phone"]
    settings.email = data.get("email") or DEFAULT_SETTINGS["email"]
    db.session.commit()
    return settings


def reset_defaults():
    """Restore the default company profile values."""
    settings = db.session.query(Settings).first()
    if settings is None:
        settings = Settings()
        db.session.add(settings)

    for key, value in DEFAULT_SETTINGS.items():
        setattr(settings, key, value)
    db.session.commit()
    return settings
