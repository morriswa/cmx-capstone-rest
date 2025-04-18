
import logging
import jwt
from typing import override, Optional

from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework import exceptions

from .utils import *
from .daos import *
from .models import User


__all__ = [
    "UserAuthenticationWithJwt",
    "User",
    "DJANGO_USER_AUTHENTICATION_CLASSES"
]


class UserAuthenticationWithJwt(BaseAuthentication):
    """ provides jwt authentication filter, imported in drf """
    @override
    def authenticate(self, request) -> Optional[tuple[User, dict]]:
        """ :return None if auth request was rejected, else User, Auth tuple """
        token = get_token_auth_header(request)
        if token is None:  # if no auth header is found the user is not authenticated
            raise exceptions.AuthenticationFailed('Failed to provide Authorization header', code=401)

        try:
            # attempt decoding auth header as jwt
            payload = jwt_decode_token(token)
            # extract token permissions and email
            jwt_permissions:list = payload.get('permissions')
            email = payload.get('email')

            # attempt retrieving user info from db using authentication email
            user_id = get_user_info(email)

            # create custom django user with retrieved info
            user = User(email=email, user_id=user_id, jwt_permissions=jwt_permissions)
            logging.info(f'successfully authenticated user {user.user_id} '
                         f'with email {user.email} and granted permissions {user.permissions}')
            return user, payload

        # handle common jwt errors
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Error decoding token.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')
        except Exception as e:
            logging.error(e)
            raise exceptions.AuthenticationFailed('Failed to authenticate, no further details.')

DJANGO_USER_AUTHENTICATION_CLASSES = [BasicAuthentication, SessionAuthentication, UserAuthenticationWithJwt]
