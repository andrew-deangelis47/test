from pydantic import BaseModel, Field
from pydantic.class_validators import validator


class EpicorPartsListTypeModel(BaseModel):
    company: str = Field(alias="Company")
    part_num: str = Field(alias="PartNum")
    part_description: str = Field(alias="PartDescription")
    class_id: str = Field(alias="ClassID")
    type_code: str = Field(alias="TypeCode")
    non_stock: bool = Field(alias="NonStock")
    prod_code: str = Field(alias="ProdCode")
    ium: str = Field(alias="IUM")  # IUM stands for Primary Inventory Unit of Measure
    pum: str = Field(alias="PUM")  # PUM stands for Purchasing Unit of Measure

    class Config:
        allow_population_by_field_name = True

    @validator("part_description")
    def truncate_description_for_paperless_payload(cls, value: str) -> str:
        max_chars = 100
        return value[:max_chars]


class EpicorPartsModel(EpicorPartsListTypeModel):
    unit_price: float = Field(alias="UnitPrice")
    internal_unit_price: float = Field(alias="InternalUnitPrice")

    class Config:
        allow_population_by_field_name = True

    @validator("unit_price")
    def truncate_for_paperless_payload(cls, value: float) -> str:
        str_format = '{:.4f}'
        return str_format.format(value)
