from .state_methods import StateMethods
from .wallet_methods import WalletMethods
from .smc_methods import SmcMethods
from ..tl.types import AccountAddress
from ..errors import InvalidUsage

class Account(StateMethods, WalletMethods, SmcMethods):
    def __repr__(self): return f"Account<{self.account_address.account_address}>"

    def __init__(self, address, key=None, local_password=None, client=None):
        if isinstance(address, AccountAddress):
            self.account_address = self.account_address
        elif isinstance(address, str):
            self.account_address = AccountAddress(address)
        else:
            raise InvalidUsage('Specify the account address')

        self.key = key
        self.local_password = local_password
        self.client = client

        self.state = None
        self.smc_id = None