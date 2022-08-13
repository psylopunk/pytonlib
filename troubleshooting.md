# ⚠ Troubleshooting

Library functions make requests via `ton.tl.functions`. Each of the classes is a reference to the `libtonlibjson` method ([full list](https://github.com/newton-blockchain/ton/blob/master/tl/generate/scheme/tonlib\_api.tl)).

To enable debugging of library actions, need to do this:

```python
import logging
logging.getLogger('ton').disabled = False
logging.getLogger('ton').setLevel(logging.DEBUG)
```

But apart from visible errors, the action can simply last indefinitely in time. This means that the error occurred inside `libtonlibjson` OR the selected liteserver is not responding. In that case, we need to see what's going on inside:

```python
await client.set_verbosity_level(5)
```

If it seems that the problem is in the lite server, you need to change it, reinitialize the library with a different ls\_index:

```python
client = TonlibClient(ls_index=N)
await client.init_tonlib()
```
