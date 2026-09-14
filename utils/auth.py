"""Password hashing + @login_required decorator. Owner: Kulankash."""
#This hashes passwords, verify the passwords, track whoever is using the app and block unauthenticated commands

import bcrypt
from functools import wraps


# Global session — set after login, cleared on logout
CURRENT_USER = {"user": None}


def hash_password(raw: str) -> str:

    # Return a bcrypt hash string for the plaintext password
    
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

    #bcrypt.gensalt are random bytes mixed into password before hashing and every user gets a diffreent salt so if users have the same password they can never produce the same hashes


def verify_password(raw: str, stored: str) -> bool:
    #returns true if raw matches the stored bcrypt hash, else fails

    try:
        return bcrypt.checkpw(raw.encode(), stored.encode())
    except(ValueError, AttributeError):
        return False


def login_required(func):
    """Block the function if no user is logged in."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CURRENT_USER["user"] is None:
            print("You must log in first.")
            return
        return func(*args, **kwargs)
    return wrapper

#@login_required Reuses the login check across many functions (DRY)
#wraps keeps the original function looking like itself when we use @login_required on a new function we preserve the new function identity so its now overridden with login required 