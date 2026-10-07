"""Customer management tests."""


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_customers_page_loads(client):
    login_admin(client)
    response = client.get("/customers")
    assert response.status_code == 200
    assert b"Customers" in response.data


def test_add_customer(client):
    login_admin(client)
    response = client.post(
        "/customers",
        data={"name": "Jane Customer", "phone": "9876543210", "csrf_token": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Customer added successfully" in response.data
