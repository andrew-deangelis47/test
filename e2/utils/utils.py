from typing import NamedTuple, Tuple, Optional
import e2.models as e2
from paperless.objects.orders import OrderComponent
from paperless.objects.components import AssemblyComponent
import pycountry


def convert_pp_country_code_to_e2_country_code(pp_country_code):
    e2_country_code = None
    country = pycountry.countries.get(alpha_3=pp_country_code)
    if country is not None:
        e2_country_code = country.name

    if e2_country_code is not None:
        return e2_country_code
    else:
        return pp_country_code


def create_addr_dict(address_info):
    addr_dict = {}
    field_keys = ['address1', 'address2', 'city', 'country', 'postal_code', 'state', 'attention', 'facility_name']
    for key in field_keys:
        value = getattr(address_info, key, None)
        if key == 'country':
            value = convert_pp_country_code_to_e2_country_code(value)
        addr_dict[key] = value
    return addr_dict


def smart_truncate(val: Optional[str], max_length: int):
    if val is None:
        return None
    return val[:max_length]


class OrderLineItemData(NamedTuple):
    order_line_item: e2.OrderDet
    order_routing_lines: Tuple[e2.OrderRouting]
    release: e2.Releases


class CustomerData(NamedTuple):
    customer: e2.CustomerCode
    customer_is_new: bool


class RoutingLinesData(NamedTuple):
    routing_lines: Tuple[e2.Routing]


class JobRequirementData(NamedTuple):
    outside_service_routing_line: Optional[e2.Routing]
    purchased_component: Optional[OrderComponent]
    purchased_component_part_record: Optional[e2.Estim]
    raw_material_part_record: Optional[e2.Estim]
    raw_material_quantity: Optional[float]
    assembly_component: Optional[AssemblyComponent] = None
    order_details: Optional[e2.OrderDet] = None


class PartData(NamedTuple):
    part: e2.Estim
    is_part_new: bool
    job_requirement: Optional[JobRequirementData]
    job_requirement_list: Optional[list[JobRequirementData]]


def normalize_string_characters(string: str):
    """
    This function takes a string as an input and replaces any Unicode characters based on the mapping in the dictionary.

    Add any additional Unicode characters to the 'unicode_map' that need to be scrubbed out in case of errors resulting
    from get() queries returning "None" as a result of a funky character, that then cause 'duplicate key row' errors on
    the create() method.
    """
    unicode_map = {
        8722: "-",  # Converts minus sign to hyphen
    }
    string_list = [str(char) for char in string]
    for i, char in enumerate(string_list):
        for key, value in unicode_map.items():
            if ord(char) == key:
                string_list[i] = str(value)
    output_string = "".join(str(char) for char in string_list)
    return output_string
