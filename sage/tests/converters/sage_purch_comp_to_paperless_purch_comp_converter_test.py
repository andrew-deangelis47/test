from sage.models.sage_models.part.product import Product as SagePurchasedComponent
from sage.models.sage_models.part.part_full_entity import PartFullEntity
from sage.models.sage_models.part.product_site_totals import ProductSiteTotals
from sage.models.converters.sage_purch_comp_to_paperless_purch_comp_converter import SagePurchasedCompToPaperlessPurchasedCompConverter
from unittest import TestCase


class TestSagePurchasedCompToPaperlessPurchasedComp(TestCase):
    # test constants
    sage_purchased_comp = None
    paperless_purchased_comp = None

    def setUp(self) -> None:
        sage_purchased_comp = SagePurchasedComponent
        sage_purchased_comp.product_code = '001'
        sage_purchased_comp.purchase_base_price = '1.00'
        sage_purchased_comp.description = 'test_description'
        sage_purchased_comp.product_category = 'TEST'
        sage_purchased_comp.stock_unit = 'EA'

        prod_site_totals = ProductSiteTotals()
        prod_site_totals.purchase_base_price = '1'

        part_full_entity = PartFullEntity()
        part_full_entity.product = sage_purchased_comp
        part_full_entity.prod_site_totals = prod_site_totals

        self.sage_purchased_comp = part_full_entity

        self.paperless_purchased_comp = SagePurchasedCompToPaperlessPurchasedCompConverter.to_paperless_purchased_comp(part_full_entity)

    def test_to_paperless_purchased_comp_sets_oem_part_number_to_product_code(self):
        assert self.paperless_purchased_comp.oem_part_number == self.sage_purchased_comp.product.product_code

    def test_to_paperless_purchased_comp_sets_piece_price_to_purchase_base_price_to(self):
        assert self.paperless_purchased_comp.piece_price == self.sage_purchased_comp.prod_site_totals.purchase_base_price

    def test_to_paperless_purchased_comp_sets_description_to_description(self):
        assert self.paperless_purchased_comp.description == self.sage_purchased_comp.product.description
