
import json

from app.exceptions import APIException
from app import database

from core.models import ChatLog, ChatBlurb
from core.views import any_view, user_view


#This function will get the search history of the user. KR
#It will return a list of prompts that the user has made. KR
#This function will later be updated with SQL statements to get the data from the database. KR
def get_search_history(user_id) -> list[ChatBlurb]:
    with database.cursor() as cur:
        cur.execute("""
            SELECT chat_id, q, created
            FROM chat_history
            WHERE user_id = %(user_id)s;
        """, {
            'user_id': user_id
        })
        rows = cur.fetchall()
        return [ChatBlurb(**row) for row in rows]


def get_chat_log(user_id, chat_id):
    with database.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM chat_history
            WHERE   chat_id = %(chat_id)s
                AND user_id = %(user_id)s
            ORDER BY created DESC
        """, {
            'chat_id': chat_id,
            'user_id': user_id
        })
        rows = cur.fetchall()
        return [ChatLog(**row) for row in rows]


def save_question_answer_pair(user_id, question, answer):
    chat_id = None
    with database.cursor() as cur:
        cur.execute("""
            INSERT INTO chat_history
                (user_id, q, a)
            VALUES
                (%(user_id)s, %(q)s, %(a)s)
            returning chat_id;
        """,{
            'user_id': user_id,
            'q': question,
            'a': json.dumps(answer)
        })

        chat_id = cur.fetchone().get("chat_id")

    if chat_id is not None:
        return get_chat_log(user_id, chat_id)
    else:
        raise APIException("Failed to create new chat...")
