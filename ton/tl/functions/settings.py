from ..base import TLObject

class SetLogVerbosityLevel(TLObject):
    def __init__(self, level: int):
        self.type = 'setLogVerbosityLevel'
        self.new_verbosity_level = level