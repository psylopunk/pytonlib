from ..base import TLObject
from ..types import InputKeyRegular
from ...utils import str_b64encode


class CreateNewKey(TLObject):
    def __init__(self, mnemonic_password: str=None, random_extra_seed: str=None, local_password: str=None):
        self.type = 'createNewKey'
        self.mnemonic_password = str_b64encode(mnemonic_password)
        self.random_extra_seed = str_b64encode(random_extra_seed)
        self.local_password = str_b64encode(local_password)


class ExportKey(TLObject):
    def __init__(self, input_key: InputKeyRegular):
        self.type = 'exportKey'
        self.input_key = input_key


class ExportUnencryptedKey(TLObject):
    def __init__(self, input_key: InputKeyRegular):
        self.type = 'exportUnencryptedKey'
        self.input_key = input_key


class ImportKey(TLObject):
    def __init__(self, exported_key, mnemonic_password, local_password=None):
        self.type = 'importKey'
        self.exported_key = exported_key
        self.mnemonic_password = str_b64encode(mnemonic_password)
        self.local_password = str_b64encode(local_password)