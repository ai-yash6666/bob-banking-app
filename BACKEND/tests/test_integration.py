"""Integration tests — full HTTP request/response cycle via Flask test client."""
import pytest


def login(client, username="testuser", password="password123"):
    """Helper: POST /login and return the response."""
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


class TestLoginFlow:
    def test_valid_credentials_redirect_to_dashboard(self, client):
        resp = login(client)
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

    def test_invalid_password_returns_login_page_with_error(self, client):
        resp = client.post(
            "/login",
            data={"username": "testuser", "password": "wrongpass"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Invalid username or password" in resp.data

    def test_unknown_user_returns_error(self, client):
        resp = client.post(
            "/login",
            data={"username": "ghost", "password": "password123"},
            follow_redirects=True,
        )
        assert b"Invalid username or password" in resp.data


class TestDashboardGuard:
    def test_unauthenticated_redirects_to_login(self, client):
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

    def test_authenticated_can_reach_dashboard(self, client):
        login(client)
        resp = client.get("/dashboard", follow_redirects=True)
        assert resp.status_code == 200
        assert b"1000" in resp.data  # balance should appear


class TestDepositFlow:
    def test_valid_deposit_redirects_and_updates_balance(self, client):
        login(client)
        resp = client.post("/deposit", data={"amount": "500"}, follow_redirects=True)
        assert resp.status_code == 200
        assert b"1500" in resp.data

    def test_zero_deposit_shows_error(self, client):
        login(client)
        resp = client.post("/deposit", data={"amount": "0"}, follow_redirects=True)
        assert b"greater than zero" in resp.data

    def test_deposit_unauthenticated_redirects(self, client):
        resp = client.post("/deposit", data={"amount": "100"}, follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]


class TestWithdrawFlow:
    def test_valid_withdrawal_updates_balance(self, client):
        login(client)
        resp = client.post("/withdraw", data={"amount": "200"}, follow_redirects=True)
        assert resp.status_code == 200
        assert b"800" in resp.data

    def test_insufficient_funds_shows_error(self, client):
        login(client)
        resp = client.post("/withdraw", data={"amount": "9999"}, follow_redirects=True)
        assert b"Insufficient funds" in resp.data

    def test_insufficient_funds_balance_unchanged(self, client):
        login(client)
        client.post("/withdraw", data={"amount": "9999"}, follow_redirects=True)
        resp = client.get("/dashboard", follow_redirects=True)
        assert b"1000" in resp.data

    def test_withdraw_unauthenticated_redirects(self, client):
        resp = client.post("/withdraw", data={"amount": "100"}, follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]


class TestLogoutFlow:
    def test_logout_clears_session_and_redirects(self, client):
        login(client)
        resp = client.get("/logout", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

    def test_after_logout_dashboard_redirects_to_login(self, client):
        login(client)
        client.get("/logout")
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]
