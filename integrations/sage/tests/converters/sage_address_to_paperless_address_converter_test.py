# from sage.converters.sage_address_to_paperless_address_converter imports SageAddressToPaperlessAddressConverter
# from sage.sage_models imports Address as SageAddress
# imports unittest
#
# TODO: fix this test, something is going wonky with the AddressUtils.get_country_and_state function during tests

#
# class TestSageAddressToPaperlessAddressConverter(unittest.TestCase):
#
#     # test constants
#     sage_address = None
#     paperless_address = None
#
#     def setUp(self) -> None:
#         self.sage_address = SageAddress
#         self.sage_address.address_line_1 = 'address_line_1'
#         self.sage_address.address_line_2 = 'address_line_2'
#         self.sage_address.city = 'city'
#         self.sage_address.state = 'state'
#         self.sage_address.country = 'US'
#         self.sage_address.zip_code = 'zip_code'
#         self.paperless_address = SageAddressToPaperlessAddressConverter.to_paperless_address(self.sage_address, 'cust_code')
#
#     def test_to_paperless_address_sets_sage_address1_paperless_address_address_line_1(self):
#         self.assertEqual(self.paperless_address.address1, self.sage_address.address_line_1)
#
#     def test_to_paperless_address_sets_sage_address2_to_paperless_address_address_line_2(self):
#         self.assertEqual(self.paperless_address.address2, self.sage_address.address_line_2)
#
#     def test_to_paperless_address_sets_city_to_paperless_address_city(self):
#         self.assertEqual(self.paperless_address.city, self.sage_address.city)
#
#     def test_to_paperless_address_sets_sage_state_to_paperless_address_state(self):
#         self.assertEqual(self.paperless_address.state, self.sage_address.state)
#
#     def test_to_paperless_address_sets_sage_country_to_paperless_address_country(self):
#         self.assertEqual(self.paperless_address.country, self.sage_address.country)
#
#     def test_to_paperless_address_sets_sage_postal_code_to_paperless_address_zip_code(self):
#         self.assertEqual(self.paperless_address.postal_code, self.sage_address.zip_code)
