# wallet/services.py
from decimal import Decimal

# Temporary fixed rate (we'll connect Yara Cash later)
USDT_TO_NGN_RATE = Decimal("1500.00")

def usdt_to_local(usdt_amount):
    return Decimal(usdt_amount) * USDT_TO_NGN_RATE