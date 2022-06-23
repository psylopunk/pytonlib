from ..base import TLObject

class ActionMsg(TLObject):
    def __init__(
            self,
            messages: dict,
            allow_send_to_uninited: bool=False
    ):
        self.type = 'actionMsg'
        self.messages = messages
        self.allow_send_to_uninited = allow_send_to_uninited