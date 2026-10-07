"""Report model for saved shipment reports."""

from datetime import datetime

from app.extensions import db


class Report(db.Model):
    """Stores generated shipment reports and summary totals."""

    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    total_shipments = db.Column(db.Integer, default=0, nullable=False)
    total_revenue = db.Column(db.Float, default=0.0, nullable=False)
    generated_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    admin = db.relationship("Admin", foreign_keys=[generated_by], backref="generated_reports")
