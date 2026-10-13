"""Application-wide error handlers for user-friendly pages."""

from flask import render_template
from sqlalchemy.exc import OperationalError


def register_error_handlers(app):
    """Register custom 404, 500 and database error handlers."""

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return render_template("errors/500.html"), 500

    @app.errorhandler(OperationalError)
    def database_unavailable(_error):
        return render_template("errors/db_down.html"), 503
