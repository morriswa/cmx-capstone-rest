import uuid

from app.exceptions import BadRequestException
from app.validation import is_blank
from rest_framework.response import Response
from rest_framework.request import Request

from app.decorators import any_view, user_view
from app import bedrock_client

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
def create_chat(request: Request):
    prompt_text = request.data.get('prompt_text')
    a = bedrock_client.ask(prompt_text)
    new_chat = daos.save_question_answer_pair(request.user.user_id, prompt_text,a)
    return Response(status=200, data=[item.json() for item in new_chat])

@user_view(['GET'])
def get_chat_log(request: Request, chat_id):
    """ This is to get a specific chat log """

    try:
        chat_uuid = uuid.UUID(chat_id)
    except ValueError:
        raise BadRequestException("required uuid path parameter 'chat_id'")

    result = daos.get_chat_log(request.user.user_id, chat_id)
    return Response(status=200, data=[item.json() for item in result])
