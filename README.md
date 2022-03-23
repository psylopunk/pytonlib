# Introduction

This library is built entirely according to the standards of the selected language in order to admire the functionality.

Install TON using pip:

```
$ pip install ton
```

Now, let's get started:

```python
>>> from ton.sync import TonlibClient
>>> import asyncio

>>> # Initiate module
>>> client = TonlibClient(asyncio.get_event_loop(), keystore='/Keystore')
>>> client.init_tonlib()
>>> 
>>> # Creating a wallet passphrase
>>> from mnemonic import Mnemonic
>>> seed = Mnemonic('english').generate(256)
>>> 
>>> # Wallet generation
>>> key = client.create_new_key(seed.split(' '))
>>> wallet = client.init_wallet(key)
>>>
>>> # Getting an address
>>> wallet.account_address.account_address
EQCi-D5OSmueD61_ZCw7D_tcMMjB8E5e5AECZT7lCM2Gm6O1
>>>
>>> # Viewing transactions
>>> txs = wallet.get_transactions()
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
>>> wallet.transfer('EQBPhcJanCxCYc-eiSxUVcm7I4-PfHODzBNhY1Cd3R5IP041', to_nano(0.3), comment='test')
{
    "@type": "ok",
    "@extra": "1648032761.9897776:0:0.6654941473285754"
}
```

### Documentation <a href="#documentation" id="documentation"></a>

To get acquainted with all the basics, go to [Developer Interface](developer-interface/)

### Dependencies <a href="#dependencies" id="dependencies"></a>

The TON library relies on these excellent libraries:

* `crc16` - Library for calculating CRC16
* `poetry` - Python packaging and dependency management made easy
* `httpx` _- A next-generation HTTP client for Python_
* `ujson` - Ultra fast JSON encoder and decoder
* `ed25519` - Public-key signature system
* `mnemonic` - Mnemonic code for generating deterministic keys
