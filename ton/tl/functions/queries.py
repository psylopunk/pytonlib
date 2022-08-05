from ..base import TLObject
from ..types import InputKeyRegular, Raw_InitialAccountState, AccountAddress, ActionMsg
from ...utils.common import str_b64encode, bytes_b64encode
from typing import Union


class Raw_CreateQuery(TLObject):
    def __init__(
            self,
            destination: Union[AccountAddress, str],
            body: bytes,
            init_code: bytes = None,
            init_data: bytes = None
    ):
        if type(destination) == str:
            destination = AccountAddress(destination)

        self.type = 'raw.createQuery'
        self.destination = destination
        self.body = bytes_b64encode(body)
        if init_code: self.init_code = bytes_b64encode(init_code)
        if init_data: self.init_data = bytes_b64encode(init_data)


class Raw_CreateAndSendMessage(TLObject):
    def __init__(self, destination: Union[AccountAddress, str], data: bytes, initial_account_state: bytes = None):
        if type(destination) == str:
            destination = AccountAddress(destination)

        self.type = 'raw.createAndSendMessage'
        self.destination = destination
        self.data = bytes_b64encode(data)
        if initial_account_state:
            self.initial_account_state = bytes_b64encode(initial_account_state)

class Raw_SendMessage(TLObject):
    def __init__(self, body: bytes):
        self.type = 'raw.sendMessage'
        self.body = bytes_b64encode(body)


class CreateQuery(TLObject):
    def __init__(
            self,
            private_key: InputKeyRegular,
            initial_account_state: Raw_InitialAccountState,
            address: AccountAddress,
            action: Union[ActionMsg],
            timeout: int = 300
    ):
        self.type = 'createQuery'
        self.private_key = private_key
        self.initial_account_state = initial_account_state
        self.address = address
        self.action = action
        self.timeout = timeout


class Query_Send(TLObject):
    def __init__(self, id: int):
        self.type = 'query.send'
        self.id = id


class Query_Forget(TLObject):
    def __init__(self, id: int):
        self.type = 'query.forget'
        self.id = id


class Query_EstimateFees(TLObject):
    def __init__(self, id: int, ignore_chksig: bool = False):
        self.type = 'query.estimateFees'
        self.id = id
        self.ignore_chksig = ignore_chksig


class Query_GetInfo(TLObject):
    def __init__(self, id: int):
        self.type = 'query.getInfo'
        self.id = id