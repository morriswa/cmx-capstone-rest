from core.models import SearchPromptHistory
import datetime
from core.views import any_view, user_view
from app import database
import json


#This function will get the search history of the user. KR
#It will return a list of prompts that the user has made. KR
#This function will later be updated with SQL statements to get the data from the database. KR
def get_search_history(user_id) -> list[SearchPromptHistory]:

    return [
        SearchPromptHistory(
            chat_id=1,
            prompt_text="hello",
            date_created="2024-02-01"
        ),

        SearchPromptHistory(
            chat_id=2,
            prompt_text="What's up",
            date_created="2024-02-03"
        ),

        SearchPromptHistory(
            chat_id=3,
            prompt_text="Hola",
            date_created="2024-02-04"
        )
    ]
#This function will post a search prompt to the database. KR
#It will return the prompt that was posted. KR
#This function will later be updated with SQL statements to post the data to the database. KR
def post_search(user_id, prompt_text) -> list[SearchPromptHistory]:
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return SearchPromptHistory(
        chat_id=4,
        prompt_text=prompt_text,
        date_created=current_date
    )
def get_chat_log(user_id, chat_id):
    with database.cursor() as cur: 
        cur.execute("""
                     SELECT * FROM chat_history WHERE chat_id = %(chat_id)s
                    and user_id = %(user_id)s; 
        
        """, {'chat_id': chat_id,
              'user_id':user_id})
        rows = cur.fetchall()
        return rows
 

def save_question_answer_pair(user_id,question, answer): 
    with database.cursor() as cur: 
        cur.execute("""
            INSERT INTO chat_history (chat_id, user_id, created, last_updated, q, a)
            VALUES
               (DEFAULT,%(user_id)s,
                DEFAULT, DEFAULT, %(q)s, %(a)s) returning chat_id;
    """,{'user_id': user_id,
         'q': question, 
         'a': json.dumps(answer)
         }
        )
        chat_id = cur.fetchone().get("chat_id")
    
        cur.execute("""
            SELECT * FROM chat_history WHERE chat_id = %(chat_id)s
                    and user_id = %(user_id)s; 
        
        """, {'chat_id': chat_id,
              'user_id': user_id})
        rows = cur.fetchall()
        return rows
    
        
