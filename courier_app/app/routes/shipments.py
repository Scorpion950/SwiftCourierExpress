"""Shipment booking and tracking routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.shipment_forms import BookShipmentForm, TrackSearchForm, UpdateStatusForm
from app.models.settings import Settings
from app.services.customer_service import search_customers
from app.services.shipment_service import book_shipment, get_by_tracking, update_status

shipments_bp = Blueprint("shipments", __name__)


@shipments_bp.route("/book", methods=["GET", "POST"])
@login_required
def book_shipment_route():
    """Book a new shipment and redirect to its bill page."""
    form = BookShipmentForm()
    if form.validate_on_submit():
        data = {
            "sender_name": form.sender_name.data,
            "sender_phone": form.sender_phone.data,
            "receiver_name": form.receiver_name.data,
            "receiver_phone": form.receiver_phone.data,
            "origin": form.origin.data,
            "destination": form.destination.data,
            "parcel_type": form.parcel_type.data,
            "service_type": form.service_type.data,
            "weight_kg": form.weight_kg.data,
            "length_cm": form.length_cm.data,
            "width_cm": form.width_cm.data,
            "height_cm": form.height_cm.data,
            "charge": form.charge.data,
        }
        parcel = book_shipment(data, current_user.id)
        flash("Shipment booked successfully.", "success")
        return redirect(url_for("shipments.bill", tracking=parcel.tracking_number))
    settings = Settings.query.first()
    customers = search_customers("")
    return render_template("shipments/book.html", form=form, settings=settings, customers=customers)


@shipments_bp.route("/bill/<tracking>")
@login_required
def bill(tracking):
    """Display a printable shipment bill."""
    parcel = get_by_tracking(tracking)
    if parcel is None:
        flash("Shipment not found.", "error")
        return redirect(url_for("dashboard.index"))
    settings = Settings.query.first()
    history = sorted(parcel.tracking_history, key=lambda h: h.timestamp, reverse=True)
    return render_template("shipments/bill.html", parcel=parcel, settings=settings, history=history)


@shipments_bp.route("/bill/<tracking>/download")
@login_required
def bill_download(tracking):
    """Download the shipment bill as HTML."""
    parcel = get_by_tracking(tracking)
    if parcel is None:
        flash("Shipment not found.", "error")
        return redirect(url_for("dashboard.index"))
    settings = Settings.query.first()
    history = sorted(parcel.tracking_history, key=lambda h: h.timestamp, reverse=True)
    html = render_template("shipments/bill.html", parcel=parcel, settings=settings, history=history)
    return html


@shipments_bp.route("/track", methods=["GET", "POST"])
@login_required
def track():
    """Search for a parcel and update its current status."""
    track_form = TrackSearchForm()
    update_form = UpdateStatusForm()
    parcel = None
    status_message = None

    if request.method == "POST":
        if "new_status" in request.form and update_form.validate_on_submit():
            parcel = get_by_tracking(request.form.get("tracking_number"))
            if parcel is None:
                flash("Tracking number not found.", "error")
            else:
                updated = update_status(parcel.tracking_number, update_form.new_status.data, update_form.remark.data, current_user.id)
                if updated:
                    status_message = "Status updated successfully."
                    flash(status_message, "success")
                    parcel = get_by_tracking(parcel.tracking_number)
        elif track_form.validate_on_submit():
            parcel = get_by_tracking(track_form.tracking_number.data.strip())
            if parcel is None:
                flash("Tracking number not found.", "error")
            else:
                update_form.new_status.data = parcel.status

    history = sorted(parcel.tracking_history, key=lambda h: h.timestamp, reverse=True) if parcel else []
    return render_template("shipments/track.html", track_form=track_form, update_form=update_form, parcel=parcel, history=history)
