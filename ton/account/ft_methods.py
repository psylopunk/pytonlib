from base64 import b64decode

from tonsdk.boc import Cell
from tonsdk.utils import Address

from ..tl.types import Tvm_StackEntrySlice, Tvm_Slice
from ..utils.cell import read_address


class FTMethods:
    async def get_jetton_data(self, **kwargs):
        response = await self.run_get_method('get_jetton_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_jetton_data exit_code: {}'.format(response.exit_code))

        return {
            'total_supply': int(response.stack[0].number.number),
            'admin_address': read_address(Cell.one_from_boc(b64decode(response.stack[2].cell.bytes))),
            'content': Cell.one_from_boc(b64decode(response.stack[3].cell.bytes)),
            'jetton_wallet_code': Cell.one_from_boc(b64decode(response.stack[4].cell.bytes))
        }

    async def get_wallet_address(self, owner_address, **kwargs):
        addr_slice = Cell()
        addr_slice.bits.write_address(Address(owner_address))
        response = await self.run_get_method('get_wallet_address', [
            Tvm_StackEntrySlice(Tvm_Slice(addr_slice.to_boc(False, False)))
        ], **kwargs)
        if response.exit_code != 0:
            raise Exception('get_wallet_address exit_code: {}'.format(response.exit_code))

        return {
            'address': read_address(Cell.one_from_boc(b64decode(response.stack[0].cell.bytes)))
        }

    async def get_wallet_data(self, **kwargs):
        response = await self.run_get_method('get_wallet_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_wallet_data exit_code: {}'.format(response.exit_code))

        return {
            'balance': int(response.stack[0].number.number),
            'owner_address': read_address(Cell.one_from_boc(b64decode(response.stack[1].cell.bytes))),
            'jetton_master_address': read_address(Cell.one_from_boc(b64decode(response.stack[2].cell.bytes))),
            'jetton_wallet_code': Cell.one_from_boc(b64decode(response.stack[3].cell.bytes))
        }

