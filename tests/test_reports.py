"""Report generation tests."""

import re
from datetime import date

from app.extensions import db
from app.models.admin import Admin
from app.models.parcel import Parcel
from app.models.report import Report


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_reports_page_loads(client):
    login_admin(client)
    response = client.get("/reports")
    assert response.status_code == 200
    assert b"Shipment Reports" in response.data


def test_clear_shipments_form_sends_valid_csrf_token(client, app):
    app.config["WTF_CSRF_ENABLED"] = True
    with app.app_context():
        admin_id = db.session.query(Admin).filter_by(email="admin@example.com").one().id
    with client.session_transaction() as session:
        session["_user_id"] = str(admin_id)
        session["_fresh"] = True

    response = client.get("/reports")
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    clear_form = re.search(
        r'<form method="post" action="/reports/clear">(.*?)</form>',
        page,
        re.DOTALL,
    )
    assert clear_form is not None
    csrf_match = re.search(
        r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', clear_form.group(1)
    )
    assert csrf_match is not None

    rejected = client.post("/reports/clear", data={"confirmation": "DELETE"})
    assert rejected.status_code == 400

    accepted = client.post(
        "/reports/clear",
        data={"confirmation": "DELETE", "csrf_token": csrf_match.group(1)},
    )
    assert accepted.status_code == 302


def test_report_generation_and_csv_export_with_date_filters(client, app):
    login_admin(client)
    client.post(
        "/book",
        data={
            "sender_name": "Report Sender",
            "sender_phone": "1234567890",
            "receiver_name": "Report Receiver",
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
            "csrf_token": "",
        },
        follow_redirects=True,
    )

    with app.app_context():
        tracking_number = db.session.query(Parcel).one().tracking_number

    today = date.today().isoformat()
    report_response = client.post(
        "/reports",
        data={"from_date": today, "to_date": today, "status": "all"},
        follow_redirects=True,
    )
    assert report_response.status_code == 200
    assert b"Report generated successfully" in report_response.data
    assert tracking_number.encode() in report_response.data

    with app.app_context():
        report = db.session.query(Report).one()
        assert report.total_shipments == 1
        assert report.total_revenue == 225

    export_response = client.get(
        f"/reports/export?from_date={today}&to_date={today}&status=all"
    )
    assert export_response.status_code == 200
    assert export_response.mimetype == "text/csv"
    assert tracking_number.encode() in export_response.data
