from ..tl.types import InputKeyRegular, WalletV3InitialAccountState, ActionMsg, \
    MsgMessage, MsgDataText, AccountAddress
from ..tl.functions import CreateQuery, QuerySend, ExportKey
from .account import Account
from ..errors import InvalidUsage
from typing import Union


class Wallet(Account):
    def __repr__(self): return f"Wallet<{self.account_address.account_address}>"

    async def send_messages(self, messages: list, allow_send_to_uninited=False, timeout: int=300):
        query = CreateQuery(
            InputKeyRegular(self.key, local_password=self.local_password),
            WalletV3InitialAccountState(self.key, self.client.config_info.default_wallet_id),
            self.account_address,
            ActionMsg(
                messages,
                allow_send_to_uninited=allow_send_to_uninited
            ),
            timeout=timeout
        )
        query_id = (await self.client.execute(query)).id
        result = await self.client.execute(QuerySend(query_id))
        return result

    async def transfer(self, destination: Union[str, list], amount: int=None, comment=None, send_mode: int=1, **kwargs):
        messages = []
        if type(destination) == str:
            assert type(amount) == int, 'amount type must be int if destination is str'
            messages.append(
                MsgMessage(
                    destination,
                    amount,
                    data=MsgDataText(comment or ''),
                    public_key=self.key.public_key,
                    send_mode=send_mode
                )
            )
        elif type(destination) == list:
            for output in destination:
                assert type(output) in [tuple, list], 'output must be tuple or list (address, amount, comment: optional)'
                messages.append(
                    MsgMessage(
                        output[0],
                        int(output[1]),
                        data=MsgDataText(
                            (output[2] if len(output) > 2 else '')
                                if comment is None else comment
                        ),
                        public_key=self.key.public_key,
                        send_mode=send_mode
                    )
                )
        else:
            raise InvalidUsage('destination must be str or list')

        return await self.send_messages(messages, **kwargs)

    @property
    def path(self):
        """
        :return: path (str)
        """
        return ''.join([self.key.public_key, self.key.secret])

    async def export(self):
        return ' '.join((await self.client.execute(
            ExportKey(
                InputKeyRegular(self.key, local_password=self.local_password)
            )
        )).word_list)