from ..utils.cell import read_address, write_address, write_coins, write_bytes
from ..tl.types import Tvm_StackEntryNumber, Tvm_NumberDecimal
from tvm_valuetypes import Cell, deserialize_boc
from base64 import b64decode

class NFTMethods:
    async def get_nft_data(self, **kwargs):
        response = await self.run_get_method('get_nft_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_nft_data exit_code: {}'.format(response.exit_code))


        return {
            'is_initialized': int(response.stack[0].number.number),
            'index': int(response.stack[1].number.number),
            'collection_address': read_address(deserialize_boc(b64decode(response.stack[2].cell.bytes))),
            'owner_address': read_address(deserialize_boc(b64decode(response.stack[3].cell.bytes))),
            'content': deserialize_boc(b64decode(response.stack[4].cell.bytes))
        }


    async def get_collection_data(self, **kwargs):
        response = await self.run_get_method('get_collection_data', **kwargs)
        if response.exit_code != 0:
            raise Exception('get_collection_data exit_code: {}'.format(response.exit_code))

        return {
            'next_item_index': int(response.stack[0].number.number),
            'content': deserialize_boc(b64decode(response.stack[1].cell.bytes)),
            'owner_address': read_address(deserialize_boc(b64decode(response.stack[2].cell.bytes)))
        }


    async def get_nft_address_by_index(self, index, **kwargs):
        response = await self.run_get_method(
            'get_nft_address_by_index', [Tvm_StackEntryNumber(Tvm_NumberDecimal(index))], **kwargs)
        if response.exit_code != 0:
            raise Exception('get_nft_address_by_index exit_code: {}'.format(response.exit_code))

        return {
            'address': read_address(deserialize_boc(b64decode(response.stack[0].cell.bytes)))
        }


    async def royalty_params(self, **kwargs):
        response = await self.run_get_method('royalty_params', **kwargs)
        if response.exit_code != 0:
            raise Exception('royalty_params exit_code: {}'.format(response.exit_code))

        return {
            'royalty_factor': int(response.stack[0].number.number),
            'royalty_base': int(response.stack[1].number.number),
            'royalty': int(response.stack[0].number.number) / int(response.stack[1].number.number),
            'royalty_address': read_address(deserialize_boc(b64decode(response.stack[2].cell.bytes)))
        }


    def create_transfer_nft_body(
        self, new_owner_address, response_address=None, query_id: int = 0,
        forward_amount: int = 0, forward_payload: bytes = None
    ) -> Cell:
        cell = Cell()
        cell.data.put_arbitrary_uint(0x5fcc3d14, 32)  # transfer op-code
        cell.data.put_arbitrary_uint(query_id, 64)
        write_address(cell, new_owner_address)
        write_address(cell, response_address)
        cell.data.put_arbitrary_uint(0, 1)  # null custom_payload
        write_coins(cell, forward_amount)
        cell.data.put_arbitrary_uint(0, 1)  # forward_payload in this slice, not separate cell
        if forward_payload: write_bytes(cell, forward_payload)
        return cell