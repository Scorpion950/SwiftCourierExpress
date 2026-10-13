"""Settings model for company profile records."""

from app.extensions import db


class Settings(db.Model):
    """Stores the single company settings row."""

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(180), nullable=True)
    tagline = db.Column(db.String(180), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(255), nullable=True)
