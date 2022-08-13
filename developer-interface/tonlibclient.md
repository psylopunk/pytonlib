# TonlibClient

In TON we have a library (or a binary) called _tonlib_. It is used to interact with TON blokchain.\
This class creates an instanse of the tonlib to do the all TON stuff.

```python
class ton.TonlibClient(keystore=None,
                       config='https://newton-blockchain.github.io/global.config.json',
                       ls_index: int=0, workchain_id=0)
```

#### Parameters:

* **keystore** – (str, optional) Directory where keys (will be) stored, need 777 rights. Default is `.keystore`.
* **config** – (str, optional) File or URL with the TON config.
* **ls\_index** – (int, optional) Light server index. Like config modes. More [here](https://github.com/ton-blockchain/ton/blob/master/lite-client/lite-client.cpp#L329).
* **workchain\_id** – (int, optional) Workchain ID. With this parameter, you can work, for example, in the masterchain by specifying -1 or in the workchain by specifying 0. No one really knows how this parameter will be used in the future, but it is there.

### Usage example:

**Default:**

```python
>>> # Classic initializing.
>>> client = ton.TonlibClient()
>>> await client.init_tonlib()
```

**Advanced:**

```python
>>> # The following code will use libtonlibjson from the current
>>> # directory, will use testnet config, will save keys in .mykeys
>>> # directory and will start the lightserver in mode 2.
>>> client = ton.TonlibClient(keystore='.mykeys',
                              config='https://ton-blockchain.github.io/testnet-global.config.json',
                              ls_index=2)
>>> await client.init_tonlib(cdll_path='./libtonlibjson.so')
```

### Methods:

*   `init_tonlib(self, cdll_path=None)`

    Initialising of a tonlib library. Can take it's path.\
    Default path will be selected automaticaly depending on your OS and CPU acrhitecture.\

*   `reconnect(self)`

    Reinitializing of a tonlib. In case if something gone wrong, for example.\

*   `execute(self, query, timeout=30) -> result TLObject`

    Direct request to liteserver.\
    In mostly, used by the other functions of module like transfer, get\_address, etc.

    **query**: dict or TLObject\
    **timeout**: int\

* `find_account(address, preload_state=True) -> Account`\
  _``_Load Account instance of any address\
  **address**: str in b64url form\
  **preload\_state**: bool. Load state in cache\

* `create_wallet(source='v3r2', workchain_id=0, wallet_id=0, local_password=None) -> Account`\
  ``The easiest and most intuitive way to create a wallet.\
  ``**source**: (str) Wallet version. It is better not to change, because others are not supported by libtonlibjson :(\
  **workchain\_id:** (int, optional) Workchain ID. With this parameter, you can work, for example, in the masterchain by specifying -1 or in the workchain by specifying 0. No one really knows how this parameter will be used in the future, but it is there.\
  **wallet\_id**: (int, optional) Wallet ID. Derivation parameter\
  **local\_password**: (None, str) password for encrypt keys in keystore dir\

* `find_wallet(path, local_password=None)`\
  Getting wallet from Keystore via Wallet.path\
  **path**: (str) serialized key-path\
  **local\_password**: (None, str) password for encrypt keys in keystore dir\

* `import_wallet(word_list, source='v3r2', workchain_id=0, wallet_id=0, local_password=None) -> Account`\
  ``Import wallet using seed phrase. Do not use this all the time with one wallet, because a new file is created in the Keystore every time \
  **word\_list**: (str) seed phrase separated by spaces\
  **source**: (str) Wallet version. It is better not to change, because others are not supported by libtonlibjson :(\
  **workchain\_id:** (int, optional) Workchain ID. With this parameter, you can work, for example, in the masterchain by specifying -1 or in the workchain by specifying 0. No one really knows how this parameter will be used in the future, but it is there.\
  **wallet\_id**: (int, optional) Wallet ID. Derivation parameter\
  **local\_password**: (None, str) password for encrypt keys in keystore dir\

* `from_nano(amount)`\
  `to_nano(amount)`\
  ``Conversion of amounts from TONs to nanoTONs and back\

* `init_wallet(key, source='v3r2', workchain_id=0, wallet_id=0, local_password=None) -> Account`\
  ``**key**: (required) Key. May be created using `create_new_key`\
  ``**source**: (str) Wallet version. It is better not to change, because others are not supported by libtonlibjson :(\
  **workchain\_id:** (int, optional) Workchain ID. With this parameter, you can work, for example, in the masterchain by specifying -1 or in the workchain by specifying 0. No one really knows how this parameter will be used in the future, but it is there.\
  **wallet\_id**: (int, optional) Wallet ID. Derivation parameter\
  **local\_password**: (None, str) password for encrypt keys in keystore dir\

* `send_boc(message) -> result TLObject`\
  ``Send raw boc messages to liteserver\
  **message**: (bytes) serialized cells\

* `set_verbosity_level(level) -> result TLObject`\
  ``Setting the log level from 0 to 5 for the libtonlibjson execution debug\
  **level**: (int) 0-5\

* `create_new_key(mnemonic_password='', random_extra_seed=None, local_password=None)`\
  ``The method creates a new private key in the Keystore to initialize the wallet account. In order for all applications to support the created wallet, do not add arguments.\

* `export_key(input_key)`\
  ``Export NaCl raw private key for signing messages\
  ``**input\_key**: (InputKeyRegular)\
  **Usage:**\
  ****`from ton.tl.types import InputKeyRegular`\
  ****`client.export_key(InputKeyRegular(wallet.key, local_password=None))`

