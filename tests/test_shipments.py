"""Shipment booking and tracking tests."""

import re

from app.extensions import db
from app.models.parcel import Parcel
from app.models.track_parcel import TrackParcel


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_book_shipment_displays_and_persists_tracking_number(client, app):
    login_admin(client)
    response = client.post(
        "/book",
        data={
            "sender_name": "Alice Test",
            "sender_phone": "1234567890",
            "receiver_name": "Bob Test",
            "receiver_phone": "0987654321",
            "origin": "Colombo",
            "destination": "Kandy",
            "parcel_type": "Documents",
            "service_type": "Express",
            "weight_kg": 2.5,
            "length_cm": 20,
            "width_cm": 15,
            "height_cm": 10,
            "charge": 225,
            "csrf_token": "test" if False else "",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Shipment booked successfully" in response.data
    tracking_match = re.search(
        r"Tracking:</strong>\s*(TRK\d+)", response.get_data(as_text=True)
    )
    assert tracking_match is not None
    tracking_number = tracking_match.group(1)

    with app.app_context():
        parcel = db.session.query(Parcel).filter_by(tracking_number=tracking_number).one()
        history = db.session.query(TrackParcel).filter_by(parcel_id=parcel.id).one()
        assert history.tracking_number == tracking_number
        assert history.status == "Booked"

    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
    assert tracking_number.encode() in dashboard.data


def test_invalid_booking_displays_field_errors(client):
    login_admin(client)
    response = client.post(
        "/book",
        data={
            "sender_name": "Alice Test",
            "sender_phone": "1234567890",
            "receiver_name": "Bob Test",
            "receiver_phone": "0987654321",
            "origin": "Colombo",
            "destination": "Kandy",
            "parcel_type": "Documents",
            "service_type": "Express",
            "weight_kg": 2.5,
            "length_cm": 20,
            "width_cm": 15,
            "height_cm": 10,
        },
    )

    assert response.status_code == 200
    assert b"Shipment was not booked" in response.data
    assert b"Charge (Rs): This field is required" in response.data


def test_track_page(client):
    login_admin(client)
    response = client.get("/track")
    assert response.status_code == 200
    assert b"Track and Update Shipment" in response.data
