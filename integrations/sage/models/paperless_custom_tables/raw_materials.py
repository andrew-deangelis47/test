from pydantic import Field

from sage.models.paperless_custom_tables.custom_table import CustomTableFormat


class RawMaterial(CustomTableFormat):
    _primary_key = 'part_num'
    _custom_table_name = 'raw_materials'

    def __init__(self):
        self.part_num: str = Field(alias="part_num")
        self.piece_price: str = Field(alias="piece_price")
        self.class_id: str = Field(alias="class_id")
        self.description: str = Field(alias="description")
