"""Report generation tests."""

from datetime import date

from app.extensions import db
from app.models.parcel import Parcel
from app.models.report import Report


def login_admin(client):
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"}, follow_redirects=True)


def test_reports_page_loads(client):
    login_admin(client)
    response = client.get("/reports")
    assert response.status_code == 200
    assert b"Shipment Reports" in response.data


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
