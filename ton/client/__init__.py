from .tonlib_methods import TonlibMethods
from .wallet_methods import WalletMethods
from .function_methods import FunctionMethods
from .tonlib_methods import TonlibMethods
from .converter_methods import ConverterMethods
from ..tl.types import AccountAddress
from ..account import Account
from typing import Union
import asyncio
import sys, os


class TonlibClient(TonlibMethods, WalletMethods, FunctionMethods, ConverterMethods):
    # Enable unaudited binaries (off by default)
    _use_unaudited_binaries = False

    def __init__(
            self,
            ls_index=0,
            config='https://ton.org/global-config.json',
            keystore=None,
            workchain_id=0,
            verbosity_level=0
    ):
        if keystore is None: # while memory keystore libtonlibjson bug keep
            if '.keystore' not in os.listdir(path='.'): os.system('mkdir .keystore')
            keystore = '.keystore'

        self.loop = None
        self.ls_index = ls_index
        self.config = config
        self.keystore = keystore
        self.workchain_id = workchain_id
        self.verbosity_level = verbosity_level

        self.queue = []
        self.lock = asyncio.Lock()
        self.locked = False

    async def find_account(self, account_address: Union[AccountAddress, str], preload_state: bool=True):
        """
        Getting a Account object by account address

        :param account_address:
        :return: Account
        """

        account = Account(account_address, client=self)
        if preload_state: await account.load_state()
        return account

    # TODO: remove in next version
    async def wallet_from_exported_key(self, exported_key: str, revision: int=0, workchain_id: int=None):
        raise Exception('TonlibClient.wallet_from_exported_key is deprecated, try Tonlibclient.find_wallet instead')