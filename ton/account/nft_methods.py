from base64 import b64decode

from tonsdk.boc import Cell
from tonsdk.utils import Address

from ..tl.types import Tvm_StackEntryNumber, Tvm_NumberDecimal
from ..utils.cell import read_address


class NFTMethods:
    async def get_nft_data(self, **kwargs):
        response = await self.run_get_method('get_nft_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_nft_data exit_code: {}'.format(response.exit_code))


        return {
            'is_initialized': int(response.stack[0].number.number),
            'index': int(response.stack[1].number.number),
            'collection_address': read_address(Cell.one_from_boc(b64decode(response.stack[2].cell.bytes))),
            'owner_address': read_address(Cell.one_from_boc(b64decode(response.stack[3].cell.bytes))),
            'content': Cell.one_from_boc(b64decode(response.stack[4].cell.bytes))
        }


    async def get_collection_data(self, **kwargs):
        response = await self.run_get_method('get_collection_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_collection_data exit_code: {}'.format(response.exit_code))

        return {
            'next_item_index': int(response.stack[0].number.number),
            'content': Cell.one_from_boc(b64decode(response.stack[1].cell.bytes)),
            'owner_address': read_address(Cell.one_from_boc(b64decode(response.stack[2].cell.bytes)))
        }


    async def get_nft_address_by_index(self, index, **kwargs):
        response = await self.run_get_method(
            'get_nft_address_by_index', [Tvm_StackEntryNumber(Tvm_NumberDecimal(index))], **kwargs)
        if response.exit_code != 0:
            raise Exception('get_nft_address_by_index exit_code: {}'.format(response.exit_code))

        return {
            'address': read_address(Cell.one_from_boc(b64decode(response.stack[0].cell.bytes)))
        }


    async def royalty_params(self, **kwargs):
        response = await self.run_get_method('royalty_params', **kwargs)
        if response.exit_code != 0:
            raise Exception('royalty_params exit_code: {}'.format(response.exit_code))

        return {
            'royalty_factor': int(response.stack[0].number.number),
            'royalty_base': int(response.stack[1].number.number),
            'royalty': int(response.stack[0].number.number) / int(response.stack[1].number.number),
            'royalty_address': read_address(Cell.one_from_boc(b64decode(response.stack[2].cell.bytes)))
        }


    def create_transfer_nft_body(
        self, new_owner_address, response_address=None, query_id: int = 0,
        forward_amount: int = 0, forward_payload: bytes = None
    ) -> Cell:
        cell = Cell()
        cell.bits.write_uint(0x5fcc3d14, 32)  # transfer op-code
        cell.bits.write_uint(query_id, 64)
        cell.bits.write_address(Address(new_owner_address))
        cell.bits.write_address(Address(response_address or new_owner_address))
        cell.bits.write_uint(0, 1)  # null custom_payload
        cell.bits.write_grams(forward_amount)
        cell.bits.write_uint(0, 1)  # forward_payload in this slice, not separate cell
        if forward_payload:
            cell.bits.write_bytes(forward_payload)

        return cell