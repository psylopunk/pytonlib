from .address import detect_address
from math import ceil
from bitarray.util import ba2int


def write_address(cell, address):
    if address is None:
        cell.data.put_arbitrary_uint(0, 2)
    else:
        raw_form = detect_address(address)['raw_form'].split(':')
        wc, hashpart = int(raw_form[0]), int(raw_form[1], 16)
        cell.data.put_arbitrary_uint(2, 2)
        cell.data.put_arbitrary_uint(0, 1)
        cell.data.put_arbitrary_uint(wc, 8)
        cell.data.put_arbitrary_uint(hashpart, 256)


def write_coins(cell, amount):
    if amount == 0:
        cell.data.put_arbitrary_uint(0, 4)
    else:
        l = ceil(len(f"{amount:x}") / 2)
        cell.data.put_arbitrary_uint(l, 4)
        cell.data.put_arbitrary_uint(amount, l * 8)


def write_bytes(cell, _bytes):
    for byte in _bytes:
        cell.data.put_uint8(byte)


def read_uint(bs, cursor, bits):
    return ba2int(bs[cursor:cursor + bits])


def read_address(cell):
    data = cell.data.data.to01()
    if len(data) < 267: return None
    return detect_address(f"{int(data[3:8], 2)}:{int(data[11:], 2):x}")