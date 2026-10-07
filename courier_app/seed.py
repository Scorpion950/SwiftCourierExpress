"""Seed the database with a default admin and settings row."""

import os

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models.admin import Admin
from app.models.settings import Settings

load_dotenv()


def seed_database():
    """Initialize the database and add the default admin and settings."""
    app = create_app()
    with app.app_context():
        db.create_all()
        email = os.getenv("ADMIN_EMAIL", "admin@swiftcourier.com").lower().strip()
        password = os.getenv("ADMIN_PASSWORD", "Admin@123")

        admin = db.session.query(Admin).filter_by(email=email).first()
        if admin is None:
            admin = Admin(name="Administrator", email=email)
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
        print(f"Seeded admin: {email}")
        print(f"Default settings created for {settings.company_name}")


if __name__ == "__main__":
    seed_database()
