from werkzeug.security import check_password_hash, generate_password_hash
from models import Customer


def verify_credentials(username: str, password: str):
    """
    Look up a customer by username and verify their password.

    Returns the Customer object on success, or None on failure.
    """
    customer = Customer.query.filter_by(username=username).first()
    if customer is None:
        return None
    if not check_password_hash(customer.password_hash, password):
        return None
    return customer


def hash_password(plain: str) -> str:
    """Return a Werkzeug-hashed version of the given plain-text password."""
    return generate_password_hash(plain)
