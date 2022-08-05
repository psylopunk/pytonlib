from .init import client
from tvm_valuetypes import Cell

# Send raw BOC
await client.send_boc(Cell().serialize_boc())