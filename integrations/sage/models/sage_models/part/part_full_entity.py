from .product import Product
from .product_site_totals import ProductSiteTotals
import attr
from attr.validators import instance_of, optional
from sage.models.sage_models.base_full_entity_object import BaseFullEntityObject


class PartFullEntity(BaseFullEntityObject):

    def __init__(self, product: Product = None, prod_site_totals: ProductSiteTotals = None):
        self.product = product
        self.prod_site_totals = prod_site_totals

    product = attr.ib(validator=optional(instance_of(Product)), default=None)
    prod_site_totals = attr.ib(validator=optional(instance_of(ProductSiteTotals)), default=None)

    def to_i_file(self):
        return self.product.to_i_file() + self.prod_site_totals.to_i_file() + 'END'
