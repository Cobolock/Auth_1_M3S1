import os


AUTHENTICATION_BACKENDS = [
    'users.auth.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_API_LOGIN_URL = f"http://{os.environ.get("AUTH_IP")}:{os.environ.get("AUTH_PORT")}/api/v1/user/login"
JWT_SECRET = os.environ.get("JWT_SECRET")