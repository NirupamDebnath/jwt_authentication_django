from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import authentication, exceptions

from authentication.utils import decode_access_token

import logging
logger = logging.getLogger(__name__)


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if auth_data is None or auth_data == b'':
            return None

        logger.info(auth_data)

        _, token = auth_data.decode('utf-8').split(' ')
        payload = decode_access_token(token)

        User = get_user_model()
        try:
            user = User.objects.get(username=payload.get("username", ""))
        except ObjectDoesNotExist:
            logger.exception(
                "User doesn't exists for user.pk : {}".format(
                    payload.get("pk", "")))

            raise exceptions.AuthenticationFailed(
                "Authentication failed.")
        except Exception:
            logger.exception("Authentication exception")
            raise exceptions.AuthenticationFailed(
                "Authentication failed.")

        return user, token
