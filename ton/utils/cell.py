from tonsdk.utils import Address


def read_address(cell):
    data = ''.join([str(cell.bits.get(x)) for x in range(cell.bits.length)])
    if len(data) < 267: return None
    return Address(f"{int(data[3:11], 2)}:{int(data[11:11+256], 2).to_bytes(32, 'big').hex()}")
