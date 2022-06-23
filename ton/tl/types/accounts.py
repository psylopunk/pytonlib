from ..base import TLObject

class AccountAddress(TLObject):
    def __init__(self, account_address):
        self.type = 'accountAddress'
        self.account_address = account_address