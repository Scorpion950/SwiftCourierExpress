"""Pytest fixtures for the SwiftCourier Express app."""

import pytest

from app import create_app
from app.extensions import db
from app.models.admin import Admin
from app.models.settings import Settings


@pytest.fixture()
def app():
    """Create and configure the Flask test app."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        admin = Admin(name="Administrator", email="admin@example.com")
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.add(
            Settings(
                company_name="SwiftCourier Express",
                tagline="Fast. Safe. Reliable.",
                address="123 Cargo Street, Colombo 03",
                phone="9876543210",
                email="contact@swiftcourier.com",
            )
        )
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Return a test client for hitting the Flask app."""
    return app.test_client()
