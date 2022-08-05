from ..base import TLObject
from ...utils.common import str_b64encode, bytes_b64encode
from typing import Union
from .accounts import *

class MsgDataText(TLObject):
    def __init__(self, text: str):
        self.type = 'msg.dataText'
        self.text = str_b64encode(text)

class MsgDataRaw(TLObject):
    def __init__(self, body: bytes, init_state: bytes=None):
        self.type = 'msg.dataRaw'
        self.body = bytes_b64encode(body)
        self.init_state = bytes_b64encode(init_state)

class MsgMessage(TLObject):
    def __init__(
            self,
            destination: Union[AccountAddress, str],
            amount: int,
            data: Union[MsgDataText]=None,
            public_key: str=None,
            send_mode: int=0
    ):
        if type(destination) == str:
            destination = AccountAddress(destination)

        self.type = 'msg.message'
        self.destination = destination
        self.amount = amount
        self.data = data
        self.public_key = public_key
        self.send_mode = send_mode