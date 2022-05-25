from ..tl.types import WalletV3InitialAccountState, Key, ExportedKey
from ..tl.functions import GetAccountAddress, ImportKey
from ..models import Wallet

class WalletMethods:
    async def create_wallet(self, revision=0, workchain_id: int=None, local_password=None):
        """
        Generating a wallet using a key from self.create_new_key and TON default seed

        :param revision: int
        :param workchain_id: int
        :param local_password: local storage encrypt password
        :return: Wallet
        """

        key = await self.create_new_key(local_password=local_password)
        return await self.init_wallet(key, revision=revision, workchain_id=workchain_id, local_password=local_password)

    async def init_wallet(self, key: Key, local_password=None, revision: int=0, workchain_id: int=None, wallet_id=None):
        workchain_id = workchain_id or self.workchain_id
        wallet_id = wallet_id or self.config_info.default_wallet_id
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(wallet_id)),
            revision=revision,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, local_password=local_password, client=self)

    async def find_wallet(self, path, local_password=None):
        """
        Getting a wallet from Keystore via Wallet.path

        :param path:
        :param local_password: local storage encrypt password
        :return: Wallet
        """

        key = Key(path[:48], secret=path[48:] if path[48:] else None)
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id))
        )
        r = await self.tonlib_wrapper.execute(query)
        return Wallet(r.account_address, key=key, local_password=local_password, client=self)

    async def import_wallet(self, word_list, local_password=''):
        """
        Restoring a wallet from a word list

        :param word_list:
        :param local_password:
        :return: Wallet
        """

        query = ImportKey(
            ExportedKey(word_list.split(' ')),
            '',
            local_password=local_password
        )
        key = await self.tonlib_wrapper.execute(query)
        key = Key(key.public_key, secret=key.secret)
        return await self.init_wallet(key, local_password=local_password)