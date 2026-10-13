"""Company settings form definitions."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

from app.utils.validators import validate_phone


class SettingsForm(FlaskForm):
    """Form for updating company details."""

    company_name = StringField("Company Name", validators=[DataRequired(), Length(min=2, max=180)])
    tagline = StringField("Tagline", validators=[Optional(), Length(max=180)])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), validate_phone])
    email = StringField("Email", validators=[Optional(), Email()])
    submit = SubmitField("Save Settings")
