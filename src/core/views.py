
from rest_framework.response import Response
from rest_framework.request import Request
from app.decorators import any_view, user_view, unverified_user_view


@any_view(['GET'])
def health(request: Request):
    """ health endpoint to test any_view """
    return Response(status=200, data={'msg': 'hello world!'})

@unverified_user_view(['GET'])
def secure_health(request: Request):
    return Response(status=200, data={'msg': 'hello secure world!'})

@unverified_user_view(['GET'])
def permissions(request: Request):
    return Response(status=200, data=request.user.permissions or [])

@user_view(['GET'])
def permissions(request: Request):
    return Response(status=200, data=request.user.permissions or [])
