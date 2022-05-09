from .tl.types import Key, WalletV3InitialAccountState, AccountAddress, ExportedKey
from .tl.functions import CreateNewKey, GetAccountAddress, ImportKey
from .tonlibjson import TonLib
from .models import Wallet, Contract
from typing import Union
from .utils.mnemonic import generate
import asyncio
import ujson as json
import httpx
import sys, os

class TonlibClient:
    def __init__(
            self,
            ls_index=0,
            config='https://newton-blockchain.github.io/global.config.json',
            keystore=None,
            workchain_id=0,
            verbosity_level=0
    ):
        if keystore is None: # while memory keystore libtonlibjson bug keep
            if '.keystore' not in os.listdir(path='.'): os.system('mkdir .keystore')
            keystore = '.keystore'

        self.loop = asyncio.get_event_loop()
        self.ls_index = ls_index
        self.config = config
        self.keystore = keystore
        self.workchain_id = workchain_id
        self.verbosity_level = 0

        self.queue = []
        self.lock = asyncio.Lock()
        self.locked = False

    async def init_tonlib(self, cdll_path=None):
        if type(self.config) == str:
            if self.config.find('http://') == 0 or self.config.find('https://') == 0:
                self.config = httpx.get(self.config).json()

        wrapper = TonLib(self.loop, self.ls_index, cdll_path=cdll_path)
        if self.keystore:
            keystore_obj = {
                '@type': 'keyStoreTypeDirectory',
                'directory': self.keystore
            }
        else:
            keystore_obj = {
                '@type': 'keyStoreTypeInMemory'
            }

        self.config['liteservers'] = [
            self.config['liteservers'][self.ls_index]
        ]
        request = {
            '@type': 'init',
            'options': {
                '@type': 'options',
                'config': {
                    '@type': 'config',
                    'config': json.dumps(self.config),
                    'use_callbacks_for_network': False,
                    'blockchain_name': '',
                    'ignore_cache': False
                },
                'keystore_type': keystore_obj
            }
        }

        r = await wrapper.execute(request)
        wrapper.set_restart_hook(hook=self.reconnect, max_requests=500)
        self.tonlib_wrapper = wrapper
        await self.set_verbosity_level(self.verbosity_level)
        self.config_info = r.config_info

    async def set_verbosity_level(self, level):
        request = {
            '@type': 'setLogVerbosityLevel',
            'new_verbosity_level': level
        }
        return await self.tonlib_wrapper.execute(request)

    async def _execute(self, query, timeout=30):
        if self.locked: return None
        self.locked = True
        self.lock.release()

        result = await self.tonlib_wrapper.execute(query, timeout=timeout)
        async with self.lock:
            self.locked = False

        return result

    async def execute(self, query, timeout=30):
        """
        Direct request to liteserver

        :param query: dict or TLObject
        :param timeout:
        :return: TLObject
        """

        while True:
            if self.locked:
                await asyncio.sleep(0.3)
            else:
                if self.lock.locked():
                    self.lock.release()

                break

        await self.lock.acquire()
        result = await self._execute(query, timeout=timeout)
        if result.type == 'error':
            raise Exception(result.message)

        return result

    async def create_new_key(self, random_extra_seed=None, local_password=None):
        """
        Generating a private key from random seeds

        :param random_extra_seed:
        :param local_password: local storage encrypt password
        :return: Key, mnemonic
        """
        mnemonic = generate()
        query = CreateNewKey(
            mnemonic.split(' '),
            random_extra_seed=random_extra_seed,
            local_password=local_password
        )

        r = await self.tonlib_wrapper.execute(query)
        return Key(r.public_key, secret=r.secret), mnemonic

    async def create_wallet(self, revision=0, workchain_id: int=None, **kwargs):
        """
        Generating a wallet using a key from self.create_new_key

        :param revision:
        :param workchain_id:
        :param local_password: local storage encrypt password
        :param random_extra_seed:
        :return:
        """

        key, mnemonic = await self.create_new_key(**kwargs)
        return (
            await self.init_wallet(key, revision=revision, workchain_id=workchain_id, **kwargs),
            mnemonic
        )

    async def init_wallet(self, key: Key, local_password=None, revision: int=0, workchain_id: int=None):
        workchain_id = workchain_id or self.workchain_id
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id)),
            revision=revision,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, local_password=local_password, client=self)

    async def find_wallet(self, path, local_password=None, revision: int=0, workchain_id: int=None):
        """
        Getting a wallet from Keystore via Wallet.path

        :param path:
        :param local_password: local storage encrypt password
        :param revision:
        :param workchain_id:
        :return: Wallet
        """

        workchain_id = workchain_id or self.workchain_id
        key = Key(path[:48], secret=path[48:])
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id)),
            revision=revision,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, local_password=local_password, client=self)

    async def find_address(self, account_address: Union[AccountAddress, str]):
        """
        Getting a wallet from Keystore via Wallet.path

        :param account_address:
        :return: Contract
        """

        return Contract(account_address, client=self)

    async def import_wallet(self, word_list, mnemonic_password, local_password=None):
        """
        Restoring a wallet from a pair word list seed & mnemonic password

        :param word_list:
        :param mnemonic_password:
        :param local_password:
        :return: Wallet
        """

        query = ImportKey(
            ExportedKey(word_list),
            mnemonic_password,
            local_password=local_password
        )
        key = await self.tonlib_wrapper.execute(query)
        return await self.init_wallet(key, local_password=local_password)

    async def reconnect(self):
        """
        Restart libtonlibjson.so in case of failure

        :return: None
        """

        if not self.tonlib_wrapper.shutdown_state:
            logger = self.tonlib_wrapper.logger
            logger.info(f'Client #{self.ls_index:03d} reconnecting')
            self.tonlib_wrapper.shutdown_state = "started"
            await self.init_tonlib()
            logger.info(f'Client #{self.ls_index:03d} reconnected')

    # TODO: remove in next version
    async def wallet_from_exported_key(self, exported_key: str, revision: int=0, workchain_id: int=None):
        raise Exception('TonlibClient.wallet_from_exported_key is deprecated, try Tonlibclient.find_wallet')