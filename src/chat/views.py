import uuid

from rest_framework.response import Response
from rest_framework.request import Request

from app import bedrock_client
from app.decorators import user_view
from app.exceptions import BadRequestException

from chat import daos



@user_view(['GET'])
def get_search_history(request: Request):
    """ This is a simple get endpoint to get
    the the history of the user's searches KR """
    history = daos.get_search_history(request.user.user_id)
    return Response(status=200, data=[item.json() for item in history])

@user_view(['POST'])
def create_chat(request: Request):
    """This is a simple post endpoint
    to make a search prompt KR"""
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
