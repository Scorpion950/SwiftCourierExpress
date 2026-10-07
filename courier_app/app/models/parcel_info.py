"""Parcel information model for measurable details and charge."""

from app.extensions import db


class ParcelInfo(db.Model):
    """Stores dimensions and price for a shipment."""

    __tablename__ = "parcel_info"

    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey("parcels.id"), unique=True, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    length_cm = db.Column(db.Float, nullable=False)
    width_cm = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)

    __table_args__ = (
        db.CheckConstraint("weight_kg > 0", name="ck_parcel_info_weight_positive"),
        db.CheckConstraint("price >= 0", name="ck_parcel_info_price_non_negative"),
    )

    parcel = db.relationship("Parcel", back_populates="parcel_info")
