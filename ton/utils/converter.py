def from_nano(value):
    return round(value / 10 ** 9, 9)

def to_nano(value):
    return int(value * (10 ** 9))