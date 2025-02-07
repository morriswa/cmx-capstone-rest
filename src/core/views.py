
from rest_framework.response import Response

from app.decorators import any_view, user_view, unverified_user_view


@any_view(['GET'])
def health(request):
    return Response(status=200, data={'msg': 'hello world!'})

@unverified_user_view(['GET'])
def secure_health(request):
    return Response(status=200, data={'msg': 'hello secure world!'})

@unverified_user_view(['GET'])
def permissions(request):
    return Response(status=200, data=request.user.permissions or [])

# NOTE example for using ML builds to generate predictions...
# def thing_one():
#     from cmx_capstone_ml_morriswa.predict import predict
#     output = predict("string")
