import hashlib
from config import CONFIRMATION_HASH

def check_password(value):
    if not value:
        return False
    return hashlib.sha256(value.encode()).hexdigest() == CONFIRMATION_HASH

def is_password_valid(value):
    return check_password(value)

def clear_password(value):
    return ""
