from plex_v2.factories.plex.customer_part import CustomerPartFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from plex_v2.objects.part import Part
from plex_v2.objects.customer import Customer


class TestCustomerPartFactory:

    VALID_PLEX_PART_ID = 'VALID_PLEX_PART_ID'
    VALID_PLEX_PART_NUMBER = 'VALID_PLEX_PART_NUMBER'
    VALID_PLEX_PART_REVISION = 'VALID_PLEX_PART_REVISION'
    VALID_PLEX_PART_DESCRIPTION = 'VALID_PLEX_PART_DESCRIPTION'
    VALID_PLEX_PART_NAME = 'VALID_PLEX_PART_NAME'

    VALID_PLEX_CUSTOMER_ID = 'VALID_PLEX_CUSTOMER_ID'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)

        self.utils = create_autospec(ExportUtils)

        self.factory = CustomerPartFactory(
            config=self.config,
            utils=self.utils
        )

        self.plex_part = create_autospec(Part)
        self.plex_part.id = self.VALID_PLEX_PART_ID
        self.plex_part.number = self.VALID_PLEX_PART_NUMBER
        self.plex_part.revision = self.VALID_PLEX_PART_REVISION
        self.plex_part.description = self.VALID_PLEX_PART_DESCRIPTION
        self.plex_part.name = self.VALID_PLEX_PART_NAME

        self.plex_customer = create_autospec(Customer)
        self.plex_customer.id = self.VALID_PLEX_CUSTOMER_ID

    def test_to_customer_part_sets_number_to_plex_part_number(self):
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.number == self.plex_part.number

    def test_to_customer_part_sets_partId_to_plex_part_id(self):
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.partId == self.plex_part.id

    def test_to_customer_part_sets_revision_to_plex_part_revision(self):
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.revision == self.plex_part.revision

    def test_to_customer_part_sets_customerId_to_id_of_assciated_customer(self):
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.customerId == self.plex_customer.id

    def test_to_customer_part_sets_description_to_plex_part_name_if_part_description_is_none(self):
        self.plex_part.description = None
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.description == self.plex_part.name

    def test_to_customer_part_sets_description_to_plex_part_description_if_part_name_is_none(self):
        self.plex_part.name = None
        customer_part = self.factory.to_customer_part(
            self.plex_part,
            self.plex_customer
        )

        assert customer_part.description == self.plex_part.description
