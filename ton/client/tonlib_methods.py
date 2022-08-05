from ..tonlibjson import TonLib, get_tonlib_path
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from logging import getLogger
import json
import asyncio
import requests
import platform
import pkg_resources

logger = getLogger('ton')

class TonlibMethods:
    @classmethod
    def enable_unaudited_binaries(cls):
        """
        Use this flag to enable unaudited libtonlibjson binaries.
        """
        cls._use_unaudited_binaries = True

    @property
    def local_config(self):
        local = deepcopy(self.config)
        local['liteservers'] = [local['liteservers'][self.ls_index]]
        return local

    async def execute(self, query, timeout=30):
        """
        Direct request to liteserver

        :param query: dict or TLObject
        :param timeout:
        :return: TLObject
        """
        result = await self.tonlib_wrapper.execute(query, timeout=timeout)
        if result.type == 'error':
            raise Exception(result.message)

        return result

    async def init_tonlib(self, cdll_path=None):
        if self.loop is None:
            self.loop = asyncio.get_event_loop()

        # Fetching actual network config from spec. url without cache
        if type(self.config) == str:
            if self.config.find('http://') == 0 or self.config.find('https://') == 0:
                self.config = requests.get(self.config).json()

        self.max_parallel_requests = self.config['liteservers'][0].get("max_parallel_requests", 50)

        if cdll_path is None:
            if self._use_unaudited_binaries is False:
                raise AttributeError(
                    "For really safe work with TON, you need to compile the TON executable files yourself (read more at https://github.com/psylopunk/ton/issues/7), "
                    "specifically libtonlibjson, with which pytonlib communicates with the network. "
                    "If the cdll_path parameter was not passed to the init_tanlib function, "
                    "it is proposed to use our collection of binaries from the community. "
                    "There is a small chance of dangerous code getting into them, so we recommend using them ONLY FOR LEARNING PURPOSES. "
                    "To use third-party binaries, please enable them by running "
                    "`TonlibClient.enable_unaudited_binaries()` and try again."
                )

            cdll_path = get_tonlib_path()

        wrapper = TonLib(self.loop, self.ls_index, cdll_path, self.verbosity_level)
        keystore_obj = {
            '@type': 'keyStoreTypeDirectory',
            'directory': self.keystore
        }
        # create keystore
        Path(self.keystore).mkdir(parents=True, exist_ok=True)

        request = {
            '@type': 'init',
            'options': {
                '@type': 'options',
                'config': {
                    '@type': 'config',
                    'config': json.dumps(self.local_config),
                    'use_callbacks_for_network': False,
                    'blockchain_name': '',
                    'ignore_cache': False
                },
                'keystore_type': keystore_obj
            }
        }
        self.tonlib_wrapper = wrapper

        # set confog
        r = await self.tonlib_wrapper.execute(request)
        self.config_info = r.config_info

        # set semaphore
        self.semaphore = asyncio.Semaphore(self.max_parallel_requests)

        logger.info(F"TonLib #{self.ls_index:03d} inited successfully")
        await self.set_verbosity_level(self.verbosity_level)

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