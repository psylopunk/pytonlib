from ..tl.types import WalletV3InitialAccountState, Key, ExportedKey, Raw_InitialAccountState, InputKeyRegular
from ..tl.functions import GetAccountAddress, ImportKey
from ..account import Account
from ..utils.wallet import contracts, sources, sha256
from nacl.signing import SigningKey
from base64 import b64decode


class WalletMethods:
    async def create_wallet(self, source='v3r2', workchain_id: int = 0, wallet_id: int = 0, local_password=None):
        """
        Generating a wallet using a key from self.create_new_key and TON default seed

        :param source: from sources list
        :param workchain_id:
        :param wallet_id:
        :param local_password:
        :return: Account
        """
        assert source in sources or source is None, 'Select one version'

        key = await self.create_new_key(local_password=local_password)
        return await self.init_wallet(key, source=source, workchain_id=workchain_id, wallet_id=wallet_id, local_password=local_password)

    async def init_wallet(self, key: Key, source='v3r2', workchain_id: int = None, wallet_id: int = None, local_password=None):
        assert source in sources or source is None, 'Select one version'

        workchain_id = workchain_id or self.workchain_id
        wallet_id = wallet_id or self.config_info.default_wallet_id

        query = GetAccountAddress(
            Raw_InitialAccountState(
                b64decode(sources[source]),
                contracts[sha256(sources[source])]['data_builder'](
                    wallet_id, SigningKey(
                        b64decode(await self.export_key(InputKeyRegular(key, local_password=local_password)))
                    ).verify_key._key
                ).serialize_boc()
            ),
            revision=0,
            workchain_id=workchain_id
        )
        r = await self.tonlib_wrapper.execute(query)
        return Account(
            r.account_address, key=key, local_password=local_password, client=self,
            source=source, workchain_id=workchain_id, wallet_id=wallet_id
        )

    async def find_wallet(self, path, local_password=None):
        """
        Getting a wallet from Keystore via Wallet.path

        :param path:
        :param local_password: local storage encrypt password
        :return: Wallet
        """

        # TODO: make pack wallet_id and other. Deprecate this method. Only v3 wallets support

        key = Key(path[:48], secret=path[48:] if path[48:] else None)
        query = GetAccountAddress(
            WalletV3InitialAccountState(key, int(self.config_info.default_wallet_id))
        )
        r = await self.tonlib_wrapper.execute(query)
        return Account(r.account_address, key=key, local_password=local_password, client=self)

    async def import_wallet(self, word_list, source='v3r2', workchain_id: int = None, wallet_id: int = None, local_password=None):
        """
        Restoring a wallet from a word list

        :param wallet_id:
        :param workchain_id:
        :param source:
        :param word_list:
        :param local_password:
        :return: Wallet
        """

        assert source in sources or source is None, 'Select one version'

        workchain_id = workchain_id or self.workchain_id
        wallet_id = wallet_id or self.config_info.default_wallet_id

        query = ImportKey(
            ExportedKey(word_list.split(' ')),
            '',
            local_password=local_password
        )
        key = await self.tonlib_wrapper.execute(query)
        key = Key(key.public_key, secret=key.secret)
        return await self.init_wallet(
            key, source=source, local_password=local_password,
            workchain_id=workchain_id, wallet_id=wallet_id
        )
