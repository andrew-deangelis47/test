from typing import Union


class RawMaterialAttribute:

    field: str
    type: str
    value: Union[float, int, str]

    def __init__(self, field: str, type: str, value: Union[float, int, str]):
        self.field = field
        self.type = type
        self.value = value
