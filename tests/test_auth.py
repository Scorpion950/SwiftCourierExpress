"""Authentication route tests."""

from app.extensions import db
from app.models.admin import Admin


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"SwiftCourier Express" in response.data


def test_login_success(client):
    response = client.post(
        "/login",
        data={"email": "admin@example.com", "password": "adminpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Login successful" in response.data


def test_login_accepts_username_identifier(client, app):
    with app.app_context():
        admin = db.session.query(Admin).filter_by(email="admin@example.com").first()
        admin.email = "prajwal@123"
        db.session.commit()

    response = client.post(
        "/login",
        data={"email": "prajwal@123", "password": "adminpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Login successful" in response.data


def test_about_page_uses_dashboard_sidebar(client):
    client.post(
        "/login",
        data={"email": "admin@example.com", "password": "adminpass"},
        follow_redirects=True,
    )
    response = client.get("/about")

    assert response.status_code == 200
    assert b'id="sidebar"' in response.data
    assert b"About SwiftCourier Express" in response.data
    assert b"Generate shipment reports by date and status" in response.data
    assert b"timestamped history of shipment status changes" in response.data
