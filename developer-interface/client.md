# Client

_class_ `ton.TonlibClient`_(loop, ls\_index: int=0, config='https://newton-blockchain.github.io/global.config.json', keystore=None, workchain\_id=0)_

> Head class for interacting with TON\
> \
> **Usage:**
>
> ```python
> >>> client = ton.TonlibClient(loop, keystore='.keystore')
> >>> await client.init_tonlib()
> ```
>
> \
> **Parameters:**
>
> * **loop** - (required) Asyncio Event Loop
> * **keystore** - (required) Directory with keys, need 777 rights
> * **ls\_index** - (optional) Light server index
> * **config** - (optional) File or URL with the TON config
> * **work**_**chain\_id** - (optional) Workchain ID_
