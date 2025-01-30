from plex_v2.factories.base import BaseFactory
from plex_v2.objects.payment_terms_mapping import PaymentTermsMapping, PaymentTermsMappingList
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from typing import List
from plex_v2.configuration import PlexConfig
from plex_v2.utils.import_utils import ImportUtils


class PaymentTermsMappingFactory(BaseFactory):
    """
    mapping payment terms to payment terms period for account creation
    """

    COLUMN_PAYMENT_TERMS = 'payment_terms'
    COLUMN_PAYMENT_TERMS_PERIOD = 'payment_terms_period'

    config: PlexConfig
    utils: ImportUtils

    def __init__(self, config: PlexConfig, utils: ImportUtils):
        self.config = config
        self.utils = utils

    def _to_payment_terms(self, custom_table_row: dict) -> PaymentTermsMapping:
        if self.COLUMN_PAYMENT_TERMS not in custom_table_row.keys():
            raise CancelledIntegrationActionException(f'Please ensure the "{self.COLUMN_PAYMENT_TERMS}" exists in the {self.config.payment_mapping_custom_table_name} custom table')
        if self.COLUMN_PAYMENT_TERMS_PERIOD not in custom_table_row.keys():
            raise CancelledIntegrationActionException(f'Please ensure the "{self.COLUMN_PAYMENT_TERMS_PERIOD}" exists in the {self.config.payment_mapping_custom_table_name} custom table')

        return PaymentTermsMapping(
            payment_terms=custom_table_row[self.COLUMN_PAYMENT_TERMS],
            payment_terms_period=custom_table_row[self.COLUMN_PAYMENT_TERMS_PERIOD]
        )

    def get_payment_terms_mapping_list(self):
        payment_terms_mapping_list: List[PaymentTermsMappingList] = []
        custom_table_rows: List[dict] = self.utils.get_custom_table_rows(self.config.payment_mapping_custom_table_name)
        custom_table_row: dict
        for custom_table_row in custom_table_rows:
            payment_terms_mapping_list.append(self._to_payment_terms(custom_table_row))

        return PaymentTermsMappingList(payment_terms_mapping_list)
