from database import db


class Customer(db.Model):
    """Represents a registered bank customer."""

    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # One-to-one relationship: each customer has exactly one account
    account = db.relationship("Account", backref="customer", uselist=False)

    def __repr__(self):
        return f"<Customer {self.username}>"


class Account(db.Model):
    """Represents a bank account linked to a customer."""

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<Account customer_id={self.customer_id} balance={self.balance}>"
