"""Shipment report generation and export routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.report_forms import ReportFilterForm
from app.models.parcel import Parcel
from app.services.report_service import build_report, export_csv, get_report_rows

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports", methods=["GET", "POST"])
@login_required
def reports():
    """Display and generate shipment reports."""
    form = ReportFilterForm()
    status = request.args.get("status", "all")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    rows = get_report_rows(from_date=from_date, to_date=to_date, status=status)

    if request.method == "POST" and form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        status = form.status.data
        rows = get_report_rows(from_date=from_date, to_date=to_date, status=status)
        build_report(from_date, to_date, status, current_user.id)
        flash("Report generated successfully.", "success")
        return redirect(url_for("reports.reports", from_date=from_date, to_date=to_date, status=status))

    total_shipments = len(rows)
    total_revenue = sum((parcel.parcel_info.price if parcel.parcel_info else 0) for parcel in rows)
    return render_template("reports/index.html", form=form, rows=rows, total_shipments=total_shipments, total_revenue=total_revenue, status=status)


@reports_bp.route("/reports/export")
@login_required
def export_reports():
    """Export filtered shipments as CSV."""
    status = request.args.get("status", "all")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    rows = get_report_rows(from_date=from_date, to_date=to_date, status=status)
    return export_csv(rows)


@reports_bp.route("/reports/clear", methods=["POST"])
@login_required
def clear_shipments():
    """Clear all shipment records after admin confirmation."""
    confirmation = request.form.get("confirmation", "")
    if confirmation != "DELETE":
        flash("Type DELETE to confirm clearing all shipments.", "error")
        return redirect(url_for("reports.reports"))

    parcels = Parcel.query.all()
    for parcel in parcels:
        if parcel.parcel_info:
            db.session.delete(parcel.parcel_info)
        db.session.delete(parcel)
    db.session.commit()
    flash("All shipments cleared.", "success")
    return redirect(url_for("reports.reports"))
