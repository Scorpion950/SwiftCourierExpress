"""Import all models so Flask-Migrate and SQLAlchemy can discover them."""

from app.models.admin import Admin
from app.models.customer import Customer
from app.models.parcel import Parcel
from app.models.parcel_info import ParcelInfo
from app.models.report import Report
from app.models.settings import Settings
from app.models.track_parcel import TrackParcel
