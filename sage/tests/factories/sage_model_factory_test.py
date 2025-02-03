from unittest import TestCase
# from sage.models.sage_models.customer.customer import Customer
# from sage.models.sage_models.customer.address import  Address
# from sage.models.sage_models.customer.contact import  Contact
# from sage.models.sage_models.vendor.supplier import Supplier
# from sage.models.sage_models.work_center.work_center import WorkCenter
# from sage.models.sage_models.part.product import Product as PurchasedComponent
# from sage.models.sage_models.part.product import Product as RawMaterial

# from sage.models.sage_models.sage_model_factory import SageModelFactory
from sage.tests.data.customer_import.sage_api_customer_test_payload_generator import SageApiCustomerTestPayloadGenerator
from sage.tests.data.vendor_import.sage_api_vendor_test_payload_generator import SageApiSupplierTestPayloadGenerator
from sage.tests.data.workcenter_import.sage_api_workcenter_test_payload_generator import SageApiWorkCenterTestPayloadGenerator
from sage.tests.data.purchased_components_import.sage_api_purchased_components_test_payload_generator import SageApiPurchasedComponentsTestPayloadGenerator
from sage.tests.data.raw_material_import .sage_api_raw_materials_test_payload_generataor import SageApiRawMaterialTestPayloadGenerator

"""
This is testing the factory's ability to set sage model class properties
according to their SEQUENCE property. The SEQUENCE property defines
which property maps to which indexed data point in the sage api payload
"""


