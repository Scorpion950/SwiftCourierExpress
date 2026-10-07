"""Authentication routes for admin login and logout."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.extensions import db
from app.forms.auth_forms import LoginForm
from app.models.admin import Admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate an admin user and start a session."""
    form = LoginForm()
    if form.validate_on_submit():
        admin = db.session.query(Admin).filter_by(email=form.email.data.lower().strip()).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash("Login successful.", "success")
            return redirect(url_for("dashboard.index"))
        flash("Invalid email or password.", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Log the current admin out and redirect to the welcome page."""
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("public.welcome"))
