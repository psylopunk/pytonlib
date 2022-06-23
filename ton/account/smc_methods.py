from ..tl.functions import Smc_Load, Smc_RunGetMethod
from typing import Union

class SmcMethods:
    async def load_smc(self):
        self.smc_id = (await self.client.tonlib_wrapper.execute(
            Smc_Load(self.account_address)
        )).id

    async def run_get_method(self, method: Union[str, int], stack: list = []):
        if self.smc_id is None:
            await self.load_smc()

        return await self.client.tonlib_wrapper.execute(
            Smc_RunGetMethod(self.smc_id, method, stack)
        )