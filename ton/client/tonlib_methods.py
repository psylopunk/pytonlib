from ..tonlibjson import TonLib
import ujson as json
import asyncio
import requests
import platform
import pkg_resources

def get_tonlib_path():
    arch_name = platform.system().lower()
    machine = platform.machine().lower()
    if arch_name == 'linux':
        lib_name = f'libtonlibjson.{machine}.so'
    elif arch_name == 'darwin':
        lib_name = f'libtonlibjson.{machine}.dylib'
    elif arch_name == 'windows':
        lib_name = f'tonlibjson.{machine}.dll'
    else:
        raise RuntimeError(f"Platform '{arch_name}({machine})' is not compatible yet. Read more at https://github.com/psylopunk/ton/issues/7")

    return pkg_resources.resource_filename('ton', f'distlib/{arch_name}/{lib_name}')

class TonlibMethods:
    @classmethod
    def enable_unaudited_binaries(cls):
        """
        Use this flag to enable unaudited libtonlibjson binaries.
        """
        cls._use_unaudited_binaries = True

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
        if self.loop is None:
            self.loop = asyncio.get_event_loop()

        # Fetching actual network config from spec. url without cache
        if type(self.config) == str:
            if self.config.find('http://') == 0 or self.config.find('https://') == 0:
                self.config = requests.get(self.config).json()

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

        self.tonlib_wrapper = TonLib(self.loop, self.ls_index, cdll_path=cdll_path)
        await self.set_verbosity_level(self.verbosity_level)
        
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

        r = await self.tonlib_wrapper.execute(request)
        self.tonlib_wrapper.set_restart_hook(hook=self.reconnect, max_requests=500)
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