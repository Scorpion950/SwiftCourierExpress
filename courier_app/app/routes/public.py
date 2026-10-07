"""Public routes for landing, about, and public parcel tracking."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app.models.settings import Settings
from app.services.shipment_service import get_by_tracking

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def welcome():
    """Render the welcome page."""
    return render_template("public/welcome.html")


@public_bp.route("/about")
@login_required
def about():
    """Render the about page."""
    settings = Settings.query.first()
    return render_template("public/about.html", settings=settings)


@public_bp.route("/t/<tracking>")
def public_tracking(tracking):
    """Render a public tracking timeline for a parcel."""
    parcel = get_by_tracking(tracking)
    if parcel is None:
        flash("Tracking number not found.", "error")
        return redirect(url_for("public.welcome"))
    history = sorted(parcel.tracking_history, key=lambda h: h.timestamp, reverse=True)
    return render_template("public/track_public.html", parcel=parcel, history=history)
