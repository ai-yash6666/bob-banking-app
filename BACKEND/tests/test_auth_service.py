"""Unit tests for services/auth_service.py."""
import pytest
from services.auth_service import verify_credentials, hash_password


class TestVerifyCredentials:
    def test_correct_credentials_returns_customer(self, flask_app):
        with flask_app.app_context():
            customer = verify_credentials("testuser", "password123")
            assert customer is not None
            assert customer.username == "testuser"

    def test_wrong_password_returns_none(self, flask_app):
        with flask_app.app_context():
            result = verify_credentials("testuser", "wrongpassword")
            assert result is None

    def test_unknown_username_returns_none(self, flask_app):
        with flask_app.app_context():
            result = verify_credentials("nobody", "password123")
            assert result is None

    def test_empty_password_returns_none(self, flask_app):
        with flask_app.app_context():
            result = verify_credentials("testuser", "")
            assert result is None


class TestHashPassword:
    def test_hash_differs_from_plain_text(self):
        plain = "mysecretpassword"
        hashed = hash_password(plain)
        assert hashed != plain

    def test_hash_is_verifiable(self):
        from werkzeug.security import check_password_hash
        plain = "anotherpassword"
        hashed = hash_password(plain)
        assert check_password_hash(hashed, plain)
