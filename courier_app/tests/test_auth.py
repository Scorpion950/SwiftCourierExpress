"""Authentication route tests."""


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
