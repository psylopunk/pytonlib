from typing import Union

from ..tl.functions import Smc_Load, Smc_RunGetMethod, Raw_CreateAndSendMessage


class SmcMethods:
    async def load_smc(self, **kwargs):
        self.smc_id = (await self.client.tonlib_wrapper.execute(
            Smc_Load(self.account_address), **kwargs
        )).id

    async def run_get_method(self, method: Union[str, int], stack: list = [], force=False, **kwargs):
        if self.smc_id is None or force is True:
            await self.load_smc(**kwargs)

        return await self.client.tonlib_wrapper.execute(
            Smc_RunGetMethod(self.smc_id, method, stack), **kwargs
        )

    async def send_message(self, body: bytes, **kwargs):
        return await self.client.tonlib_wrapper.execute(
            Raw_CreateAndSendMessage(self.account_address, body), **kwargs
        )
