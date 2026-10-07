"""Report generation tests."""


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_reports_page_loads(client):
    login_admin(client)
    response = client.get("/reports")
    assert response.status_code == 200
    assert b"Shipment Reports" in response.data
