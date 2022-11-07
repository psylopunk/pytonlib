import asyncio
import os
from typing import Union

from .converter_methods import ConverterMethods
from .function_methods import FunctionMethods
from .tonlib_methods import TonlibMethods
from .tonlib_methods import TonlibMethods
from .wallet_methods import WalletMethods
from ..account import Account
from ..tl.types import AccountAddress


class TonlibClient(TonlibMethods, WalletMethods, FunctionMethods, ConverterMethods):
    # Enable unaudited binaries (off by default)
    _use_unaudited_binaries = False

    def __init__(
            self,
            ls_index=0,
            config='https://ton.org/global-config.json',
            keystore=None,
            workchain_id=0,
            verbosity_level=0,
            default_timeout=10
    ):
        if keystore is None:  # while memory keystore libtonlibjson bug keep
            keystore = '.keystore'

        self.loop = None
        self.ls_index = ls_index
        self.config = config
        self.keystore = keystore
        self.workchain_id = workchain_id
        self.verbosity_level = verbosity_level
        self.default_timeout = default_timeout

        self.queue = []  # legacy
        self.lock = asyncio.Lock()
        self.locked = False

    async def find_account(self, account_address: Union[AccountAddress, str], preload_state: bool=True, **kwargs):
        """
        Getting an Account object by account address

        :param account_address:
        :return: Account
        """

        account = Account(account_address, client=self)
        if preload_state:
            await account.load_state(**kwargs)

        return account
