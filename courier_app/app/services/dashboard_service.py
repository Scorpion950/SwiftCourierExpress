"""Dashboard statistics and recent shipment queries."""

from datetime import datetime

from sqlalchemy import func

from app.extensions import db
from app.models.customer import Customer
from app.models.parcel import Parcel
from app.models.parcel_info import ParcelInfo


def get_dashboard_data():
    """Return summary metrics for the operations overview."""
    today = datetime.utcnow().date()
    total_shipments = db.session.query(Parcel).count()
    booked_today = db.session.query(Parcel).filter(func.date(Parcel.created_at) == today).count()
    in_progress = db.session.query(Parcel).filter(Parcel.status.in_(["Picked Up", "In Transit", "Out for Delivery"])).count()
    delivered = db.session.query(Parcel).filter(Parcel.status == "Delivered").count()
    customers = db.session.query(Customer).count()
    revenue_sum = db.session.query(func.coalesce(func.sum(ParcelInfo.price), 0)).join(Parcel, Parcel.id == ParcelInfo.parcel_id).scalar() or 0
    recent_shipments = db.session.query(Parcel).order_by(Parcel.created_at.desc()).limit(5).all()

    return {
        "total_shipments": total_shipments,
        "booked_today": booked_today,
        "in_progress": in_progress,
        "delivered": delivered,
        "customers": customers,
        "total_revenue": float(revenue_sum),
        "recent_shipments": recent_shipments,
    }
