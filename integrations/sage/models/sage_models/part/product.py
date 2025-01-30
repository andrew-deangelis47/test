from sage.models.sage_models.base_object import BaseObject


class Product(BaseObject):
    SEQUENCE = [
        ('entity_type', 0),
        ('product_category', 1),
        ('product_code', 2),
        ('description', 3),
        ('stock_unit', 6),
        ('sales_unit', 9),
        ('purchase_unit', 11),
        ('accounting_code', 17),
        ('tax_level', 18),
        ('revision_number', 27)
    ]

    TOTAL_ELEMENTS = 28

    entity_type: str
    product_category: str
    product_code: str
    description: str
    stock_unit: str
    sales_unit: str
    purchase_unit: str
    accounting_code: str
    tax_level: str
    is_purchased: int
    revision_number: str

    def __init__(self):
        self.entity_type: str = 'I'
        self.product_category: str = 'RML'
        self.description: str = 'default description'
        self.stock_unit: str = 'EA'
        self.sales_unit: str = 'EA'
        self.purchase_unit: str = 'EA'
        self.accounting_code: str = 'PURRAWMAT'
        self.tax_level = 'NTX'
        self.revision_number = '0'
