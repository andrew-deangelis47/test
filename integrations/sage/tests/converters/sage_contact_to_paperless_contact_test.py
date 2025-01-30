import unittest
from sage.models.sage_models.customer.contact import Contact
from sage.models.converters.sage_contact_to_paperless_contact_converter import SageContactToPaperlessContactConverter

"""
This test simply tests that the converter sets each property of the model
"""


class TestSageContactToPaperlessContactConverter(unittest.TestCase):

    # test constants
    ACCOUNT_ID = 123
    sage_contact = None
    paperless_contact = None

    def setUp(self) -> None:
        self.sage_contact = Contact
        self.sage_contact.first_name = 'first_name'
        self.sage_contact.last_name = 'last_name'
        self.sage_contact.email = 'email'
        self.paperless_contact = SageContactToPaperlessContactConverter.to_paperless_contact(self.sage_contact, self.ACCOUNT_ID)

    def test_to_paperless_contact_sets_account_id(self):
        self.assertEqual(self.paperless_contact.account_id, self.ACCOUNT_ID)

    def test_to_paperless_contact_sets_email(self):
        self.assertEqual(self.paperless_contact.email, self.sage_contact.email)

    def test_to_paperless_contact_sets_first_name(self):
        self.assertEqual(self.paperless_contact.first_name, self.sage_contact.first_name)

    def test_to_paperless_contact_sets_last_name(self):
        self.assertEqual(self.paperless_contact.last_name, self.sage_contact.last_name)
