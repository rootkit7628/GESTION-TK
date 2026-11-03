"""PIN hashing and the shuffled keypad. Only standard library primitives."""

import hashlib
import hmac
import random
import secrets

ITERATIONS = 310_000
PIN_LENGTH = 6
MAX_ATTEMPTS = 3
LOCK_MINUTES = 15


def hash_pin(pin: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def check_pin(pin: str, stored: str) -> bool:
    try:
        algo, iterations, salt, digest = stored.split("$")
    except ValueError:
        return False
    if algo != "pbkdf2_sha256":
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", pin.encode(), bytes.fromhex(salt), int(iterations))
    return hmac.compare_digest(candidate.hex(), digest)


def valid_pin(pin: str) -> bool:
    return len(pin) == PIN_LENGTH and pin.isdigit()


def keypad_layout(rng: random.Random | None = None) -> list[str]:
    """The ten digits in a new random order at each login, as on online-banking keypads."""
    digits = list("0123456789")
    (rng or secrets.SystemRandom()).shuffle(digits)
    return digits
