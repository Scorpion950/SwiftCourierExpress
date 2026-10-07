"""Business logic for customer records."""

from app.extensions import db
from app.models.customer import Customer
from app.models.parcel import Parcel


def add_customer(name, phone):
    """Create a new customer if one does not already exist."""
    clean_name = name.strip()
    clean_phone = phone.strip()
    customer = db.session.query(Customer).filter_by(name=clean_name, phone=clean_phone).first()
    if customer:
        return customer
    customer = Customer(name=clean_name, phone=clean_phone)
    db.session.add(customer)
    db.session.commit()
    return customer


def search_customers(query=None):
    """Return customers matching the optional search term."""
    q = db.session.query(Customer)
    if query:
        lookup = f"%{query.strip()}%"
        q = q.filter((Customer.name.ilike(lookup)) | (Customer.phone.ilike(lookup)))
    return q.order_by(Customer.created_at.desc()).all()


def delete_customer(customer_id):
    """Delete a customer only if they have no shipments."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        return False

    shipments = db.session.query(Parcel).filter_by(sender_id=customer_id).first()
    if shipments is not None:
        raise ValueError("Customer cannot be deleted because they have shipments on record.")

    db.session.delete(customer)
    db.session.commit()
    return True
