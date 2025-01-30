import mietrak_pro.models
from typing import NamedTuple, Optional, Tuple, Union, List
from paperless.objects.orders import OrderedAddOn
from paperless.objects.quotes import AddOn


def create_addr_dict(address_info):
    addr_dict = {}
    field_keys = ['address1', 'address2', 'city', 'country', 'postal_code', 'state', 'attention', 'facility_name']
    for key in field_keys:
        value = getattr(address_info, key, None)
        addr_dict[key] = value
    return addr_dict


class CustomerData(NamedTuple):
    customer: mietrak_pro.models.Party
    is_customer_new: bool


class RawMaterialPartData(NamedTuple):
    raw_material_part: Optional[mietrak_pro.models.Item]
    is_raw_material_new: Optional[bool]
    raw_material_bom_quantity: Optional[float]


class PartData(NamedTuple):
    part: mietrak_pro.models.Item
    is_part_new: bool
    raw_material_part_data: Optional[List[RawMaterialPartData]]


class RouterData(NamedTuple):
    router: mietrak_pro.models.Router
    is_router_new: bool


class AddOnData(NamedTuple):
    add_on: Union[OrderedAddOn, AddOn]
    add_on_item: mietrak_pro.models.Item
    should_include_add_on_item_in_bom: bool


class RoutingLinesData(NamedTuple):
    routing_lines: Tuple[mietrak_pro.models.Routerworkcenter]


class BillOfMaterial:  # TODO - talk to the team about why these are necessary (tables in MIE Trak Pro are polymorphic)
    """ Trivial class to allow separate BOM and RoutingLine processors to be registered. """
    pass


class RoutingLine:
    """ Trivial class to allow separate BOM and RoutingLine processors to be registered. """
    pass


class Estimator:
    """ Trivial class to make the code more clear - the estimator is a reference to the User table. """
    pass


class AdditionalCharge:
    """ Trivial class to make the code more clear - an add-on in MIE Trak Pro is represented by an Item with type
        Tooling or Miscellaneous. """
    pass


class AdditionalChargeSalesOrderLine:
    """ Trivial class to make the code more clear """
    pass
