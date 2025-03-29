import datetime
import json

from app.exceptions import APIException, BadRequestException
from app import database

from chat.models import ChatLog, ChatBlurb


def get_search_history(user_id) -> list[ChatBlurb]:
    with database.cursor() as cur:
        """
            This function will get the search history of the user.
            It will return a list of prompts that the user has made.
            This function will get the data from the database. KR

            :author: William Morris
        """
        cur.execute("""
            select distinct on (chat_id)
                chat_id, q, created
            from chat_history
            where user_id = %(user_id)s
            order by chat_id, created desc
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
        if rows is None or len(rows) == 0:
            raise BadRequestException(f"No chats found with ID {chat_id}")

        return [ChatLog(**row) for row in rows]


def create_chat(user_id, question, answer):
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


def continue_chat(user_id, chat_id, question, answer):
    """
                :author: William Morris

    """
    with database.cursor() as cur:
        cur.execute("""
            select * from chat_history
            where user_id = %(user_id)s
            and   chat_id = %(chat_id)s
            order by created desc limit 1;
        """, {'user_id': user_id, 'chat_id': chat_id})

        row = cur.fetchone()
        if row is None:
            raise BadRequestException(f"Chat {chat_id} not found")

        created = row['created']
        if created < datetime.datetime.now() - datetime.timedelta(hours=1):
            raise BadRequestException(f"Chat {chat_id} expired")

        cur.execute("""
            INSERT INTO chat_history
                (user_id, chat_id, q, a)
            VALUES
                (%(user_id)s, %(chat_id)s, %(q)s, %(a)s)
            returning chat_id;
        """,{
            'user_id': user_id,
            'chat_id': chat_id,
            'q': question,
            'a': json.dumps(answer)
        })

    return get_chat_log(user_id, chat_id)
