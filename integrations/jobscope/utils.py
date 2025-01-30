from typing import NamedTuple
from paperless.objects.orders import OrderComponent


class Customer:
    pass


class Part:
    pass


class Routing:
    pass


class BOM:
    pass


class Job:
    pass


def get_part_number_and_name(component):
    part_number = component.part_number
    if not part_number:
        part_number = str(component.part_name)[0:20]
    part_name = component.part_name
    return part_number[0:20], part_name


class ItemData(NamedTuple):
    item_number: str
    component: OrderComponent
    item_is_new: bool
