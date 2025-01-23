from typing import override

from django.conf import settings
from rest_framework.views import APIView

from app.permissions import DJANGO_USER_PERMISSION_CLASSES, DJANGO_MOD_PERMISSION_CLASSES
from app.authentication import DJANGO_USER_AUTHENTICATION_CLASSES


class AnyView(APIView):
    """ inherit this class to create a view for unsecured requests """
    permission_classes = []
    authentication_classes = []


class UserView(APIView):
    """ inherit this class to create a view for unsecured requests """
    permission_classes = DJANGO_USER_PERMISSION_CLASSES
    authentication_classes = DJANGO_USER_AUTHENTICATION_CLASSES


class ModView(APIView):
    """ inherit this class to create a view for unsecured requests """
    permission_classes = DJANGO_MOD_PERMISSION_CLASSES
    authentication_classes = DJANGO_USER_AUTHENTICATION_CLASSES
