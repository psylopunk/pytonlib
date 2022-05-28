from ..tonlibjson import TonLib
import ujson as json
import asyncio
import requests

class TonlibMethods:
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

    async def init_tonlib(self, cdll_path=None):
        if type(self.config) == str:
            if self.config.find('http://') == 0 or self.config.find('https://') == 0:
                self.config = requests.get(self.config).json()

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