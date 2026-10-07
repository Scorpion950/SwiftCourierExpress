"""Report filter form definitions."""

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class ReportFilterForm(FlaskForm):
    """Filter form for shipment reports."""

    from_date = DateField("From Date", format="%Y-%m-%d", validators=[Optional()])
    to_date = DateField("To Date", format="%Y-%m-%d", validators=[Optional()])
    status = SelectField(
        "Status",
        choices=[("all", "All"), ("Booked", "Booked"), ("Picked Up", "Picked Up"), ("In Transit", "In Transit"), ("Out for Delivery", "Out for Delivery"), ("Delivered", "Delivered"), ("Cancelled", "Cancelled")],
        default="all",
    )
    submit = SubmitField("Generate")
