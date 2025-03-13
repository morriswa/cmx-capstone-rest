
from rest_framework.response import Response
from rest_framework.request import Request
from app.decorators import any_view, user_view
from core import daos


#This is a simple health check endpoint to make sure the server is running KR
@any_view(['GET'])
def health(request: Request):
    """ health endpoint to test any_view """
    return Response(status=200, data={'msg': 'hello world!'})
#This is a simple health check endpoint to make sure the secure endpoints are working KR
@user_view(['GET'])
def secure_health(request: Request):
    return Response(status=200, data={'msg': 'hello secure world!'})
#This is a simple get endpoint to get the user's permissions KR
@user_view(['GET'])
def permissions(request: Request):
    return Response(status=200, data=request.user.permissions or [])
#This is a simple get endpoint to get the the history of the user's searches KR
@user_view(['GET'])
def get_search_history(request: Request):
    history = daos.get_search_history(request.user.user_id)
    return Response(status=200, data=[item.json() for item in history])
#This is a simple post endpoint to make a search prompt KR
@user_view(['POST'])
def post_search(request: Request):
    prompt_text = request.data.get('prompt_text')
    new_chat = daos.post_search(request.user.user_id, prompt_text)
    return Response(status=200, data=new_chat.json())
#This is to get the chat log for specific users. KR
@user_view(['GET'])
def get_chat_log(request: Request):
    result = daos.get_chat_log(request.user.user_id)
    return Response(status=200, data=result)

# @user_view(['GET'])
# def results_details(request: Request):
#     result = daos.get_result_details(request.user.user_id)
#     return Response(status=200, data=[item.json() for item in result])
# NOTE example for using ML builds to generate predictions...
# def thing_one():
#     from cmx_capstone_ml_morriswa.predict import predict
#     output = predict("string")
