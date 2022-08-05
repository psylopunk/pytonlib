from ..tl.functions import CreateNewKey, SetLogVerbosityLevel, ExportUnencryptedKey, Raw_SendMessage
from ..tl.types import Key, InputKeyRegular


class FunctionMethods:
    async def set_verbosity_level(self, level):
        return await self.tonlib_wrapper.execute(
            SetLogVerbosityLevel(level)
        )


    async def send_boc(self, message: bytes):
        """
        Sending a message to the network

        :param message: bytes
        :return:
        """

        query = Raw_SendMessage(message)
        return await self.tonlib_wrapper.execute(query)


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

    async def export_key(self, input_key: InputKeyRegular):
        """
        Exporting a signing private key

        :param input_key:
        :return: base64 str
        """

        query = ExportUnencryptedKey(input_key)
        r = await self.tonlib_wrapper.execute(query)
        return r.data