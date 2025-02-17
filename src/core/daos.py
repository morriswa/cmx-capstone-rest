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

def get_search_result(prompt_text) -> list[SearchPromptHistory]:

     return [
        SearchPromptHistory(
            result_id=1,
            title="The University of Kansas",
            url="https://ku.edu/",
            summary="The University of Kansas harnesses the talent, ingenuity, and determination of Jayhawks. We inspire our community, bolster Kansas, and better the world through each creation and discovery.",
            description="This is mock description",
            source="The University of Kansas Homepage"
        ),

        SearchPromptHistory(
            result_id=2,
            title="The University of Kansas Admissions",
            url="https://admissions.ku.edu/",
            summary="The University of Kansas is the state’s flagship university and one of just 65 invited members of the prestigious Association of American Universities (AAU). We consistently earn high rankings for academics and recognition as a premier research university.",
            description="This is mock description",
            source="The University of Kansas Admissions Homepage"
        ),

        SearchPromptHistory(
            result_id=3,
            title="The University of Kansas Financial Aid",
            url="https://financialaid.ku.edu/",
            summary="The University of Kansas is the state’s flagship university and one of just 65 invited members of the prestigious Association of American Universities (AAU). We consistently earn high rankings for academics and recognition as a premier research university.",
            description="This is mock description",
            source="The University of Kansas Financial Aid Homepage"
        )
    ]
