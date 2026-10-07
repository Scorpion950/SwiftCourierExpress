"""Create the Flask application with the application factory pattern."""

import os

from flask import Flask

from app.cli import register_commands
from app.errors import register_error_handlers
from app.extensions import csrf, db, login_manager, migrate
from app.routes import register_blueprints
from config import CONFIG


def create_app(config_name=None):
    """Create and configure the Flask application."""
    config_name = config_name or os.getenv("FLASK_CONFIG", "development")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(CONFIG[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.admin import Admin

        return db.session.get(Admin, int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "error"

    register_blueprints(app)
    register_commands(app)
    register_error_handlers(app)

    return app
 