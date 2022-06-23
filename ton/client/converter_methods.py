
class ConverterMethods:
    def from_nano(self, value):
        return round(value / 10 ** 9, 9)

    def to_nano(self, value):
        return int(value * (10 ** 9))