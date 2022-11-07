import json
import logging
from base64 import b64encode, b64decode
from typing import Union

from nacl.signing import SigningKey

from ..errors import InvalidUsage
from ..tl.functions import CreateQuery, Query_Send, ExportKey
from ..tl.types import InputKeyRegular, Raw_InitialAccountState, ActionMsg, MsgMessage, MsgDataRaw, MsgDataText
from ..utils.wallet import sources, contracts, sha256

logger = logging.getLogger('ton')


class WalletMethods:
    async def build_state(self):
        state = await self.get_state()
        if state.code:
            return {'code': b64decode(state.code), 'data': b64decode(state.data) if state.data else state.data}

        assert hasattr(self, 'source'), 'source must be specified'
        assert hasattr(self, 'wallet_id'), 'wallet_id must be specified'
        assert hasattr(self, 'key'), 'key must be specified'
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
            ).to_boc(False)
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
        ).to_boc(False)
        return await self.transfer(nft_address, self.client.to_nano(0.05), data=body)


    async def seqno(self, **kwargs):
        result = await self.run_get_method('seqno', force=True, **kwargs)
        if result.exit_code != 0:
            return 0

        return int(result.stack[0].number.number)


    async def get_public_key(self, **kwargs):
        if hasattr(self, 'key'):
            return b64decode(
                await self.client.export_key(InputKeyRegular(self.key, local_password=self.__dict__.get('local_password')))
            )
        else:
            try:
                result = await self.run_get_method('get_public_key', **kwargs)
                assert result.exit_code == 0, 'get_public_key failed'
                return int(result.stack[0].number.number).to_bytes(32, 'big')
            except Exception as e:
                logger.debug('get_public_key failed: {}'.format(e))
                return None


    @property
    def path(self):
        """
        :return: path (str)
        """

        path_obj = dict()
        path_obj['pk'] = self.key.public_key
        path_obj['sk'] = self.key.secret if hasattr(self.key, 'secret') else None
        path_obj['wi'] = self.wallet_id if hasattr(self, 'wallet_id') else None
        path_obj['wc'] = self.workchain_id if hasattr(self, 'workchain_id') else None
        path_obj['sr'] = self.source if hasattr(self, 'source') else None
        return b64encode(
            json.dumps(path_obj).encode('utf-8')
        ).decode('utf-8')


    async def export(self):
        return ' '.join((await self.client.execute(
            ExportKey(
                InputKeyRegular(self.key, local_password=self.local_password)
            )
        )).word_list)
