"""Shipment booking and tracking tests."""


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_book_shipment(client):
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


def test_track_page(client):
    login_admin(client)
    response = client.get("/track")
    assert response.status_code == 200
    assert b"Track and Update Shipment" in response.data
