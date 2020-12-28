import datetime
from typing import Tuple

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import exceptions

import jwt
from decouple import config

User = get_user_model()

algorithm = 'HS256'


def get_token(payload: dict, secret: str) -> bytes:
    access = jwt.encode(
        payload,
        secret,
        algorithm=algorithm
    )
    return access


def decode_token(token: bytes, secret: str) -> dict:
    try:
        return jwt.decode(token, secret)
    except jwt.DecodeError as identifier:
        raise exceptions.AuthenticationFailed(
            "Authentication failed. Invalid refresh token.")
    except jwt.ExpiredSignatureError as identifier:
        raise exceptions.AuthenticationFailed(
            "Authentication failed. Token expired.")


def get_token_for_user(user: User, secret: str, minutes: int) -> bytes:
    payload = {
        'username': user.username,
        'email': user.email,
        'pk': user.pk,
        'exp': timezone.now() + datetime.timedelta(minutes=minutes)
    }
    access = get_token(payload, secret)
    return access


def get_token_pair_for_user(user: User) -> Tuple[bytes, bytes]:
    access = get_token_for_user(user, config("JWT_SECRET"), 5)
    refresh = get_token_for_user(user, config("JET_REFRESH_SECRET"), 60)
    return access, refresh


def decode_access_token(token):
    return decode_token(token, config("JWT_SECRET"))


def refresh_token_pair(refresh_token: bytes) -> Tuple[bytes, bytes]:
    payload = decode_token(refresh_token, config("JET_REFRESH_SECRET"))
    payload['exp'] = timezone.now() + datetime.timedelta(minutes=5)
    access = get_token(payload, config("JWT_SECRET"))
    payload['exp'] = timezone.now() + datetime.timedelta(minutes=60)
    refresh = get_token(payload, config("JET_REFRESH_SECRET"))
    return access, refresh
