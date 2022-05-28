# Synchronous

To use the library without asyncio, we can use similar code:

```python
from ton.sync import TonlibClient
client = TonlibClient()
client.init_tonlib()

# then all methods can be used without await
wallet = client.create_wallet()
```
