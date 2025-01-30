from plex_v2.objects.part import Part
from plex_v2.objects.customer import CustomerPart
from typing import List
from paperless.objects.orders import OrderItem


class PlexPartToPlexCustomerPartMapping:
    """
    represents a plex part and it's corresponding customer part, and it's quantity, for the current order
    """

    part: Part
    customer_part: CustomerPart
    pp_order_item: OrderItem

    def __init__(self, part: Part, customer_part: CustomerPart, order_item: OrderItem):
        self.part = part
        self.customer_part = customer_part
        self.pp_order_item = order_item


class PlexPartToPlexCustomerPartMappings:

    mappings: List[PlexPartToPlexCustomerPartMapping]

    def __init__(self):
        self.mappings: List[PlexPartToPlexCustomerPartMapping] = []

    def add_mapping(self, mapping: PlexPartToPlexCustomerPartMapping) -> None:
        self.mappings.append(mapping)
