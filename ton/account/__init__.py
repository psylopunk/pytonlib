from .state_methods import StateMethods
from .wallet_methods import WalletMethods
from .smc_methods import SmcMethods
from .nft_methods import NFTMethods
from ..tl.types import AccountAddress, Raw_InitialAccountState
from ..tl.functions import GetAccountAddress
from ..errors import InvalidUsage


class Account(StateMethods, WalletMethods, SmcMethods, NFTMethods):
    def __repr__(self):
        return f"Account<{self.account_address.account_address}>"

    def __init__(self, address, **kwargs):
        if isinstance(address, AccountAddress):
            self.account_address = self.account_address
        elif isinstance(address, str):
            self.account_address = AccountAddress(address)
        else:
            raise InvalidUsage('Specify the account address')

        self.__dict__.update(kwargs)

        self.state = None
        self.smc_id = None

    @property
    def address(self):
        return self.account_address.account_address

    @classmethod
    async def from_state(cls, client, state: Raw_InitialAccountState, workchain_id=0):
        account_address = await client.execute(GetAccountAddress(state, workchain_id=workchain_id))
        return cls(account_address.account_address, state=state, workchain_id=workchain_id)
