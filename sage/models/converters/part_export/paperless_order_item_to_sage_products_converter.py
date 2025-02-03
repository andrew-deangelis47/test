from paperless.objects.orders import OrderItem
from sage.models.sage_models.part import PartFullEntity
from .paperless_order_item_to_sage_product_site_totals_converter import PaperlessOrderItemToSageProductSiteTotalsConverter
from .paperless_order_item_component_to_sage_products_converter import PaperlessOrderItemComponentToSageProductConverter


class PaperlessOrderItemToSageProductsConverter:

    @staticmethod
    def to_sage_product(part_number: str, part_name: str, order_component, order_item: OrderItem):
        product = PaperlessOrderItemComponentToSageProductConverter.to_sage_product(order_component)
        prod_site_totals = PaperlessOrderItemToSageProductSiteTotalsConverter.to_sage_prod_site_totals(order_component,
                                                                                                       order_item)
        return PartFullEntity(product, prod_site_totals)
