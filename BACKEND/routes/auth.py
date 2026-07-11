from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import verify_credentials

auth_bp = Blueprint("auth", __name__)


def login_required(f):
    """Decorator that redirects to /login if no valid session exists."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "customer_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Already logged in — send straight to dashboard
    if "customer_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            error = "Please enter both username and password."
        else:
            customer = verify_credentials(username, password)
            if customer is None:
                error = "Invalid username or password."
            else:
                session.clear()
                session["customer_id"] = customer.id
                return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
