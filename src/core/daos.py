from core.models import SearchPromptHistory


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
            chat_id=1,
            prompt_text="Hola",
            date_created="2024-02-04"
        )
    ]
