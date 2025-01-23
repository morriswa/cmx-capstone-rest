"""
    provides core authentication utils
    author: William Morris [morriswa]
"""

import logging
import uuid
from typing import Optional


import app.database
from app.exceptions import APIException



def register_user(email:str):
    with app.database.cursor() as cursor:
        cursor.execute(
            "insert into auth_integration (email) values (%(email)s) returning user_id;",
            {'email': email}
        )
        result = cursor.fetchone()
        if result is None:
            msg = f'failed to register user with email {email}'
            logging.error(msg)
            raise APIException(msg)

        user_id = result.get('user_id')
        logging.info(f'successfully registered user {user_id} with email {email}')
        return user_id

def get_user_info(email: str):
    user_id = None
    with app.database.cursor() as cursor:
        cursor.execute(
            "select user_id from auth_integration where email = %(email)s",
            {'email': email}
        )
        result = cursor.fetchone()
        if result is None:
            logging.info(f'did not find database entry for user with email {email}, attemping registration')
            user_id = register_user(email)
        else:
            user_id = result['user_id']

    return user_id
