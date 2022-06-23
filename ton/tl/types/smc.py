from ..base import TLObject

class Smc_MethodIdNumber(TLObject):
    def __init__(self, number: int):
        self.type = 'smc.methodIdNumber'
        self.number = number

class Smc_MethodIdName(TLObject):
    def __init__(self, name: str):
        self.type = 'smc.methodIdName'
        self.name = name