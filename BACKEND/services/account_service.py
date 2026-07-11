from models import Account
from database import db


def get_balance(customer_id: int) -> float:
    """Return the current balance for the given customer."""
    account = Account.query.filter_by(customer_id=customer_id).first()
    if account is None:
        raise ValueError(f"No account found for customer_id={customer_id}")
    return account.balance


def deposit(customer_id: int, amount: float) -> float:
    """
    Add *amount* to the customer's balance.

    Returns the new balance.
    Raises ValueError if amount is not positive.
    """
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")

    account = Account.query.filter_by(customer_id=customer_id).first()
    if account is None:
        raise ValueError(f"No account found for customer_id={customer_id}")

    account.balance += amount
    db.session.commit()
    return account.balance


def withdraw(customer_id: int, amount: float) -> float:
    """
    Subtract *amount* from the customer's balance.

    Returns the new balance.
    Raises ValueError if amount is not positive or exceeds the current balance.
    """
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")

    account = Account.query.filter_by(customer_id=customer_id).first()
    if account is None:
        raise ValueError(f"No account found for customer_id={customer_id}")

    if amount > account.balance:
        raise ValueError(
            f"Insufficient funds. Your current balance is ${account.balance:,.2f}."
        )

    account.balance -= amount
    db.session.commit()
    return account.balance
