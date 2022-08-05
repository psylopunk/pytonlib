from ..tl.functions import CreateQuery, Query_Send, ExportKey
from ..tl.types import InputKeyRegular, Raw_InitialAccountState, ActionMsg, MsgMessage, MsgDataRaw, MsgDataText
from ..errors import InvalidUsage
from ..utils.wallet import sources, contracts, sha256
from nacl.signing import SigningKey
from base64 import b64decode
from typing import Union

class WalletMethods:
    async def build_state(self):
        state = await self.get_state()
        if state.code:
            return {'code': b64decode(state.code), 'data': b64decode(state.data) if state.data else state.data}

        assert 'source' in self.__dict__, 'source must be specified'
        assert 'wallet_id' in self.__dict__, 'wallet_id must be specified'
        assert 'key' in self.__dict__, 'key must be specified'
        return {
            'code': b64decode(sources[self.source]),
            'data': contracts[sha256(sources[self.source])]['data_builder'](
                self.wallet_id, SigningKey(
                    b64decode(
                        await self.client.export_key(
                            InputKeyRegular(self.key, local_password=self.__dict__.get('local_password'))
                        )
                    )
                ).verify_key._key
            ).serialize_boc()
        }


    async def send_messages(self, messages: list, allow_send_to_uninited=False, timeout: int = 300):
        state = await self.build_state()
        query = CreateQuery(
            InputKeyRegular(self.key, local_password=self.local_password),
            Raw_InitialAccountState(state['code'], state['data']),
            self.account_address,
            ActionMsg(
                messages,
                allow_send_to_uninited=allow_send_to_uninited
            ),
            timeout=timeout
        )
        query_id = (await self.client.execute(query)).id
        result = await self.client.execute(Query_Send(query_id))
        return result


    async def transfer(self, destination: Union[str, list], amount: int = None, data: bytes = None, comment=None, send_mode: int = 1, **kwargs):
        messages = []
        if type(destination) == str:
            assert type(amount) == int, 'amount type must be int if destination is str'
            messages.append(
                MsgMessage(
                    destination,
                    amount,
                    data=MsgDataRaw(data) if not (data is None) else MsgDataText(comment or ''),
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
                        data=(MsgDataRaw(data) if not (data is None) else MsgDataText(
                            (output[2] if len(output) > 2 else '') if comment is None else comment
                        )),
                        public_key=self.key.public_key,
                        send_mode=send_mode
                    )
                )
        else:
            raise InvalidUsage('destination must be str or list')

        return await self.send_messages(messages, **kwargs)

    async def transfer_nft(
        self, nft_address, new_owner_address, response_address=None,
        query_id: int = 0, forward_amount: int = 0, forward_payload: bytes = None
    ):
        account = await self.client.find_account(nft_address)
        body = account.create_transfer_nft_body(
            new_owner_address, response_address, query_id, forward_amount, forward_payload
        ).serialize_boc()
        return await self.transfer(nft_address, self.client.to_nano(0.05), data=body)


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
