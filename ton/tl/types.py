from .base import TLObject
from ..utils import str_b64encode
from typing import Union

class Key(TLObject):
    def __init__(self, public_key, secret=None):
        """

        :type public_key: str
        :param secret: str
        """
        self.type = 'key'
        self.public_key = public_key
        self.secret = secret

class InputKeyRegular(TLObject):
    def __init__(self, key: Key, local_password: str=None):
        self.type = 'inputKeyRegular'
        self.key = key
        self.local_password = str_b64encode(local_password)

class WalletV3InitialAccountState(TLObject):
    def __init__(self, public_key: Union[Key, str], wallet_id: int):
        if isinstance(public_key, Key):
            public_key = public_key.public_key

        self.type = 'wallet.v3.initialAccountState'
        self.public_key = public_key
        self.wallet_id = int(wallet_id)

class AccountAddress(TLObject):
    def __init__(self, account_address):
        self.type = 'accountAddress'
        self.account_address = account_address

# MSG
class MsgDataText(TLObject):
    def __init__(self, text: str):
        self.type = 'msg.dataText'
        self.text = str_b64encode(text)

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

# ACTIONS
class ActionMsg(TLObject):
    def __init__(
            self,
            messages: dict,
            allow_send_to_uninited: bool=False
    ):
        self.type = 'actionMsg'
        self.messages = messages
        self.allow_send_to_uninited = allow_send_to_uninited

class Internal_TransactionId(TLObject):
    def __init__(self, lt: Union[str, int], hash: Union[str]):
        self.type = 'internal.transactionId'
        self.lt = int(lt)
        self.hash = hash