from ..tl.types import AccountAddress, Key, InputKeyRegular, \
    WalletV3InitialAccountState, ActionMsg, MsgMessage, MsgDataText, \
    Internal_TransactionId
from ..tl.functions import CreateQuery, QuerySend, GetAccountState, Raw_GetTransactions
from typing import Union
import ujson as json

class Wallet:
    def __init__(self, account_address: Union[AccountAddress, str], key: Key=None, local_password: str=None, client=None):
        if client is None: raise Exception('Client is not connected')
        if type(account_address) == str:
            account_address = AccountAddress(account_address)

        self.account_address = account_address
        self.key = key
        self.local_password = local_password
        self.client = client

    async def transfer(self, destination, amount, comment=None, allow_send_to_uninited=False, send_mode: int=0, timeout: int=300):
        if self.key is None: raise Exception('PrivateKey is empty')

        query = CreateQuery(
            InputKeyRegular(self.key, local_password=self.local_password),
            WalletV3InitialAccountState(self.key, self.client.config_info.default_wallet_id),
            self.account_address,
            ActionMsg(
                [
                    MsgMessage(
                        destination,
                        amount + 1000000,
                        data=MsgDataText(comment if not comment is None else ''),
                        send_mode=send_mode
                    )
                ],
                allow_send_to_uninited=allow_send_to_uninited
            ),
            timeout=timeout
        )

        r = await self.client.tonlib_wrapper.execute(query)
        query = QuerySend(r.id)
        r = await self.client.tonlib_wrapper.execute(query)
        return r

    async def get_state(self):
        return await self.client.tonlib_wrapper.execute(
            GetAccountState(self.account_address)
        )

    async def get_balance(self):
        return int((await self.get_state()).balance)

    async def get_transactions(self, from_transaction_lt=None, from_transaction_hash=None, to_transaction_lt=0, limit=10):
        if from_transaction_lt == None or from_transaction_hash == None:
            state = await self.get_state()
            from_transaction_lt, from_transaction_hash = state.last_transaction_id.lt, state.last_transaction_id.hash

        reach_lt = False
        all_transactions = []
        current_tx = Internal_TransactionId(
            from_transaction_lt, from_transaction_hash
        )
        while not reach_lt and len(all_transactions) < limit:
            raw_transactions = await self.client.tonlib_wrapper.execute(
                Raw_GetTransactions(
                    self.account_address,
                    current_tx
                )
            )
            transactions, current_tx = raw_transactions.transactions, raw_transactions.__dict__.get("previous_transaction_id", None)
            for tx in transactions:
                tlt = int(tx.transaction_id.lt)
                if tlt <= to_transaction_lt:
                    reach_lt = True
                    break
                all_transactions.append(tx)

            if current_tx is None:
                break

            if current_tx.lt == 0:
                break

        return all_transactions

    def export_key(self):
        if self.key is None: raise Exception('PrivateKey is empty')

        return json.dumps(self.key.to_json())