from ..base import TLObject
from ...utils import bytes_b64encode


class Tvm_Slice(TLObject):
    def __init__(self, data: bytes):
        self.type = 'tvm.slice'
        self.bytes = bytes_b64encode(data)


class Tvm_Cell(TLObject):
    def __init__(self, data: bytes):
        self.type = 'tvm.cell'
        self.data = bytes_b64encode(data)


class Tvm_NumberDecimal(TLObject):
    def __init__(self, number: int):
        self.type = 'tvm.numberDecimal'
        self.number = str(int(number))


class Tvm_StackEntrySlice(TLObject):
    def __init__(self, slice: Tvm_Slice):
        self.type = 'tvm.stackEntrySlice'
        self.slice = slice


class Tvm_StackEntryCell(TLObject):
    def __init__(self, cell: Tvm_Cell):
        self.type = 'tvm.stackEntryCell'
        self.cell = cell


class Tvm_StackEntryNumber(TLObject):
    def __init__(self, number: Tvm_NumberDecimal):
        self.type = 'tvm.stackEntryNumber'
        self.number = number


class Tvm_StackEntryTuple(TLObject):
    def __init__(self, tuple_data: list):
        self.type = 'tvm.stackEntryTuple'
        self.tuple = Tvm_Tuple(tuple_data)


class Tvm_StackEntryList(TLObject):
    def __init__(self, list_data):
        self.type = 'tvm.stackEntryList'
        self.list = Tvm_List(list_data)


class Tvm_Tuple(TLObject):
    def __init__(self, elements):
        self.type = 'tvm.tuple'
        self.elements = []
        for element in elements:
            if type(element) == int:
                self.elements.append(Tvm_StackEntryNumber(element))
            elif element.type == 'tvm.numberDecimal':
                self.elements.append(Tvm_StackEntryNumber(element))
            elif element.type == 'tvm.slice':
                self.elements.append(Tvm_StackEntrySlice(element))
            elif element.type == 'tvm.cell':
                self.elements.append(Tvm_StackEntryCell(element))
            elif element.type == 'tvm.tuple':
                self.elements.append(Tvm_StackEntryTuple(element.elements))
            elif element.type == 'tvm.list':
                self.elements.append(Tvm_StackEntryList(element.elements))

class Tvm_List(TLObject):
    def __init__(self, elements):
        self.type = 'tvm.list'
        self.elements = []
        for element in elements:
            if type(element) == int:
                self.elements.append(Tvm_StackEntryNumber(element))
            elif element.type == 'tvm.numberDecimal':
                self.elements.append(Tvm_StackEntryNumber(element))
            elif element.type == 'tvm.slice':
                self.elements.append(Tvm_StackEntrySlice(element))
            elif element.type == 'tvm.cell':
                self.elements.append(Tvm_StackEntryCell(element))
            elif element.type == 'tvm.tuple':
                self.elements.append(Tvm_StackEntryTuple(element.elements))
            elif element.type == 'tvm.list':
                self.elements.append(Tvm_StackEntryList(element.elements))