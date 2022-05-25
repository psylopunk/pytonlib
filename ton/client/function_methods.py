from ..tl.functions import CreateNewKey, SetLogVerbosityLevel
from ..tl.types import Key

class FunctionMethods:
    async def set_verbosity_level(self, level):
        return await self.tonlib_wrapper.execute(
            SetLogVerbosityLevel(level)
        )

    async def create_new_key(self, mnemonic_password='', random_extra_seed=None, local_password=None):
        """
        Generating a private key from random seeds

        :param mnemonic_password: str
        :param random_extra_seed:
        :param local_password: local storage encrypt password
        :return: Key, mnemonic
        """

        query = CreateNewKey(
            mnemonic_password,
            random_extra_seed=random_extra_seed,
            local_password=local_password
        )
        r = await self.tonlib_wrapper.execute(query)
        return Key(r.public_key, secret=r.secret)