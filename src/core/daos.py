from core.models import SearchPromptHistory
import datetime
from core.views import any_view, user_view


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

def get_chat_log(chat_id) -> list[SearchPromptHistory]:
    #Let's define some mock data.
    #We will get the current time.

    chat_id = 1
    current_time = datetime.datetime.now()
    #A list of chat logs.
    chat_logs = {
        1: [
            {"type": "Text", "payload": "Hey there!"},
            {"type": "Text", "payload": "How can I help you?"}
        ],
        2: [
            {"type": "Text", "payload": "What time is it?"},
            {"type": "Text", "payload": current_time}
        ]
    }

    return {
        "user": "Y" if chat_id in chat_logs else "N",
        "data": chat_logs.get(chat_id, "That chat_id was not found")  # Ensure `data` is always a list
    }


    #Once we start actually putting data in our PostGreSQL database, SQL statements will be used instead

def save_question_answer_pair(question, answer): 
    pass