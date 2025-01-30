# from unittest import TestCase
# from sage.soap_api_processing import SageXmlParser
#
#
# class TestSageXmlParser(TestCase):
#
#     IMPORT_SUCCESS_TEST_DATA_FILE = 'data/xml_parser_test_success_import_response.xml'
#     raw_xml_payload = None
#
#     def setUp(self) -> None:
#         xml_file = open(self.IMPORT_SUCCESS_TEST_DATA_FILE, "r")
#         self.raw_payload = xml_file.read()
#         xml_file.close()
#
#     def test_get_import_o_file_payload(self):
#         SageXmlParser.get_import_o_file_payload(self.raw_payload)
#
#
