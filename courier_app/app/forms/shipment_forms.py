"""Shipment-related form definitions."""

from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.utils.validators import validate_phone


class BookShipmentForm(FlaskForm):
    """Form for creating a new shipment booking."""

    sender_name = StringField("Sender Name", validators=[DataRequired(), Length(min=2, max=120)])
    sender_phone = StringField("Sender Phone", validators=[DataRequired(), validate_phone])
    receiver_name = StringField("Receiver Name", validators=[DataRequired(), Length(min=2, max=120)])
    receiver_phone = StringField("Receiver Phone", validators=[DataRequired(), validate_phone])
    origin = StringField("Origin", validators=[DataRequired(), Length(min=2, max=120)])
    destination = StringField("Destination", validators=[DataRequired(), Length(min=2, max=120)])
    parcel_type = SelectField(
        "Parcel Type",
        choices=[("Documents", "Documents"), ("Parcel", "Parcel"), ("Fragile", "Fragile"), ("Heavy", "Heavy")],
        validators=[DataRequired()],
    )
    service_type = SelectField(
        "Service Type",
        choices=[("Standard", "Standard"), ("Express", "Express"), ("International", "International")],
        validators=[DataRequired()],
    )
    weight_kg = FloatField("Weight (kg)", validators=[DataRequired(), NumberRange(min=0.01)])
    length_cm = FloatField("Length (cm)", validators=[DataRequired(), NumberRange(min=1)])
    width_cm = FloatField("Width (cm)", validators=[DataRequired(), NumberRange(min=1)])
    height_cm = FloatField("Height (cm)", validators=[DataRequired(), NumberRange(min=1)])
    charge = FloatField("Charge (Rs)", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Book Shipment")


class UpdateStatusForm(FlaskForm):
    """Form for updating a parcel status."""

    new_status = SelectField(
        "New Status",
        choices=[
            ("Booked", "Booked"),
            ("Picked Up", "Picked Up"),
            ("In Transit", "In Transit"),
            ("Out for Delivery", "Out for Delivery"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        validators=[DataRequired()],
    )
    remark = TextAreaField("Remark", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Update Status")


class TrackSearchForm(FlaskForm):
    """Form for searching a parcel by tracking number."""

    tracking_number = StringField("Tracking No", validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField("Find")
