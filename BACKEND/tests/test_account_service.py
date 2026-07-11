"""Unit tests for services/account_service.py."""
import pytest
from services.account_service import get_balance, deposit, withdraw
from models import Customer, Account
from database import db
from werkzeug.security import generate_password_hash


class TestGetBalance:
    def test_returns_correct_balance(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            balance = get_balance(customer.id)
            assert balance == 1000.00


class TestDeposit:
    def test_increases_balance(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            new_balance = deposit(customer.id, 250.00)
            assert new_balance == 1250.00
            assert get_balance(customer.id) == 1250.00

    def test_rejects_zero_amount(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            with pytest.raises(ValueError):
                deposit(customer.id, 0)

    def test_rejects_negative_amount(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            with pytest.raises(ValueError):
                deposit(customer.id, -50)


class TestWithdraw:
    def test_decreases_balance_when_sufficient(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            new_balance = withdraw(customer.id, 300.00)
            assert new_balance == 700.00
            assert get_balance(customer.id) == 700.00

    def test_rejects_when_insufficient_funds(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            with pytest.raises(ValueError, match="Insufficient funds"):
                withdraw(customer.id, 9999.00)

    def test_balance_unchanged_after_failed_withdrawal(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            try:
                withdraw(customer.id, 9999.00)
            except ValueError:
                pass
            assert get_balance(customer.id) == 1000.00

    def test_withdraw_exact_balance_goes_to_zero(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            new_balance = withdraw(customer.id, 1000.00)
            assert new_balance == 0.00

    def test_rejects_zero_amount(self, flask_app):
        with flask_app.app_context():
            customer = Customer.query.filter_by(username="testuser").first()
            with pytest.raises(ValueError):
                withdraw(customer.id, 0)
