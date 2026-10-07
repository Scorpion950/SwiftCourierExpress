"""Authentication form definitions."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Admin login form."""

    email = StringField("Username", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
