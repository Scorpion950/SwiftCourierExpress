"""Parcel model for shipment booking data."""

from datetime import datetime

from app.extensions import db


class Parcel(db.Model):
    """Represents a shipment as booked by an admin."""

    __tablename__ = "parcels"

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    sender_name = db.Column(db.String(120), nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    receiver_name = db.Column(db.String(120), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    parcel_type = db.Column(db.String(30), nullable=False)
    service_type = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), default="Booked", nullable=False)
    booked_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    sender = db.relationship("Customer", back_populates="parcels", foreign_keys=[sender_id])
    booking_admin = db.relationship("Admin", foreign_keys=[booked_by], backref="booked_parcels")
    parcel_info = db.relationship("ParcelInfo", back_populates="parcel", uselist=False, cascade="all, delete-orphan")
    tracking_history = db.relationship("TrackParcel", back_populates="parcel", cascade="all, delete-orphan")
