# Banking Web Application — Implementation Plan

---

## 1. Solution Overview

### Objective
Build a simple, browser-based banking web application that allows registered customers to securely log in, view their account balance, and perform basic financial transactions (deposit and withdrawal), all backed by a lightweight Python Flask API and a local SQLite database.

### Scope

**In scope:**
- Customer login and session management
- Authenticated dashboard with account summary
- View current account balance
- Deposit funds into the account
- Withdraw funds from the account (with basic balance validation)
- Logout and session termination

**Out of scope:**
- Customer registration / self-service account creation
- Multi-account support per customer
- Fund transfers between accounts
- Transaction history / statement download
- Admin or teller portal
- Password reset or two-factor authentication

### Users
| Persona | Description |
|---|---|
| **Bank Customer** | A pre-registered individual who logs in to view and manage their single account. |

### Functional Requirements
| ID | Requirement |
|---|---|
| FR-01 | A customer must authenticate with a username and password before accessing any feature. |
| FR-02 | An authenticated customer can view their current account balance on the dashboard. |
| FR-03 | An authenticated customer can deposit a positive monetary amount; the balance updates immediately. |
| FR-04 | An authenticated customer can withdraw a positive monetary amount up to their available balance. |
| FR-05 | The system must prevent overdrafts — withdrawals exceeding the current balance are rejected. |
| FR-06 | A customer can log out, which terminates their session immediately. |
| FR-07 | Unauthenticated requests to protected pages must be redirected to the login page. |

### Non-Functional Requirements
| ID | Requirement |
|---|---|
| NFR-01 | Passwords must be stored as hashed values — never plain text. |
| NFR-02 | All session tokens must be server-side and expire on logout. |
| NFR-03 | The UI must be responsive and usable on both desktop and mobile browsers (Bootstrap). |
| NFR-04 | All backend responses must return appropriate HTTP status codes. |
| NFR-05 | The application should be runnable locally with zero external infrastructure beyond Python and a browser. |

### Assumptions
- Customer accounts are pre-seeded in the database; there is no self-registration flow.
- A single SQLite file is sufficient for the expected local/demo workload.
- Bootstrap is loaded via CDN; no custom build pipeline is required.
- The Flask development server is acceptable for local use; production hardening is out of scope.
- A single account is associated with each customer login.

---

## 2. High-Level Architecture

See STEP_BY_STEP_IMPLEMENTATION_GUIDE.md for the full architecture diagram.

---

## 3. Folder Structure

```
banking-workshop/
│
├── FRONTEND/                        # All browser-facing assets
│   ├── templates/                   # Jinja2 HTML templates (served by Flask)
│   │   ├── base.html                # Shared layout: Bootstrap, navbar, flash messages
│   │   ├── login.html               # Customer login form
│   │   └── dashboard.html           # Balance display + deposit/withdraw forms
│   └── static/                      # Static assets
│       └── css/
│           └── custom.css
│
├── BACKEND/                         # All server-side code
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── database.py
│   ├── errors.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   └── transactions.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── account_service.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth_service.py
│       ├── test_account_service.py
│       └── test_integration.py
│
├── IMPLEMENTATION_PLAN.md
├── STEP_BY_STEP_IMPLEMENTATION_GUIDE.md
└── README.md
```

---

*End of Implementation Plan*
