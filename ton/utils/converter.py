import warnings

def from_nano(value):
    warnings.DeprecationWarning("ton.utils.from_nano is deprecated, use TonlibClient.from_nano instead")
    return round(value / 10 ** 9, 9)

def to_nano(value):
    warnings.DeprecationWarning("ton.utils.to_nano is deprecated, use TonlibClient.to_nano instead")
    return int(value * (10 ** 9))