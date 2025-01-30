from attr import attr
from attr.validators import optional, instance_of
from sage.models.sage_models import BaseFullEntityObject
from sage.models.sage_models.bom import BomDetail, BomHeader
from typing import List


class BomFullEntity(BaseFullEntityObject):

    def __init__(self, bom_details: List[BomDetail], bom_header: BomHeader):
        self.bom_details = bom_details
        self.bom_header = bom_header

    bom_details = attr.ib(validator=optional(instance_of(List[BomDetail])), default=None)
    bom_header = attr.ib(validator=optional(instance_of(BomHeader)), default=None)

    def to_i_file(self):
        i_file = self.bom_header.to_i_file()
        for bom_detail in self.bom_details:
            i_file = i_file + bom_detail.to_i_file()
        return i_file + 'END'
