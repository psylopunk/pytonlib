from .init import client
from .wallet import wallet

# Viewing transactions
txs = await wallet.get_transactions()
in_msg = txs[0].in_msg
in_msg.source.account_address  # Sender
in_msg.destination.account_address  # Recipient
int(in_msg.amount)  # Amount in nanoTONs
client.from_nano(int(in_msg.value))  # Amount in TONs

# Sending transaction with 1 TON
await wallet.transfer('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ', client.to_nano(1), comment='test')

# Send transaction with multiple outputs
await wallet.transfer(
    ('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ', client.to_nano(1), 'test comment'),
    ('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ', client.to_nano(0.5), 'test comment 2'),
    ('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ', client.to_nano(1))
)

# Sending transaction with raw BOC data
from tvm_valuetypes import Cell
await wallet.transfer('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ', client.to_nano(1), data=Cell().serialize_boc())


# View account
account = await client.find_account('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ')
# View transactions of an account
txs = await account.get_transactions()  # Returns a list of TL Objects (transactions)
# [
#     {
#     '@type': 'raw.transaction', # An example of 'in' transaction
#       'data': 'XXXXXX',
#       'fee': '0',
#       'in_msg': {
#                  '@type': 'raw.message',
#                  'body_hash': 'XXXXXX',
#                  'created_lt': '28669675000002',
#                  'destination': {'@type': 'accountAddress',
#                                  'account_address': 'XXXXXX'},
#                  'fwd_fee': '666672',
#                  'ihr_fee': '0',
#                  'msg_data': {'@type': 'msg.dataRaw',
#                               'body': 'XXXXXX',
#                               'init_state': ''},
#                  'source': {'@type': 'accountAddress',
#                             'account_address': 'XXXXXX'},
#                  'value': '1000000000'
#                 },
#       'other_fee': '0',
#       'out_msgs': [], # When it is 'in' transaction then there will be an array of msgs like 'in_msg'
#       'storage_fee': '0',
#       'transaction_id': {'@type': 'internal.transactionId',
#                          'hash': 'XXXXXX',
#                          'lt': '28669675000003'},
#       'utime': 1654954281 # Timestamp
#   }
# ]