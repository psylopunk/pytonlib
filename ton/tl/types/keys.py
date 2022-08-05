from ..base import TLObject
from ...utils.common import str_b64encode


class Key(TLObject):
    def __init__(self, public_key, secret=None):
        """

        :type public_key: str
        :param secret: str
        """
        self.type = 'key'
        self.public_key = public_key
        self.secret = secret


class InputKeyRegular(TLObject):
    def __init__(self, key: Key, local_password: str=None):
        self.type = 'inputKeyRegular'
        self.key = key
        self.local_password = str_b64encode(local_password)


class ExportedKey(TLObject):
    def __init__(self, word_list: list):
        self.type = 'exportedKey'
        self.word_list = word_list