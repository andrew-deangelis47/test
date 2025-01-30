from unittest import TestCase
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter, ErrorMessageMapping
from typing import List

ERP_ERROR_MESSAGE_0 = 'ERP_ERROR_MESSAGE_0'
PAPERLESS_ERROR_0 = 'PAPERLESS_ERROR_0'
ERP_ERROR_MESSAGE_1 = 'ERP_ERROR_MESSAGE_1'
PAPERLESS_ERROR_1 = 'PAPERLESS_ERROR_1'
ERP_ERROR_MESSAGE_2 = 'ERP_ERROR_MESSAGE_2'
PAPERLESS_ERROR_2 = 'PAPERLESS_ERROR_2'

UNRECOGNIZED_ERP_ERROR = 'UNRECOGNIZED_ERP_ERROR'


class TestErpMessageConverter(TestCase):

    def setUp(self) -> None:
        dictionary = {
            ERP_ERROR_MESSAGE_0: PAPERLESS_ERROR_0,
            ERP_ERROR_MESSAGE_1: PAPERLESS_ERROR_1,
            ERP_ERROR_MESSAGE_2: PAPERLESS_ERROR_2
        }

        self.converter: ERPErrorMessageConverter = ERPErrorMessageConverter(dictionary)

    def test_mappings_contain_erp_error_message_from_dict_keys(self):
        """
        testing that the keys in the dictionary that is passed to the constructor end up as the erp error messages
        in the ErrorMessageMapping objects
        """

        mappings: List[ErrorMessageMapping] = self.converter.mappings
        self.assertEqual(mappings[0].erp_error_message, ERP_ERROR_MESSAGE_0)
        self.assertEqual(mappings[1].erp_error_message, ERP_ERROR_MESSAGE_1)
        self.assertEqual(mappings[2].erp_error_message, ERP_ERROR_MESSAGE_2)

    def test_mappings_contain_paperless_message_from_dict_key_values(self):
        """
        testing that the keys in the dictionary that is passed to the constructor end up as the erp error messages
        in the ErrorMessageMapping objects
        """

        mappings: List[ErrorMessageMapping] = self.converter.mappings
        self.assertEqual(mappings[0].paperless_error_message, PAPERLESS_ERROR_0)
        self.assertEqual(mappings[1].paperless_error_message, PAPERLESS_ERROR_1)
        self.assertEqual(mappings[2].paperless_error_message, PAPERLESS_ERROR_2)

    def test_get_clean_message_returns_corresponding_message_if_exists(self):
        """
        testing that if we have the error message in the dict then we get the right paperless message
        """
        corresponding_paperless_message = self.converter.get_clean_message(ERP_ERROR_MESSAGE_0)
        self.assertEqual(corresponding_paperless_message, PAPERLESS_ERROR_0)

    def test_get_clean_message_returns_none_if_message_isnt_in_dict(self):
        """
        testing that if we have the error message in the dict then we get the right paperless message
        """
        corresponding_paperless_message = self.converter.get_clean_message(UNRECOGNIZED_ERP_ERROR)
        self.assertIsNone(corresponding_paperless_message)


class TestErrorMessageMapping(TestCase):

    def setUp(self) -> None:
        self.mapping: ErrorMessageMapping = ErrorMessageMapping(ERP_ERROR_MESSAGE_0, PAPERLESS_ERROR_0)

    def test_error_message_matches_returns_true_if_error_in_parameter_matches_erp_error_in_object(self):
        self.assertTrue(self.mapping.error_message_matches(ERP_ERROR_MESSAGE_0))

    def test_error_message_matches_returns_false_if_error_in_parameter_does_not_match_erp_error_in_object(self):
        self.assertFalse(self.mapping.error_message_matches(ERP_ERROR_MESSAGE_1))
