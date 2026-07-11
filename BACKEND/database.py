from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialise SQLAlchemy with the Flask app, create tables, and seed test data."""
    db.init_app(app)

    with app.app_context():
        # Import models so SQLAlchemy is aware of the table definitions
        import models  # noqa: F401

        db.create_all()
        _seed(app)


def _seed(app):
    """Insert a test customer and account if they don't already exist (idempotent)."""
    from werkzeug.security import generate_password_hash
    from models import Customer, Account

    existing = Customer.query.filter_by(username="testuser").first()
    if existing:
        return

    customer = Customer(
        username="testuser",
        password_hash=generate_password_hash("password123"),
    )
    db.session.add(customer)
    db.session.flush()  # assign customer.id before using it

    account = Account(customer_id=customer.id, balance=1000.00)
    db.session.add(account)
    db.session.commit()
