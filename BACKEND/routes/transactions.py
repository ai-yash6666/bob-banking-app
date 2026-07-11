from flask import Blueprint, request, redirect, url_for, session, flash
from routes.auth import login_required
from services import account_service

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/deposit", methods=["POST"])
@login_required
def deposit():
    customer_id = session["customer_id"]
    raw_amount = request.form.get("amount", "").strip()

    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Please enter a valid numeric amount.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        new_balance = account_service.deposit(customer_id, amount)
        flash(f"Successfully deposited ${amount:,.2f}. New balance: ${new_balance:,.2f}.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")

    return redirect(url_for("dashboard.dashboard"))


@transactions_bp.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    customer_id = session["customer_id"]
    raw_amount = request.form.get("amount", "").strip()

    if not raw_amount:
        flash("Amount is required", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Please enter a valid numeric amount.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    if amount <= 0:
        flash("Amount must be greater than zero", "danger")
        return redirect(url_for("dashboard.dashboard"))

    current_balance = account_service.get_balance(customer_id)
    if amount > current_balance:
        flash("Insufficient funds", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        new_balance = account_service.withdraw(customer_id, amount)
        flash(f"Successfully withdrew ${amount:,.2f}. New balance: ${new_balance:,.2f}.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")

    return redirect(url_for("dashboard.dashboard"))
