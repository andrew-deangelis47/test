from paperless.objects.orders import OrderComponent, OrderItem
from sage.models.sage_models.part import ProductSiteTotals
from typing import List


def get_purchased_base_price(component: OrderComponent, order_item: OrderItem):
    # if component.type == 'manufactured' or component.type == 'hardware':
    #     return order_item.unit_price
    # TODO: get this from p3L
    return 1


class PaperlessOrderItemToSageProductSiteTotalsConverter:

    @staticmethod
    def to_sage_prod_site_totals(component: OrderComponent, order_item: OrderItem) -> List[ProductSiteTotals]:
        prod_site_totals = ProductSiteTotals()
        prod_site_totals.purchase_base_price = get_purchased_base_price(component, order_item)
        return prod_site_totals
