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
SwiftCourierExpress/
├── app/                    # Routes, models, services, templates, CSS and JS
├── instance/               # Local database files (not committed)
├── migrations/             # Database migration scripts
├── tests/                  # Automated tests
├── .env                    # Your local settings (create this; never commit)
├── .env.example            # Safe configuration template
├── .gitignore
├── README.md
├── SwiftCourier_Express_Project_Info.txt
├── requirements.txt
├── run.py                  # Local development entry point
├── seed.py                 # Creates database tables and starter admin/settings
├── wsgi.py                 # Production WSGI entry point
└── Procfile
```

## Setup and Run (Windows)

Example .env values (replace the placeholders with your own settings):

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
SECRET_KEY=replace-with-a-long-random-secret
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=replace-with-a-strong-password
```

The .env file belongs in the repository's top-level folder, beside run.py and README.md. It contains local settings and must not be committed. Commit .env.example instead.

Open the SwiftCourierExpress project folder in VS Code. Then follow these steps in the VS Code integrated terminal:

1. Open Terminal > New Terminal. Make sure the terminal's current folder contains this README and run.py.
2. Create the Python virtual environment: `py -3.11 -m venv .venv`
3. Install the project packages: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Create your local environment file: `copy .env.example .env`
5. Open .env from the VS Code Explorer. Replace the sample database URL with your PostgreSQL/Neon connection string, and set a private SECRET_KEY, ADMIN_EMAIL, and strong ADMIN_PASSWORD. Save the file.
6. Create the database tables and configured admin/settings row: `.\.venv\Scripts\python.exe seed.py`
7. Start the development server: `.\.venv\Scripts\python.exe run.py`
8. Open http://127.0.0.1:5000 in your browser.
9. When finished, stop the server with Ctrl+C in the VS Code terminal.

### Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Production

On a supported Linux deployment environment, start the WSGI app with:

```bash
gunicorn wsgi:app
```

The admin login identifier and password are the values you set in .env. The identifier is stored in the admin email column and may be username-style. Admin passwords are hashed before storage. Keep database credentials and secret keys private.

## Database Notes

- The application uses PostgreSQL through psycopg2-binary; Neon PostgreSQL is supported.
- Database URL format: postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require.
- SQLAlchemy uses pool_pre_ping=True and pool_recycle=300 for reliable hosted database connections.

## Manual testing checklist

1. Welcome page: open / and click Enter System to login.
2. Login: log in using the seeded admin email and password.
3. Dashboard: verify the six stat cards and recent shipments list load.
4. Book Shipment: go to /book, fill the sender and receiver details, then submit and confirm the bill page loads.
5. Bill page: use the Print Bill / Slip button and Save Bill HTML link.
6. Track / Update: go to /track, find a shipment by tracking number, update the status, and confirm the timeline updates.
7. Customers: go to /customers, add a customer, search for them, and test deletion restriction for customers with shipments.
8. Reports: go to /reports, generate a report, export CSV, and confirm the summary values update.
9. Settings: update company details, save, and verify they appear on the bill header.
10. Public tracking: open /t/<tracking> and confirm the status timeline is visible without logging in.
11. Error pages: confirm the 404 page loads for a missing page and the database-down page is shown if the database is unreachable.

## Security

- Keep .env private and never commit database credentials, secret keys, or admin passwords.
- Commit .env.example only; it contains placeholder values.
