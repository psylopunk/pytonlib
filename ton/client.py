from .utils import str_b64encode, raw_to_userfriendly
from .tl.types import Key, WalletV3InitialAccountState, AccountAddress
from .tl.functions import CreateNewKey, GetAccountAddress, GetAccountState
from .tonlibjson import TonLib
from .models import Wallet
from loguru import logger
from typing import Union
import ujson as json
import httpx

class TonlibClient:

    def __init__(
            self,
            loop,
            ls_index=0,
            config='https://newton-blockchain.github.io/global.config.json',
            keystore=None,
            workchain_id=0
    ):
        self.loop = loop
        self.ls_index = ls_index
        self.config = config
        self.keystore = keystore
        self.workchain_id = workchain_id

    async def init_tonlib(self, cdll_path=None):
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
        await self.set_verbosity_level(0)
        self.config_info = r.config_info

    async def set_verbosity_level(self, level):
        request = {
            '@type': 'setLogVerbosityLevel',
            'new_verbosity_level': level
        }
        return await self.tonlib_wrapper.execute(request)

    async def execute(self, query, timeout=30):
        return await self.tonlib_wrapper.execute(query, timeout=timeout)

    async def create_new_key(self, mnemonic, random_extra_seed=None, local_password=None):
        query = CreateNewKey(
            mnemonic,
            random_extra_seed=random_extra_seed,
            local_password=local_password
        )

        r = await self.tonlib_wrapper.execute(query)
        return Key(r.public_key, secret=r.secret)

    async def init_wallet(self, key: Key, revision: int=0, workchain_id: int=None):
        if workchain_id is None:
            workchain_id = self.workchain_id

        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id)),
            revision=revision,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, client=self)

    async def wallet_from_exported_key(self, exported_key: str, revision: int=0, workchain_id: int=None):
        if workchain_id is None:
            workchain_id = self.workchain_id

        data = json.loads(exported_key)
        key = Key(
            data['public_key'],
            secret=data.get('secret')
        )
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id)),
            revision=revision,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, client=self)

    async def get_wallet(self, account_address: Union[AccountAddress, str]):
        return Wallet(account_address, client=self)

    async def reconnect(self):
        if not self.tonlib_wrapper.shutdown_state:
            logger.info(f'Client #{self.number:03d} reconnecting')
            self.tonlib_wrapper.shutdown_state = "started"
            await self.init_tonlib()
            logger.info(f'Client #{self.number:03d} reconnected')