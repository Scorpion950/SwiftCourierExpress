"""Shipment tracking history model."""

from datetime import datetime

from app.extensions import db


class TrackParcel(db.Model):
    """Stores every status change for a parcel."""

    __tablename__ = "track_parcel"

    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey("parcels.id"), nullable=False)
    tracking_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    remark = db.Column(db.Text, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    parcel = db.relationship("Parcel", back_populates="tracking_history")
    admin = db.relationship("Admin", foreign_keys=[updated_by], backref="tracking_updates")
