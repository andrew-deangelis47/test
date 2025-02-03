from sage.models.sage_models.part.part_full_entity import PartFullEntity
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent


class SagePurchasedCompToPaperlessPurchasedCompConverter:

    @staticmethod
    def to_paperless_purchased_comp(sage_purchased_component: PartFullEntity) -> PaperlessPurchasedComponent:

        # TODO: right now we are often getting blank values for this from Sage
        #       it's required for the purchased components table, default to 0.01 as
        #       stated in the SOW
        if sage_purchased_component.prod_site_totals.purchase_base_price == '':
            sage_purchased_component.prod_site_totals.purchase_base_price = '0.01'

        paperless_purchased_component = PaperlessPurchasedComponent(
            oem_part_number=sage_purchased_component.product.product_code,
            piece_price=sage_purchased_component.prod_site_totals.purchase_base_price,
            description=sage_purchased_component.product.description,
            internal_part_number=sage_purchased_component.product.product_code,
        )

        paperless_purchased_component.set_property("uom", sage_purchased_component.product.stock_unit)
        paperless_purchased_component.set_property("category", sage_purchased_component.product.product_category)

        # TODO: is stock material, this depends on the category coming in, make sure to circle back on this
        #       we probably need some sort of mapping of product categories that we care about, and what
        #       they mean
        # paperless_purchased_component.set_property('is_stock_material', sage_purchased_component.product_category)

        return paperless_purchased_component
