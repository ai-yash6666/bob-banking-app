from flask import Blueprint, render_template, session
from routes.auth import login_required
from services.account_service import get_balance

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    customer_id = session["customer_id"]
    balance = get_balance(customer_id)
    return render_template("dashboard.html", balance=balance)
