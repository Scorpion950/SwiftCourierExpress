"""Customer management tests."""

import re

from app.extensions import db
from app.models.customer import Customer


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_customers_page_loads(client):
    login_admin(client)
    client.post(
        "/customers",
        data={"name": "Jane Customer", "phone": "9876543210", "csrf_token": ""},
    )
    response = client.get("/customers")
    assert response.status_code == 200
    assert b"Customers" in response.data


def test_customer_delete_csrf_token_is_hidden(client):
    login_admin(client)
    client.post(
        "/customers",
        data={"name": "Jane Customer", "phone": "9876543210", "csrf_token": ""},
    )
    response = client.get("/customers")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    delete_form = re.search(
        r'<form method="post" action="/customers/delete/\d+"[^>]*>(.*?)</form>',
        html,
        re.DOTALL,
    )
    assert delete_form is not None
    hidden_token = re.search(
        r'<input id="csrf_token" name="csrf_token" type="hidden" value="([^"]+)">',
        delete_form.group(1),
    )
    assert hidden_token is not None
    assert hidden_token.group(1) not in delete_form.group(1).replace(hidden_token.group(0), "")


def test_add_customer(client):
    login_admin(client)
    response = client.post(
        "/customers",
        data={"name": "Jane Customer", "phone": "9876543210", "csrf_token": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Customer added successfully" in response.data


def test_customer_add_search_and_delete(client, app):
    login_admin(client)
    client.post(
        "/customers",
        data={"name": "Morgan Customer", "phone": "9876543211", "csrf_token": ""},
    )

    with app.app_context():
        customer = db.session.query(Customer).filter_by(name="Morgan Customer").one()
        customer_id = customer.id

    search_response = client.get("/customers?q=Morgan")
    assert search_response.status_code == 200
    assert b"Morgan Customer" in search_response.data

    delete_response = client.post(
        f"/customers/delete/{customer_id}", follow_redirects=True
    )
    assert delete_response.status_code == 200
    assert b"Customer deleted successfully" in delete_response.data

    with app.app_context():
        assert db.session.get(Customer, customer_id) is None
