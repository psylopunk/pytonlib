# Client

In TON we have a library (or a binary) called _tonlib_. It is used to interact with TON blokchain.
\
This class creates an instanse of the tonlib to do the all TON stuff.

``` python
class ton.TonlibClient(keystore=None,
                       config='https://newton-blockchain.github.io/global.config.json',
                       ls_index: int=0, workchain_id=0)
```

#### Parameters:

* **keystore** -- (str, optional) Directory where keys (will be) stored, need 777 rights. Default is `.keystore`.
* **config** -- (str, optional) File or URL with the TON config.
* **ls\_index** -- (int, optional) Light server index. Like config modes. More [here](https://github.com/ton-blockchain/ton/blob/master/lite-client/lite-client.cpp#L329).
* **work**_**chain\_id** -- (int, optional) Workchain ID. With this parameter, you can work, for example, in the masterchain by specifying -1 or in the workchain by specifying 0. No one really knows how this parameter will be used in the future, but it is there.

</br>

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

</br>

### Methods:
* `init_tonlib(self, cdll_path=None)`

    Initialising of a tonlib library. Can take it's path.
    \
    Default path will be selected automaticaly depending on your OS and CPU acrhitecture.


* `reconnect(self)`

    Reinitializing of a tonlib. In case if something gone wrong, for example.


* `execute(self, query, timeout=30) -> result: TL Object`

    Direct request to liteserver.
    \
    In mostly, used by the other functions of module like transfer, get_address, etc.

    **query**: dict or TLObject
    \
    **timeout**: int
