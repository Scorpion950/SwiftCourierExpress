"""Business logic for shipment booking and tracking updates."""

from datetime import datetime

from app.extensions import db
from app.models.customer import Customer
from app.models.parcel import Parcel
from app.models.parcel_info import ParcelInfo
from app.models.track_parcel import TrackParcel
from app.utils.tracking import generate_tracking_number


def get_customer_by_name_phone(name, phone):
    """Locate a customer by name and phone number."""
    return db.session.query(Customer).filter_by(name=name.strip(), phone=phone.strip()).first()


def book_shipment(data, admin_id):
    """Create a parcel and its initial tracking history entry."""
    sender = get_customer_by_name_phone(data["sender_name"], data["sender_phone"])
    if sender is None:
        sender = Customer(name=data["sender_name"].strip(), phone=data["sender_phone"].strip())
        db.session.add(sender)
        db.session.flush()

    tracking_number = generate_tracking_number()
    parcel = Parcel(
        tracking_number=tracking_number,
        sender_id=sender.id,
        sender_name=sender.name,
        sender_phone=sender.phone,
        receiver_name=data["receiver_name"].strip(),
        receiver_phone=data["receiver_phone"].strip(),
        origin=data["origin"].strip(),
        destination=data["destination"].strip(),
        parcel_type=data["parcel_type"],
        service_type=data["service_type"],
        status="Booked",
        booked_by=admin_id,
        created_at=datetime.utcnow(),
    )
    db.session.add(parcel)
    db.session.flush()

    parcel_info = ParcelInfo(
        parcel_id=parcel.id,
        weight_kg=float(data["weight_kg"]),
        length_cm=float(data["length_cm"]),
        width_cm=float(data["width_cm"]),
        height_cm=float(data["height_cm"]),
        price=float(data["charge"]),
    )
    db.session.add(parcel_info)

    history = TrackParcel(
        parcel_id=parcel.id,
        tracking_number=tracking_number,
        status="Booked",
        remark="Shipment booked",
        updated_by=admin_id,
        timestamp=datetime.utcnow(),
    )
    db.session.add(history)
    db.session.commit()
    return parcel


def get_by_tracking(tracking_number):
    """Load a parcel with its info and tracking history by tracking number."""
    return db.session.query(Parcel).filter_by(tracking_number=tracking_number).first()


def update_status(tracking_number, new_status, remark, updated_by):
    """Update parcel status and log the change in tracking history."""
    parcel = get_by_tracking(tracking_number)
    if not parcel:
        return None

    parcel.status = new_status
    db.session.add(
        TrackParcel(
            parcel_id=parcel.id,
            tracking_number=parcel.tracking_number,
            status=new_status,
            remark=remark or "Status updated",
            updated_by=updated_by,
            timestamp=datetime.utcnow(),
        )
    )
    db.session.commit()
    return parcel
