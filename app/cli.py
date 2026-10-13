"""Custom Flask CLI commands for database initialization and seeding."""

import os

import click

from app.extensions import db
from app.models.admin import Admin
from app.models.settings import Settings


def register_commands(app):
    """Register project-specific Flask CLI commands."""

    @app.cli.command("init-db")
    def init_db_command():
        """Create all database tables."""
        with app.app_context():
            db.create_all()
            click.echo("Database tables created successfully.")

    @app.cli.command("seed")
    def seed_command():
        """Create the default admin and settings row."""
        with app.app_context():
            email = os.getenv("ADMIN_EMAIL", "admin@swiftcourier.com").lower().strip()
            password = os.getenv("ADMIN_PASSWORD", "Admin@123")
            name = "Administrator"

            admin = db.session.query(Admin).filter_by(email=email).first()
            if admin is None:
                admin = Admin(name=name, email=email)
                admin.set_password(password)
                db.session.add(admin)

            settings = db.session.query(Settings).first()
            if settings is None:
                settings = Settings(
                    company_name="SwiftCourier Express",
                    tagline="Fast. Safe. Reliable.",
                    address="123 Cargo Street, Colombo 03",
                    phone="9876543210",
                    email="contact@swiftcourier.com",
                )
                db.session.add(settings)

            db.session.commit()
            click.echo(f"Seeded admin user: {email}")
