from ..base import TLObject
from ...utils.common import str_b64encode, bytes_b64encode
from .keys import *
from typing import Union

class Raw_InitialAccountState(TLObject):
    def __init__(self, code: bytes, data: bytes=None):
        self.type = 'raw.initialAccountState'
        self.code = bytes_b64encode(code)
        self.data = bytes_b64encode(data)


class WalletV3InitialAccountState(TLObject):
    def __init__(self, public_key: Union[Key, str], wallet_id: int):
        if isinstance(public_key, Key):
            public_key = public_key.public_key

        self.type = 'wallet.v3.initialAccountState'
        self.public_key = public_key
        self.wallet_id = int(wallet_id)


class Internal_TransactionId(TLObject):
    def __init__(self, lt: Union[str, int], hash: Union[str]):
        self.type = 'internal.transactionId'
        self.lt = int(lt)
        self.hash = hash
