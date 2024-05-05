import http
import json
from enum import StrEnum, auto
from jose import jwt, JWTError

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as UserType
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class Roles(StrEnum):
    ADMIN = auto()
    SUBSCRIBER = auto()
    STAFF = auto()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None) -> UserType | None:
        url = settings.AUTH_API_LOGIN_URL
        payload = {'username': username, 'password': password}
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()
        try:
            token = jwt.decode(
                token=data['access_token'],
                key=settings.JWT_SECRET,
                algorithms=['HS256'],
            )
        except JWTError:
            return None

        try:
            profile = Profile.objects.filter(uuid=token['id']).first()
            if profile:
                user = User.objects.get(auth_profile__uuid=token['id'])
            if not profile:
                user = User.objects.create()
                user.auth_profile.uuid = token.get('id')
                user.username = token.get('sub')
                user.first_name = token.get('first_name') or ''
                user.last_name = token.get('last_name', '') or ''
            user.is_staff = Roles.STAFF in (token.get('roles') or [])
            user.is_superuser = Roles.ADMIN in (token.get('roles') or [])
            user.is_active = token.get('enabled')
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
