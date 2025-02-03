# from sage.converters.sage_address_to_paperless_billing_address_converter imports SageAddressToPaperlessBillingAddressConverter
# from sage.sage_models imports Address as SageAddress
# imports unittest
#
# TODO: fix this test, something is going wonky with the AddressUtils.get_country_and_state function during tests
#
# class TestSageAddressToPaperlessBillingAddressConverter(unittest.TestCase):
#
#     # test constants
#     sage_address = None
#     paperless_address = None
#
#     def setUp(self) -> None:
#         sage_address = SageAddress
#         sage_address.address_line_1 = 'address_line_1'
#         sage_address.address_line_2 = 'address_line_2'
#         sage_address.city = 'city'
#         sage_address.state = 'state'
#         sage_address.country = 'US'
#         sage_address.zip_code = 'zip_code'
#
#         self.sage_address = sage_address
#         self.paperless_address = SageAddressToPaperlessBillingAddressConverter.to_paperless_billing_address(sage_address, 'cust_code')
#
#     def test_to_paperless_address_sets_address1_to_bill_to_customer_address_address_line_1(self):
#         self.assertEqual(self.paperless_address.address1, self.sage_address.address_line_1)
#
#     def test_to_paperless_billing_address_sets_address2_to_bill_to_customer_address_address_line_2(self):
#         self.assertEqual(self.paperless_address.address2, self.sage_address.address_line_2)
#
#     def test_to_paperless_billing_address_sets_city_to_bill_to_customer_address_city(self):
#         self.assertEqual(self.paperless_address.city, self.sage_address.city)
#
#     def test_to_paperless_billing_address_sets_state_to_bill_to_customer_address_state(self):
#         self.assertEqual(self.paperless_address.state, self.sage_address.state)
#
#     def test_to_paperless_billing_address_sets_country_to_bill_to_customer_address_country(self):
#         self.assertEqual(self.paperless_address.country, self.sage_address.country)
#
#     def test_to_paperless_billing_address_sets_postal_code_to_bill_to_customer_address_zip_code(self):
#         self.assertEqual(self.paperless_address.postal_code, self.sage_address.zip_code)
#
#
#
