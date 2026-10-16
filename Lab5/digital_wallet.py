
"""Demonstration digital wallet with basic payment tracking."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.getenv("WALLET_GATEWAY_SECRET", "")
WALLET_PIN = os.getenv("WALLET_PIN", "")
wallet = {"balance": 0.0}
transactions = []


def hash_pin(pin):
    """Return a SHA-256 digest of the supplied PIN."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def add_money(amount, source="UPI", log=None):
    """Add money to the wallet and record the credit."""
    if amount <= 0:
        return False

    if log is None:
        log = []

    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat(),
    })
    log.append(amount)
    return True


def pay_merchant(merchant, amount, pin, daily_limit):
    """Validate a PIN and process a merchant payment."""
    if not WALLET_PIN or not hmac.compare_digest(
        hash_pin(pin), hash_pin(WALLET_PIN)
    ):
        print("Wrong PIN for payment to", merchant)
        return False

    if amount <= 0 or amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat(),
    })
    return True


def mini_statement(count=3):
    """Print the most recent wallet transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount):
    """Calculate the wallet's standard cashback amount."""
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Check whether the supplied gateway secret is valid."""
    return bool(GATEWAY_SECRET) and hmac.compare_digest(
        secret, GATEWAY_SECRET
    )


def receipt_path():
    """Create a secure temporary file for a receipt."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf", delete=False
    ) as receipt:
        return receipt.name


def main():
    """Run the digital wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)

    add_money(2000)
    add_money(500, "Card")
    add_money(-10)

    daily_limit = 1500
    pay_merchant("Coffee Corner", 180, "4321", daily_limit)
    pay_merchant("Book Store", 5000, "4321", daily_limit)
    pay_merchant("Grocery Mart", 350, "0000", daily_limit)
    pay_merchant("Pharmacy", 420, "4321", daily_limit)

    mini_statement()
    print("Cashback on 420:", cashback_for(420))
    print("Gateway check:", check_gateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])

    credit_amounts = [
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
