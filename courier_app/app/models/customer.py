"""Customer model for sender and receiver records."""

from datetime import datetime

from app.extensions import db


class Customer(db.Model):
    """Stores customer name and phone number."""

    __tablename__ = "customers"
    __table_args__ = (
        db.UniqueConstraint("name", "phone", name="uq_customer_name_phone"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    parcels = db.relationship("Parcel", back_populates="sender", foreign_keys="Parcel.sender_id")
