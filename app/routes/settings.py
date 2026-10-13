"""Company settings management route."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app.forms.settings_forms import SettingsForm
from app.services.settings_service import get_settings, reset_defaults, save_settings

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def company_settings():
    """Allow admins to update the company profile settings."""
    form = SettingsForm()
    settings = get_settings()
    if form.validate_on_submit():
        save_settings({
            "company_name": form.company_name.data,
            "tagline": form.tagline.data,
            "address": form.address.data,
            "phone": form.phone.data,
            "email": form.email.data,
        })
        flash("Settings saved successfully.", "success")
        return redirect(url_for("settings.company_settings"))
    form.company_name.data = settings.company_name
    form.tagline.data = settings.tagline
    form.address.data = settings.address
    form.phone.data = settings.phone
    form.email.data = settings.email
    return render_template("settings/index.html", form=form, settings=settings)


@settings_bp.route("/settings/reset", methods=["POST"])
@login_required
def reset_settings():
    """Reset company settings back to their default values."""
    reset_defaults()
    flash("Default settings restored.", "success")
    return redirect(url_for("settings.company_settings"))
