# Introduction

This library is built entirely according to the standards of the selected language in order to admire the functionality.

[![PyPI version](https://badge.fury.io/py/ton.svg)](https://badge.fury.io/py/ton)

Install TON using pip:

```bash
$ pip install ton
```

or (if error with illegal instructions):

```bash
$ git clone https://github.com/psylopunk/ton && cd ton
$ chmod +x build_tonlib.sh && ./build_tonlib.sh # docker is needed
```

### Now, let's get started:

```python
>>> from ton import TonlibClient
>>>
>>> # Initiate module
>>> client = TonlibClient()
>>> await client.init_tonlib()
>>> 
>>> # Wallet generation
>>> wallet = await client.create_wallet()
>>> wallet
Wallet<EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1>
>>>
>>> # Get a word list
>>> seed = await wallet.export()
>>>
>>> # Importing wallet
>>> wallet = await client.import_wallet(seed)
>>>
>>> # Get saved wallet from Keystore
>>> path = wallet.path
>>> wallet = await client.find_wallet(path)
>>>
>>> # Getting an address
>>> wallet.account_address.account_address
EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1
>>>
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
>>> 
>>> # Sending transaction
>>> from ton.utils import to_nano
>>> await wallet.transfer('EQBPhcJanCxCYc-eiSxUVcm7I4-PfHODzBNhY1Cd3R5IP041', to_nano(0.3), comment='test')
{
    "@type": "ok",
    "@extra": "1648032761.9897776:0:0.6654941473285754"
}
```

### Documentation <a href="#documentation" id="documentation"></a>

To get acquainted with all the basics, go to [Developer Interface](developer-interface/)

### Troubleshooting

Read more about this in [Troubleshooting](./#undefined)

### Dependencies <a href="#dependencies" id="dependencies"></a>

The TON library relies on these excellent libraries:

* `crc16` - Library for calculating CRC16
* `poetry` - Python packaging and dependency management made easy
* `requests` _- HTTP interface for python_
* `ujson` - Ultra fast JSON encoder and decoder
* `ed25519` - Public-key signature system
