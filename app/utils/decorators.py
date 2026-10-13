"""Reusable decorators for access control."""

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(func):
    """Require an authenticated admin to access the route."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return decorated_view
