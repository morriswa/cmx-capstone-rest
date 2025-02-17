from app.validation import ValidatedDataModel,is_blank #Super class for all data models in the app

class SearchPromptHistory(ValidatedDataModel):
    def __init__(self, **kwargs):
        self.chat_id = kwargs.get('chat_id')
        self.prompt_text = kwargs.get('prompt_text')
        self.date_created=kwargs.get('date_created')
        self.result_id=kwargs.get('result_id')
        self.title=kwargs.get('title')
        self.url=kwargs.get('url')
        self.summary=kwargs.get('summary')
        self.description=kwargs.get('description')
        self.source=kwargs.get('source')

