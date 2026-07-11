"""
Shared pytest fixtures for the test suite.

Every test module that needs the Flask app or a DB-backed test client
can simply import `app_with_db` or `client` from here via conftest auto-discovery.
"""
import sys
import os

# Make BACKEND/ importable when tests are run from the BACKEND directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from flask import Flask
from database import db as _db
from models import Customer, Account
from werkzeug.security import generate_password_hash


def make_test_app():
    """Create a minimal Flask app configured for testing with an in-memory DB."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    frontend_dir = os.path.join(base_dir, "..", "FRONTEND")

    app = Flask(
        __name__,
        template_folder=os.path.join(frontend_dir, "templates"),
        static_folder=os.path.join(frontend_dir, "static"),
    )
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
    )
    _db.init_app(app)

    with app.app_context():
        import models  # noqa: F401 — register table metadata
        _db.create_all()
        _seed()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp
    from errors import register_error_handlers

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    register_error_handlers(app)

    return app


def _seed():
    customer = Customer(
        username="testuser",
        password_hash=generate_password_hash("password123"),
    )
    _db.session.add(customer)
    _db.session.flush()
    account = Account(customer_id=customer.id, balance=1000.00)
    _db.session.add(account)
    _db.session.commit()


@pytest.fixture
def flask_app():
    app = make_test_app()
    yield app
    # Tear down in-memory DB after each test
    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()
