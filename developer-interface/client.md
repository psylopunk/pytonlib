# Client

_class_ `ton.TonlibClient`_(ls\_index: int=0, config='https://newton-blockchain.github.io/global.config.json', keystore=None, workchain\_id=0)_

> Head class for interacting with TON\
> \
> **Usage:**
>
> ```python
> >>> client = ton.TonlibClient(keystore='.keystore')
> >>> await client.init_tonlib()
> ```
>
> \
> **Parameters:**
>
> * **keystore** - (str, optional) Directory with keys, need 777 rights. Default is `.keystore`
> * **ls\_index** - (int, optional) Light server index
> * **config** - (str, optional) File or URL with the TON config
> * **work**_**chain\_id** - (int, optional) Workchain ID_
