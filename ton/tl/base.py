import ujson as json

class TLObject:
    def __repr__(self):
        return json.dumps(self.to_json(), indent=4)

    def __init__(self, _type):
        if type(_type) != str:
            raise Exception(f'@type must be a string, {_type}')

        self.type = _type

    def to_json(self):
        _values = {}
        for key in self.__dict__:
            if key == 'type':
                continue
            elif type(self.__dict__[key]) == list:
                _values[key] = []
                for i, e in enumerate(self.__dict__[key]):
                    if isinstance(e, TLObject):
                        _values[key].append(e.to_json())
                    else:
                        _values[key].append(e)
            elif isinstance(self.__dict__[key], TLObject):
                _values[key] = self.__dict__[key].to_json()
            else:
                _values[key] = self.__dict__[key]

        return {
            '@type': self.type,
            **_values
        }

    @classmethod
    def from_json(cls, entries):
        if '@type' not in entries:
            raise Exception('Type is not specified')

        object = TLObject(entries['@type'])
        del entries['@type']
        _data = {}
        for key in entries:
            if type(entries[key]) == dict:
                _data[key] = TLObject.from_json(entries[key])
            elif type(entries[key]) == list:
                _data[key] = []
                for i, e in enumerate(entries[key]):
                    if type(e) == dict:
                        _data[key].append(TLObject.from_json(e))
                    else:
                        _data[key].append(e)
            else:
                _data[key] = entries[key]

        object.__dict__.update(_data)
        return object