"""Business logic for generating and exporting shipment reports."""

import csv
import io
from datetime import date, datetime, time, timedelta

from flask import Response
from sqlalchemy.orm import contains_eager

from app.extensions import db
from app.models.parcel import Parcel
from app.models.parcel_info import ParcelInfo
from app.models.report import Report


def get_report_rows(from_date=None, to_date=None, status="all"):
    """Query parcel rows for report generation."""
    query = (
        db.session.query(Parcel)
        .join(ParcelInfo, Parcel.id == ParcelInfo.parcel_id)
        .options(contains_eager(Parcel.parcel_info))
    )

    if from_date:
        if isinstance(from_date, str):
            from_date = date.fromisoformat(from_date)
        query = query.filter(Parcel.created_at >= datetime.combine(from_date, time.min))
    if to_date:
        if isinstance(to_date, str):
            to_date = date.fromisoformat(to_date)
        day_after_to_date = datetime.combine(to_date + timedelta(days=1), time.min)
        query = query.filter(Parcel.created_at < day_after_to_date)
    if status and status != "all":
        query = query.filter(Parcel.status == status)

    return query.order_by(Parcel.created_at.desc()).all()


def build_report(from_date, to_date, status, admin_id):
    """Generate a summary report and save it in the report table."""
    rows = get_report_rows(from_date=from_date, to_date=to_date, status=status)
    total_shipments = len(rows)
    total_revenue = sum((row.parcel_info.price if row.parcel_info else 0) for row in rows)
    report = Report(
        from_date=from_date or datetime.utcnow().date(),
        to_date=to_date or datetime.utcnow().date(),
        total_shipments=total_shipments,
        total_revenue=total_revenue,
        generated_by=admin_id,
        created_at=datetime.utcnow(),
    )
    db.session.add(report)
    db.session.commit()
    return rows, report


def export_csv(rows):
    """Render the report rows as CSV content."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Tracking", "Date", "Receiver", "Route", "Status", "Charge"])

    for parcel in rows:
        writer.writerow([
            parcel.tracking_number,
            parcel.created_at.strftime("%Y-%m-%d"),
            parcel.receiver_name,
            f"{parcel.origin} -> {parcel.destination}",
            parcel.status,
            parcel.parcel_info.price if parcel.parcel_info else 0,
        ])

    csv_data = output.getvalue()
    response = Response(csv_data, mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=shipments_report.csv"
    return response
