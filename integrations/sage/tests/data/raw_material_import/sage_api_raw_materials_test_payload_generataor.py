"""
This class provides some test data mirroring what we get from the ITM exports template - which gets product data (which is also used for raw materials)
All field names in this file come from sage
We can get 4 possible entities from a single customer payload (in this order), each prefixed with an indicator
- I: product data
- S: product sales data
- U: customer product data
- P: supplier product data
"""


class SageApiRawMaterialTestPayloadGenerator:
    # delimiter for the ifile we are reading from
    DELIMITER = ';'

    # test product data
    SAGE_RAW_MATERIAL_PRODUCT_INDICATOR = 'I'
    SAGE_RAW_MATERIAL_CATEGORY = 'supplier_category'
    SAGE_RAW_MATERIAL_PRODUCT = '000-00-000'
    SAGE_RAW_MATERIAL_DESCRIPTION_1 = ''
    SAGE_RAW_MATERIAL_DESCRIPTION_2 = ''
    SAGE_RAW_MATERIAL_DESCRIPTION_3 = ''
    SAGE_RAW_MATERIAL_STOCK_UNIT_OF_MEASURE = 'stock_uom'
    SAGE_RAW_MATERIAL_WEIGHT_UNIT = ''
    SAGE_RAW_MATERIAL_ITEM_WEIGHT = ''
    SAGE_RAW_MATERIAL_SALES_UNIT = ' '
    SAGE_RAW_MATERIAL_SAL_STK_CONV = ''
    SAGE_RAW_MATERIAL_PURCHASE_UNIT_OF_MEASURE = 'purchase_uom'
    SAGE_RAW_MATERIAL_PUR_STK_CONV = ''
    SAGE_RAW_MATERIAL_PACKING_UNIT = ''
    SAGE_RAW_MATERIAL_PAC_STK_CONV = ''
    SAGE_RAW_MATERIAL_ACCOUNTING_CODE = ''
    SAGE_RAW_MATERIAL_TAX_LEVEL_0 = ''
    SAGE_RAW_MATERIAL_TAX_LEVEL_1 = ''
    SAGE_RAW_MATERIAL_ALTERNATE_PRODUCT = ''
    SAGE_RAW_MATERIAL_FIRM_HORIZON = ''
    SAGE_RAW_MATERIAL_REORDER_LT = ''
    SAGE_RAW_MATERIAL_PURCHASE_TEXT_0 = ''
    SAGE_RAW_MATERIAL_PURCHASE_TEXT_1 = ''
    SAGE_RAW_MATERIAL_MANUFACTURING_TEXT_0 = ''
    SAGE_RAW_MATERIAL_MANUFACTURING_TEXT_1 = ''

    # test product sales data
    SAGE_RAW_MATERIAL_PRODUCT_SALES_INDICATOR = 'S'
    SAGE_RAW_MATERIAL_PRODUCT_SALES_SUBSTITUTION_PRODUCT = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_PACKAGING = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_PACKAGING_CAPACITY = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_BASE_PRICE = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_SALES_TEXT_0 = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_SALES_TEXT_1 = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_PREP_TEXT_0 = ''
    SAGE_RAW_MATERIAL_PRODUCT_SALES_PREP_TEXT_1 = ''

    # test customer product data
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_INDICATOR = 'U'
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_CUSTOMER = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_CUSTOMER_PRODUCT = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKING_1 = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PAC_1_SAL_CONV = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKAGING = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKAGING_CAP = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_RETURN_TEXT = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_SALES_TEXT = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PREP_TEXT_0 = ''
    SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PREP_TEXT_1 = ''

    # test supplier product data
    SAGE_RAW_MATERIAL_SUPPLIER_INDICATOR = 'P'
    SAGE_RAW_MATERIAL_SUPPLIER_SUPPLIER = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PRODUCT = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PRIORITY = ''
    SAGE_RAW_MATERIAL_SUPPLIER_UPC_CODE = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_UNIT = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PUR_STK_CONV = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PACKING_UNIT = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PAC_PUR_CONV = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_TEXT_0 = ''
    SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_TEXT_1 = ''

    # test product-site data
    SAGE_RAW_MATERIAL_PRODUCT_SITE_INDICATOR = 'K'
    SAGE_RAW_MATERIAL_PRODUCT_SITE_PURCHASE_BASE_PRICE = '212.22'

    def generate_test_product_payload(self) -> str:
        """
        returns a test payload of ONLY product data
        """
        product_test_payload = self.SAGE_RAW_MATERIAL_PRODUCT_INDICATOR + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_CATEGORY + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_DESCRIPTION_1 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_DESCRIPTION_2 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_DESCRIPTION_3 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_STOCK_UNIT_OF_MEASURE + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_WEIGHT_UNIT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_ITEM_WEIGHT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_SALES_UNIT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_SAL_STK_CONV + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PURCHASE_UNIT_OF_MEASURE + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PUR_STK_CONV + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PACKING_UNIT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PAC_STK_CONV + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PACKING_UNIT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PAC_STK_CONV + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_ACCOUNTING_CODE + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_TAX_LEVEL_0 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_TAX_LEVEL_1 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_ALTERNATE_PRODUCT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_FIRM_HORIZON + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_REORDER_LT + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PURCHASE_TEXT_0 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_PURCHASE_TEXT_1 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_MANUFACTURING_TEXT_0 + self.DELIMITER
        product_test_payload += self.SAGE_RAW_MATERIAL_MANUFACTURING_TEXT_1 + self.DELIMITER

        return product_test_payload

    def generate_test_product_sales_data(self) -> str:
        product_sales_test_payload = self.SAGE_RAW_MATERIAL_PRODUCT_SALES_INDICATOR + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_SUBSTITUTION_PRODUCT + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_PACKAGING + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_PACKAGING_CAPACITY + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_BASE_PRICE + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_SALES_TEXT_0 + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_SALES_TEXT_1 + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_PREP_TEXT_0 + self.DELIMITER
        product_sales_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SALES_PREP_TEXT_1 + self.DELIMITER

        return product_sales_test_payload

    def generate_test_customer_product_data(self) -> str:
        customer_product_test_payload = self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_INDICATOR + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_CUSTOMER + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_CUSTOMER_PRODUCT + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKING_1 + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PAC_1_SAL_CONV + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKAGING + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PACKAGING_CAP + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_RETURN_TEXT + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_SALES_TEXT + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PREP_TEXT_0 + self.DELIMITER
        customer_product_test_payload += self.SAGE_RAW_MATERIAL_CUSTOMER_PRODUCT_PREP_TEXT_1 + self.DELIMITER

        return customer_product_test_payload

    def generate_test_supplier_product_data(self) -> str:
        supplier_product_test_payload = self.SAGE_RAW_MATERIAL_SUPPLIER_INDICATOR + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_SUPPLIER + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PRODUCT + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PRIORITY + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_UPC_CODE + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_UNIT + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PUR_STK_CONV + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PACKING_UNIT + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PAC_PUR_CONV + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_TEXT_0 + self.DELIMITER
        supplier_product_test_payload += self.SAGE_RAW_MATERIAL_SUPPLIER_PURCHASE_TEXT_1 + self.DELIMITER

        return supplier_product_test_payload

    def generate_test_product_site_data(self) -> str:
        product_site_test_payload = self.SAGE_RAW_MATERIAL_PRODUCT_SITE_INDICATOR + self.DELIMITER
        product_site_test_payload += self.SAGE_RAW_MATERIAL_PRODUCT_SITE_PURCHASE_BASE_PRICE + self.DELIMITER

        return product_site_test_payload

    def generate_test_full_raw_material_export_payload(self) -> str:
        """
            returns a test payload of a whole supplier payload from the sage BPS exports template
            - includes product data (I), sales product data (S), customer product data (U), and supplier product data (P)
        """

        product_data_payload = self.generate_test_product_payload() + '|'
        sales_product_data_payload = self.generate_test_product_sales_data() + '|'
        customer_product_data_payload = self.generate_test_customer_product_data() + '|'
        supplier_product_data_payload = self.generate_test_supplier_product_data() + '|'
        product_site_data_payload = self.generate_test_product_site_data() + '|'

        return product_data_payload + sales_product_data_payload + customer_product_data_payload + supplier_product_data_payload + product_site_data_payload
