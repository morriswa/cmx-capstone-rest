
from rest_framework.response import Response
from rest_framework.request import Request

from app.decorators import any_view, user_view



@any_view(['GET'])
def health(request: Request):
    """ This is a simple health check endpoint to make sure the server is running KR """
    return Response(status=200, data={'msg': 'hello world!'})

@user_view(['GET'])
def secure_health(request: Request):
    """ This is a simple health check endpoint to
    make sure the secure endpoints are working KR """
    return Response(status=200, data={'msg': 'hello secure world!'})

@user_view(['GET'])
def permissions(request: Request):
    """ This is a simple get endpoint to get the user's permissions KR """
    return Response(status=200, data=request.user.permissions or [])
