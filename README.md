# SecureBank — Banking Web Application

A simple browser-based banking application built with Python Flask, Jinja2 templates, Bootstrap 5, and SQLite. Customers can log in, view their account balance, deposit funds, and withdraw funds — all from a clean, responsive UI.

---

## Project Structure

```
banking-workshop/
├── FRONTEND/
│   ├── templates/
│   │   ├── base.html          # Shared layout: Bootstrap, navbar, flash messages
│   │   ├── login.html         # Login form
│   │   └── dashboard.html     # Balance display + deposit / withdraw forms
│   └── static/css/
│       └── custom.css         # Minor style overrides
│
├── BACKEND/
│   ├── app.py                 # Flask entry point
│   ├── config.py              # App configuration (secret key, DB path, debug flag)
│   ├── models.py              # SQLAlchemy models: Customer, Account
│   ├── database.py            # DB initialisation and seed data
│   ├── errors.py              # 404 / 500 error handlers
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   ├── auth.py            # /login, /logout + login_required guard
│   │   ├── dashboard.py       # /dashboard
│   │   └── transactions.py    # /deposit, /withdraw
│   ├── services/
│   │   ├── auth_service.py    # Password hashing / verification
│   │   └── account_service.py # Balance read / deposit / withdraw logic
│   └── tests/
│       ├── conftest.py        # Shared fixtures (in-memory SQLite test app)
│       ├── test_auth_service.py
│       ├── test_account_service.py
│       └── test_integration.py
│
├── IMPLEMENTATION_PLAN.md
├── STEP_BY_STEP_IMPLEMENTATION_GUIDE.md
└── README.md
```

---

## Prerequisites

| Tool | Minimum version | Check |
|---|---|---|
| Python | 3.9+ | `python --version` |
| pip | Bundled with Python | `pip --version` |

No external database server or build pipeline is required.

---

## Local Setup & Run

### 1 — Install dependencies

Open a terminal and navigate to the `BACKEND/` folder:

```bash
cd banking-workshop/BACKEND
pip install -r requirements.txt
```

### 2 — Start the Flask development server

```bash
python app.py
```

On first run the application automatically:
- Creates `BACKEND/banking.db` (SQLite database file).
- Creates the `customer` and `account` tables.
- Seeds a test customer with a starting balance of **$1,000.00**.

Expected output:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 3 — Open the app

Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
You will be redirected to the login page automatically.

### 4 — Log in with the demo account

| Field | Value |
|---|---|
| Username | `testuser` |
| Password | `password123` |

### 5 — Stop the server

Press **Ctrl + C** in the terminal.

---

## Running the Tests

All tests use an in-memory SQLite database — no setup required.

```bash
cd banking-workshop/BACKEND
python -m pytest tests/ -v
```

Expected: **29 passed**.

---

## Features

| Feature | Description |
|---|---|
| Login / Logout | Secure cookie-based session (only customer ID stored). Passwords hashed with Werkzeug. |
| Dashboard | Displays current account balance fetched fresh from the database on every request. |
| Deposit | Accepts any positive amount; balance updated immediately. |
| Withdraw | Accepts any positive amount up to the current balance; overdrafts are rejected with a clear error message. |
| Flash messages | One-time success / error alerts displayed via Bootstrap alerts. |
| Responsive UI | Bootstrap 5 grid — forms stack on mobile, side-by-side on desktop. |
| Auth guard | All protected routes redirect unauthenticated users to `/login`. |
| Error pages | Custom 404 and 500 pages — no stack traces exposed to the browser. |

---

## Application URLs

| URL | Method | Description |
|---|---|---|
| `/` | — | Redirects to `/login` |
| `/login` | GET, POST | Login page |
| `/logout` | GET | Clears session, redirects to `/login` |
| `/dashboard` | GET | Balance + transaction forms (auth required) |
| `/deposit` | POST | Deposit funds (auth required) |
| `/withdraw` | POST | Withdraw funds (auth required) |

---

## Production Considerations

> The Flask development server is **not suitable for production**.

Before deploying:

- Set `DEBUG = False` in `config.py`.
- Replace `SECRET_KEY` with a strong random value loaded from an environment variable.
- Serve with a production WSGI server: **Gunicorn** (Linux/Mac) or **Waitress** (Windows).
- Place behind a reverse proxy (e.g. Nginx) with HTTPS/TLS.
- Consider migrating from SQLite to PostgreSQL for concurrent workloads.
- Add CSRF protection (Flask-WTF) to all POST forms.
