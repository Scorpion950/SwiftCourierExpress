"""Blueprint registration for all application modules."""

from app.routes.auth import auth_bp
from app.routes.customers import customers_bp
from app.routes.dashboard import dashboard_bp
from app.routes.public import public_bp
from app.routes.reports import reports_bp
from app.routes.shipments import shipments_bp
from app.routes.settings import settings_bp


def register_blueprints(app):
    """Register each module blueprint with the Flask app."""
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(shipments_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