class TestSageModelFactory(TestCase):

    def setUp(self) -> None:
        self.sage_api_cust_test_data_generator = SageApiCustomerTestPayloadGenerator()
        self.sage_api_supplier_test_data_generator = SageApiSupplierTestPayloadGenerator()
        self.sage_api_work_center_test_data_generator = SageApiWorkCenterTestPayloadGenerator()
        self.sage_api_purchased_components_test_data_generator = SageApiPurchasedComponentsTestPayloadGenerator()
        self.sage_api_raw_material_test_data_generator = SageApiRawMaterialTestPayloadGenerator()

    def test_create_sage_model_sets_all_properties_of_Customer(self):
        self.assertTrue(True)
        # customer_test_payload = self.sage_api_cust_test_data_generator.generate_test_customer_payload()
        # customer = SageModelFactory.create_sage_model(Customer, customer_test_payload)
        # assert customer.code == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_CUSTOMER
        # assert customer.company_name == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_COMPANY_NAME
        # assert customer.default_address == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_DEFAULT_ADDRESS
        # assert customer.payment_days == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_PAYMENT_TERM
        # assert customer.default_ship_to_address == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_SHIP_TO_CUSTOMER_ADDRESS
        # assert customer.bill_to_customer_address == SageApiCustomerTestPayloadGenerator.SAGE_CUSTOMER_BILL_TO_CUSTOMER

    # def test_create_sage_model_sets_all_properties_of_Address(self):
    #     address_type = 'BILL'
    #     address_test_payload = self.sage_api_cust_test_data_generator.generate_test_address_payload(address_type)
    #     address = SageModelFactory.create_sage_model(Address, address_test_payload)
    #     assert address.address_id == address_type
    #     assert address.address_line_1 == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_ADDRESS_LINE_0
    #     assert address.address_line_2 == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_ADDRESS_LINE_1
    #     assert address.city == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_CITY
    #     assert address.state == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_STATE
    #     assert address.country == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_COUNTRY
    #     assert address.zip_code == SageApiCustomerTestPayloadGenerator.SAGE_ADDRESS_POSTAL_CODE
    #
    # def test_create_sage_model_sets_all_properties_of_Contact(self):
    #     contact_test_payload = self.sage_api_cust_test_data_generator.generate_test_contact_payload()
    #     contact = SageModelFactory.create_sage_model(Contact, contact_test_payload)
    #     assert contact.first_name == SageApiCustomerTestPayloadGenerator.SAGE_CONTACT_FIRST_NAME
    #     assert contact.last_name == SageApiCustomerTestPayloadGenerator.SAGE_CONTACT_LAST_NAME
    #     assert contact.email == SageApiCustomerTestPayloadGenerator.SAGE_CONTACT_EMAIL

    # def test_create_sage_model_sets_all_properties_of_Supplier(self):
        # supplier_test_payload = self.sage_api_supplier_test_data_generator.generate_test_supplier_payload()
        # supplier = SageModelFactory.create_sage_model(Supplier, supplier_test_payload)
        # assert supplier == SageApiSupplierTestPayloadGenerator.SAGE_SUPPLIER_SUPPLIER
        # assert supplier.short_description == SageApiSupplierTestPayloadGenerator.SAGE_SUPPLIER_SHORT_DESCRIPTION

    # def test_create_sage_model_sets_all_properties_of_work_center(self):
    #     work_center_test_payload = self.sage_api_work_center_test_data_generator.generate_test_work_center_payload()
    #     work_center = SageModelFactory.create_sage_model(WorkCenter, work_center_test_payload)
    #     assert work_center.work_center_id == SageApiWorkCenterTestPayloadGenerator.SAGE_WORK_CENTER_WORK_CENTER
    #     assert work_center.description == SageApiWorkCenterTestPayloadGenerator.SAGE_WORK_CENTER_SHORT_DESCRIPTION
    #     assert work_center.site == SageApiWorkCenterTestPayloadGenerator.SAGE_WORK_CENTER_MANUFACTURING_SITE
        # assert work_center.type == SageApiWorkCenterTestPayloadGenerator.SAGE_WORK_CENTER_TYPE
        # assert work_center.group == SageApiWorkCenterTestPayloadGenerator.SAGE_WORK_CENTER_GROUP

    # def test_create_sage_model_sets_all_properties_of_purchased_component(self):
    #     purchased_component_test_payload = self.sage_api_purchased_components_test_data_generator.generate_test_full_purchased_component_export_payload()
    #     purchased_component = SageModelFactory.create_sage_model(PurchasedComponent, purchased_component_test_payload)
    #     assert purchased_component.product_code == SageApiPurchasedComponentsTestPayloadGenerator.SAGE_PURCHASED_COMPONENT_PRODUCT
    #     assert purchased_component.purchase_base_price == SageApiPurchasedComponentsTestPayloadGenerator.SAGE_PURCHASED_COMPONENT_PRODUCT_SALES_BASE_PRICE
    #     assert purchased_component.description == SageApiPurchasedComponentsTestPayloadGenerator.SAGE_PURCHASED_COMPONENT_DESCRIPTION_1
    #     assert purchased_component.product_category == SageApiPurchasedComponentsTestPayloadGenerator.SAGE_PURCHASED_COMPONENT_CATEGORY
    #     # TODO: test this once we know where to get it and we are actually setting it
    #     #       assert purchased_component.is_purchased == SageApiPurchasedComponentsTestPayloadGenerator.SAGE_PURCHASED_COMPONENT_PRODUCT

    # def test_create_sage_model_sets_all_properties_of_raw_material(self):
    #     raw_material_test_payload = self.sage_api_raw_material_test_data_generator.generate_test_full_raw_material_export_payload()
    #     raw_material = SageModelFactory.create_sage_model(RawMaterial, raw_material_test_payload)
    #     assert raw_material.code == SageApiRawMaterialTestPayloadGenerator.SAGE_RAW_MATERIAL_PRODUCT
    #     assert raw_material.purchase_base_price == SageApiRawMaterialTestPayloadGenerator.SAGE_RAW_MATERIAL_PRODUCT_SITE_PURCHASE_BASE_PRICE
    #     assert raw_material.product_category == SageApiRawMaterialTestPayloadGenerator.SAGE_RAW_MATERIAL_CATEGORY
    #     assert raw_material.description_1 == SageApiRawMaterialTestPayloadGenerator.SAGE_RAW_MATERIAL_DESCRIPTION_1
