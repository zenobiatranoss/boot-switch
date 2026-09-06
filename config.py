import hashlib

APP_NAME = "Boot Switch"
APP_VERSION = "1.0.0"
WINDOWS_NAME = "Windows Boot Manager"
CONFIRMATION_HASH = hashlib.sha256(b"1999").hexdigest()
COMMAND_TIMEOUT = 15
