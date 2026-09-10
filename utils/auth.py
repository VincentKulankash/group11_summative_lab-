"""Password hashing + @login_required decorator. Owner: YOU."""
import hashlib
import os
from functools import wraps


# Global session — set after login, cleared on logout
CURRENT_USER = {"user": None}


def hash_password(raw: str) -> str:
    """Return 'salt$hash' string."""
    # TODO (YOU)
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", raw.encode(), bytes.fromhex(salt), 100_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(raw: str, stored: str) -> bool:
    """Check raw password against stored hash."""
    # TODO (YOU)
    try:
        salt, digest = stored.split("$")
    except (ValueError, AttributeError):
        return False
    check = hashlib.pbkdf2_hmac(
        "sha256", raw.encode(), bytes.fromhex(salt), 100_000
    ).hex()
    return check == digest


def login_required(func):
    """Block the function if no user is logged in."""
    # TODO (YOU)
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CURRENT_USER["user"] is None:
            print("✘ You must log in first.")
            return
        return func(*args, **kwargs)
    return wrapper