from typing import override

from app.validation import ValidatedDataModel,is_blank #Super class for all data models in the app

#This is the class that when instantiated will be used for each user. KR
#Each user will have a chat_id, prompt_text, and date_created for each session. KT

class ChatLog(ValidatedDataModel):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.chat_id = kwargs.get('chat_id')
        self.prompt_text = kwargs.get('q')
        self.answer = kwargs.get('a')
        self.created = kwargs.get('created')
        self.last_updated = kwargs.get('last_updated')


class ChatBlurb(ChatLog):
    @override
    def json(self):
        return {
            "chat_id": self.chat_id,
            "prompt_text": self.prompt_text,
            "created": self.created,
        }
