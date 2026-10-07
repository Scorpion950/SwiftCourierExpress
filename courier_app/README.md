# SwiftCourier Express

SwiftCourier Express is a Flask-based courier management system designed to handle parcel booking, shipment tracking, customer records, billing, reporting, and admin settings in a single web application.

## Overview

This project was built to manage the day-to-day operations of a courier business. It allows administrators to:

- log in securely to the admin dashboard
- register and manage customers
- book parcel shipments
- generate bills and receipts
- update parcel delivery statuses
- track shipments publicly via tracking links
- generate reports and export data
- manage company setup information

## Features

- Secure admin authentication
- Dashboard with summary statistics
- Customer management module
- Shipment booking and billing
- Tracking and status updates
- Public parcel tracking page
- Reports and CSV export
- Settings module for company information
- Error handling pages for 404 and database issues

## Tech Stack

- Python 3.11+
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Flask-Migrate 4.0.7
- PostgreSQL / Neon PostgreSQL
- psycopg2-binary 2.9.9
- Jinja2 + HTML + CSS + JavaScript
- pytest + pytest-flask
- Gunicorn

## Project Structure

```text
courier_app/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── cli.py
│   ├── errors.py
│   ├── extensions.py
│   └── utils.py
├── config.py
├── instance/
├── migrations/
├── tests/
├── .env.example
├── README.md
├── requirements.txt
├── run.py
├── seed.py
├── wsgi.py
└── Procfile
```

## Environment Setup

1. Create a Neon PostgreSQL project or prepare a PostgreSQL database.
2. Copy the connection string from your database provider and place it into a `.env` file.
3. Use `.env.example` as a template.
4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Seed the admin account and default settings:

```bash
python seed.py
```

6. Run the application:

```bash
python run.py
```

7. Open the app in a browser at:

```text
http://127.0.0.1:5000
```

Default admin login:

- Email: value from `ADMIN_EMAIL`
- Password: value from `ADMIN_PASSWORD`

## Production Run

```bash
gunicorn wsgi:app
```

## Testing

```bash
python -m pytest -q
```

## Notes

- Database URL format: `postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require`
- This app is configured to use PostgreSQL and works well with Neon.
- Passwords are hashed via Werkzeug before being stored.

## Manual testing checklist

1. Welcome page: open `/` and click Enter System to login.
2. Login: log in using the seeded admin email and password.
3. Dashboard: verify the six stat cards and recent shipments list load.
4. Book Shipment: go to `/book`, fill the sender and receiver details, then submit and confirm the bill page loads.
5. Bill page: use the Print Bill / Slip button and Save Bill HTML link.
6. Track / Update: go to `/track`, find a shipment by tracking number, update the status, and confirm the timeline updates.
7. Customers: go to `/customers`, add a customer, search for them, and test deletion restriction for customers with shipments.
8. Reports: go to `/reports`, generate a report, export CSV, and confirm the summary values update.
9. Settings: update company details, save, and verify they appear on the bill header.
10. Public tracking: open `/t/<tracking>` and confirm the status timeline is visible without logging in.
11. Error pages: confirm the 404 page loads for a missing page and the database-down page is shown if the database is unreachable.

## Notes

- Database URL format: `postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require`
- Use `pool_pre_ping=True` and `pool_recycle=300` to handle Neon idle compute restarts.
- All admin passwords are hashed via Werkzeug before storage.
