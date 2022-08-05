## Introduction

This library allows you to work with the [TON blockchain](https://ton.org) API from Python.

**Features**:
- Creating and importing wallet
- Getting wallets balance
- Getting transactions of any wallet
- Transfering coins
- Executing methods of smart-contracts

[![PyPI version](https://badge.fury.io/py/ton.svg)](https://badge.fury.io/py/ton) ![visitors](https://visitor-badge.glitch.me/badge?page_id=psylopunk.pytonlib.readme&left_color=gray&right_color=red)

## How to install:

```bash
pip install ton
```

If you have an *illegal instruction* error then you need to build libtonlibjson by yourself:

```bash
git clone https://github.com/psylopunk/ton && cd ton
chmod +x build_tonlib.sh && ./build_tonlib.sh # docker is needed
```

### Getting started:

```python
>>> from ton import TonlibClient

>>> # Initiate module
>>> client = TonlibClient()
>>> await client.init_tonlib()

>>> # Wallet generation
>>> wallet = await client.create_wallet()
>>> wallet
Wallet<EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1>

>>> # Get a word list
>>> seed = await wallet.export()

>>> # Importing wallet
>>> wallet = await client.import_wallet(seed)

>>> # Get saved wallet from Keystore
>>> path = wallet.path
>>> wallet = await client.find_wallet(path)

>>> # Getting an address
>>> wallet.account_address.account_address
EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1

>>> # Viewing transactions
>>> txs = await wallet.get_transactions()
>>> in_msg = txs[0].in_msg
>>> in_msg.source.account_address # Sender
EQBPhcJanCxCYc-eiSxUVcm7I4-PfHODzBNhY1Cd3R5IP041

>>> in_msg.destination.account_address # Recipient
EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1

>>> from ton.utils import from_nano
>>> from_nano(int(in_msg.value)) # Amount
0.6

>>> # Sending transaction
>>> from ton.utils import to_nano
>>> await wallet.transfer('EQBPhcJanCxCYc-eiSxUVcm7I4-PfHODzBNhY1Cd3R5IP041', to_nano(0.3), comment='test')
{
    "@type": "ok",
    "@extra": "1648032761.9897776:0:0.6654941473285754"
}
>>> # View account
>>> account = await client.find_account('EQBPhcJanCxCYc-eiSxUVcm7I4-PfHODzBNhY1Cd3R5IP041')
>>> # View transactions of an account
>>> txs = await account.get_transactions() # Returns a list of TL Objects (transactions)
[
    {
    '@type': 'raw.transaction', # An example of 'in' transaction
      'data': 'XXXXXX',
      'fee': '0',
      'in_msg': {
                 '@type': 'raw.message',
                 'body_hash': 'XXXXXX',
                 'created_lt': '28669675000002',
                 'destination': {'@type': 'accountAddress',
                                 'account_address': 'XXXXXX'},
                 'fwd_fee': '666672',
                 'ihr_fee': '0',
                 'msg_data': {'@type': 'msg.dataRaw',
                              'body': 'XXXXXX',
                              'init_state': ''},
                 'source': {'@type': 'accountAddress',
                            'account_address': 'XXXXXX'},
                 'value': '1000000000'
                },
      'other_fee': '0',
      'out_msgs': [], # When it is 'in' transaction then there will be an array of msgs like 'in_msg'
      'storage_fee': '0',
      'transaction_id': {'@type': 'internal.transactionId',
                         'hash': 'XXXXXX',
                         'lt': '28669675000003'},
      'utime': 1654954281 # Timestamp
  }
]
```

### [More documentation here](docs/) <a href="#documentation" id="documentation"></a>


### Troubleshooting

Found a bug? Or just improvments? -- Read more about this in [Troubleshooting](troubleshooting.md)

