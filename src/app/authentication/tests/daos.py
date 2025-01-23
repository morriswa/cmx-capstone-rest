

from django.conf import settings

from django.test import TestCase
from unittest import mock

from psycopg2.extras import RealDictCursor

from app.authentication.daos import *
from app import database
from app.exceptions import APIException



class RegisterUserDAOTests(TestCase):
    def test_successfully_register_user(self):
        test_email = 'test@morriswa.org'
        new_user_id = register_user(test_email)

        with database.cursor() as cur:
            cur.execute("""select user_id from auth_integration where email = 'test@morriswa.org'""")
            res = cur.fetchone()
            self.assertIsNotNone(res, 'should retrieve new user row from db')
            self.assertEqual(new_user_id, res['user_id'])

    @mock.patch('app.database.cursor')
    def test_unsuccessfully_register_user(self, mock_cur):
        class __MockCursor:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def execute(*args):
                pass

            def fetchone(*args):
                return None

        mock_cur.return_value = __MockCursor()

        test_email = 'test@morriswa.org'
        try:
            new_user_id = register_user(test_email)
        except Exception as e:
            self.assertTrue(isinstance(e, APIException), 'ensure correct error is thrown')
            self.assertEqual(
                e.error,
                f'failed to register user with email {test_email}',
                'ensure correct error is thrown'
            )

class GetUserInfoDAOTests(TestCase):

    def __setup_get_user(self):
        user_id = uuid.uuid4()
        test_email = 'test@morriswa.org'
        with database.cursor() as cur:
            cur.execute("""
                insert into auth_integration (user_id, email)
                values (%(user_id)s, %(email)s)
            """, {'user_id': user_id, 'email': test_email})

        return user_id, test_email

    def test_get_user(self):

        user_id, test_email = self.__setup_get_user()

        created_user_id = get_user_info(test_email)

        self.assertIsNotNone(created_user_id, 'should get response')
        self.assertEqual(created_user_id, user_id, 'user_id should be returned')

    def __setup_get_user_vendor(self):
        user_id = uuid.uuid4()
        test_email = 'test@morriswa.org'
        with database.cursor() as cur:
            cur.execute("""
                insert into auth_integration (user_id, email)
                values
                    (%(user_id)s, %(email)s);
            """, {'user_id': user_id, 'email': test_email})

            res = cur.fetchone()
            return user_id, test_email

    def test_get_and_register_user(self):

        test_email = 'test@morriswa.org'
        res = get_user_info(test_email)

        self.assertIsNotNone(res, 'user_id should be returned')

        with database.cursor() as cur:
            cur.execute("""
                select * from auth_integration
                where user_id = %(user_id)s
            """, {'user_id': res})
            row = cur.fetchone()

            self.assertIsNotNone(row, 'row should be created')
            self.assertEqual(test_email, row['email'], 'email should be correct')
