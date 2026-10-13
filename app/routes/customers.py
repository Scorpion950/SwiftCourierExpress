"""Customer management routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.forms.customer_forms import CustomerForm
from app.services.customer_service import add_customer, delete_customer, search_customers

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    """Add, search, and delete customer records."""
    form = CustomerForm()
    query = request.args.get("q", "")

    if request.method == "POST" and form.validate_on_submit():
        add_customer(form.name.data, form.phone.data)
        flash("Customer added successfully.", "success")
        return redirect(url_for("customers.customers"))

    customers_list = search_customers(query)
    return render_template("customers/index.html", form=form, customers=customers_list, query=query)


@customers_bp.route("/customers/delete/<int:customer_id>", methods=["POST"])
@login_required
def delete_customer_route(customer_id):
    """Delete a customer if no shipments exist for them."""
    try:
        delete_customer(customer_id)
        flash("Customer deleted successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("customers.customers"))
