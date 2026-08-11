from datetime import UTC, datetime, timedelta, timezone
import random


def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def otp_expiry() -> datetime:
    return datetime.now() + timedelta(minutes=5)
