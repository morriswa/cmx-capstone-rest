
from uuid import UUID

from django.conf import settings


class User:
    """ represents a user and stores important authentication info """
    def __init__(self, **kwargs):
        self.user_id: UUID = kwargs.get('user_id')
        self.email: str = kwargs.get('email')
        self.username: str = self.email
        self.__jwt_permissions: list[str] = kwargs.get('jwt_permissions') or []
        self.__db_permissions: list[str] = kwargs.get('db_permissions') or []

    @property
    def permissions(self) -> list[str]:
        # add token permissions
        perms = [*self.__jwt_permissions, *self.__db_permissions]

        return perms

    @property
    def is_authenticated(self) -> bool:
        # users without an id, email, or username will not be considered authenticated
        return (self.user_id is not None
                and self.email is not None
                and self.username is not None)
