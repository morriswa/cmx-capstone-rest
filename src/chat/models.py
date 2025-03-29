
from typing import override

from app.validation import ValidatedDataModel


class ChatLog(ValidatedDataModel):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.chat_id = kwargs.get('chat_id')
        self.pair_id = kwargs.get('pair_id')
        self.prompt_text = kwargs.get('q')
        self.answer = kwargs.get('a')
        self.created = kwargs.get('created')


class ChatBlurb(ChatLog):
    @override
    def json(self):
        return {
            "chat_id": self.chat_id,
            "prompt_text": self.prompt_text,
            "created": self.created,
        }
