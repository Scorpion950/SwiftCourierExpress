"""Customer form definitions."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.utils.validators import validate_phone


class CustomerForm(FlaskForm):
    """Form for adding a customer record."""

    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField("Phone", validators=[DataRequired(), validate_phone])
    submit = SubmitField("Add")
