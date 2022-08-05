from ..tl.functions import Smc_Load, Smc_RunGetMethod, Raw_CreateAndSendMessage
from typing import Union


class SmcMethods:
    async def load_smc(self):
        self.smc_id = (await self.client.tonlib_wrapper.execute(
            Smc_Load(self.account_address)
        )).id

    async def run_get_method(self, method: Union[str, int], stack: list = [], force=False):
        if self.smc_id is None or force is True:
            await self.load_smc()

        return await self.client.tonlib_wrapper.execute(
            Smc_RunGetMethod(self.smc_id, method, stack)
        )

    async def send_message(self, body: bytes):
        return await self.client.tonlib_wrapper.execute(
            Raw_CreateAndSendMessage(self.account_address, body)
        )