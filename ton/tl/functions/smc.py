from ..base import TLObject
from ..types import AccountAddress, Smc_MethodIdName, Smc_MethodIdNumber
from typing import Union


class Smc_Load(TLObject):
    def __init__(self, account_address: Union[str, AccountAddress]):
        if isinstance(account_address, str):
            account_address = AccountAddress(account_address)

        self.type = 'smc.load'
        self.account_address = account_address


class Smc_GetCode(TLObject):
    def __init__(self, id: int):
        self.type = 'smc.getCode'
        self.id = id


class Smc_GetData(TLObject):
    def __init__(self, id: int):
        self.type = 'smc.getData'
        self.id = id


class Smc_GetState(TLObject):
    def __init__(self, id: int):
        self.type = 'smc.getState'
        self.id = id


class Smc_RunGetMethod(TLObject):
    def __init__(self, id: int, method: Union[Smc_MethodIdName, Smc_MethodIdNumber], stack: list = []):
        if type(method) == str:
            method = Smc_MethodIdName(method)
        elif type(method) == int:
            method = Smc_MethodIdNumber(method)

        self.type = 'smc.runGetMethod'
        self.id = id
        self.method = method
        self.stack = stack