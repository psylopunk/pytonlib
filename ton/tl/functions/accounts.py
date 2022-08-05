from ..base import TLObject
from ..types import AccountAddress, Internal_TransactionId
from ...utils import str_b64encode
from typing import Union


class GetAccountAddress(TLObject):
    def __init__(self, initial_account_state, revision: int=0, workchain_id: int=0):
        self.type = 'getAccountAddress'
        self.initial_account_state = initial_account_state
        self.revision = revision
        self.workchain_id = workchain_id


class GetAccountState(TLObject):
    def __init__(self, account_address: Union[AccountAddress, str]):
        if type(account_address) == str:
            account_address = AccountAddress(account_address)

        self.type = 'getAccountState'
        self.account_address = account_address


class Raw_GetAccountState(TLObject):
    def __init__(self, account_address: Union[AccountAddress, str]):
        if type(account_address) == str:
            account_address = AccountAddress(account_address)

        self.type = 'raw.getAccountState'
        self.account_address = account_address


class Raw_GetTransactions(TLObject):
    def __init__(self, account_address: Union[AccountAddress, str], from_transaction_id: Internal_TransactionId):
        self.type = 'raw.getTransactions'
        self.account_address = account_address
        self.from_transaction_id = from_transaction_id