
class ConverterMethods:
    def from_nano(self, value) -> float:
        return round(int(value) / 10 ** 9, 9)

    def to_nano(self, value) -> int:
        return int(float(value) * (10 ** 9))