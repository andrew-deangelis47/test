from paperless.objects.orders import OrderComponent
from sage.models.sage_models.part import Product
from typing import List


def is_empty(some_var):
    if some_var is None:
        return True
    return len(some_var.strip()) == 0


def get_is_purchased(component: OrderComponent) -> bool:
    if component.type == "purchased":
        return 1
    return 0


def get_is_manufactured(component: OrderComponent) -> bool:
    if component.type in {'assembled', 'manufactured'}:
        return 1
    return 0


def get_description(component: OrderComponent) -> str:
    if component.type in {'hardware', 'manufactured'}:
        if component.description is not None:
            return component.description
        else:
            return "default description"

    if len(component.material_operations) > 0:
        return component.material_operations[0].notes

    return "default description"


def get_product_code(component: OrderComponent) -> str:
    if not is_empty(component.part_number):
        return component.part_number
    return "default_product_code"


def get_product_category(component: OrderComponent) -> str:
    if component.is_root_component:
        return 'FG'
    return "WIP"


class PaperlessOrderItemComponentToSageProductConverter:

    @staticmethod
    def to_sage_product(component: OrderComponent) -> List[Product]:
        product = Product()
        product.product_category = get_product_category(component)
        product.product_code = get_product_code(component)
        product.description = get_description(component)
        product.is_purchased = get_is_purchased(component)
        product.is_manufactured = get_is_manufactured(component)

        return product
