"""Operations dashboard route."""

from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required

from app.services.dashboard_service import get_dashboard_data
from app.services.settings_service import get_settings


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    """Render the main operations overview page."""
    data = get_dashboard_data()
    settings = get_settings()
    return render_template(
        "dashboard/index.html",
        data=data,
        settings=settings,
        current_date=datetime.utcnow().strftime("%b %d, %Y"),
    )
