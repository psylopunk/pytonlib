from ..base import TLObject
from ..types import InputKeyRegular, WalletV3InitialAccountState, AccountAddress, ActionMsg
from ...utils.base import str_b64encode
from typing import Union

class CreateQuery(TLObject):
    def __init__(
            self,
            private_key: InputKeyRegular,
            initial_account_state: WalletV3InitialAccountState,
            address: AccountAddress,
            action: Union[ActionMsg],
            timeout: int = 300
    ) -> object:
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