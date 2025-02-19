from app.validation import ValidatedDataModel,is_blank #Super class for all data models in the app

class SearchPromptHistory(ValidatedDataModel):
    def __init__(self, **kwargs):
        self.chat_id = kwargs.get('chat_id')
        self.prompt_text = kwargs.get('prompt_text')
        self.date_created=kwargs.get('date_created')
        

