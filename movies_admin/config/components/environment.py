import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INTERNAL_IPS = ["127.0.0.1", "localhost"]
