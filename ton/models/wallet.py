from ..tl.types import InputKeyRegular, WalletV3InitialAccountState, ActionMsg, \
    MsgMessage, MsgDataText
from ..tl.functions import CreateQuery, QuerySend, ExportKey
from .contract import Contract

class Wallet(Contract):
    def __repr__(self): return f"Wallet<{self.account_address.account_address}>"

    async def transfer(self, destination, amount, comment=None, allow_send_to_uninited=False, send_mode: int=1, timeout: int=300):
        query = CreateQuery(
            InputKeyRegular(self.key, local_password=self.local_password),
            WalletV3InitialAccountState(self.key, self.client.config_info.default_wallet_id),
            self.account_address,
            ActionMsg(
                [
                    MsgMessage(
                        destination,
                        amount,
                        data=MsgDataText(comment if not comment is None else ''),
                        public_key=self.key.public_key,
                        send_mode=send_mode
                    )
                ],
                allow_send_to_uninited=allow_send_to_uninited
            ),
            timeout=timeout
        )
        query_id = (await self.client.execute(query)).id
        result = await self.client.execute(QuerySend(query_id))
        return result

    @property
    def path(self):
        """
        :return: path (str)
        """
        return ''.join([self.key.public_key, self.key.secret])

    async def export(self):
        return await self.client.execute(
            ExportKey(
                InputKeyRegular(self.key, local_password=self.local_password)
            )
        )