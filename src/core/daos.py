from core.models import SearchPromptHistory
import datetime



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
    current_time = datetime.datetime.now()
    #A list of chat logs.
    chat_logs = {
        1: [
            {"type": "Text", "payload": "Hey there!"},
            {"type": "Text", "payload": "How can I help you?"}
        ],
        2: [
            {"type": "Image", "payload": "What time is it?"},
            {"type": "Text", "payload": current_time}
        ]
    }

    #Now, let's check if the chat_id exists.
    if(chat_id in chat_logs):
        response = {
            "user": "Y",
            "data": chat_logs[chat_id]
        }
    else:
        response = {
            "user": "N",
            "data": []
        }

    return response
