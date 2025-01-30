from unittest import TestCase


from baseintegration.integration.integration_export_report import IntegrationExportReport
from baseintegration.integration import Integration
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote

COLUMN_NAME_EXPORT_ID = 'export_id'
COLUMN_NAME_ORDER_NUM = 'order_num'
COLUMN_NAME_QUOTE_NUM = 'quote_num'
COLUMN_NAME_QUOTE_REV = 'quote_rev'
KEY_INTEGRATION_REPORT_COLUMNS_CONFIG = 'integration_report_columns'
CUSTOM_TABLE_COLUMNS_CONFIG = ['test1', 'test2', 'test3']
KEY_REPORT_ROW_LIMIT_CONFIG = 'integration_report_row_limit'
REPORT_ROW_LIMIT_CONFIG = 5
KEY_REPORT_ROW_REMOVE_COUNT = 'integration_report_clear_count'
REPORT_ROW_REMOVE_COUNT = 1


class TestIntegrationExportReport(TestCase):

    def _setup_with_quote(self) -> None:
        int = Integration()
        int.config_yaml[KEY_INTEGRATION_REPORT_COLUMNS_CONFIG] = CUSTOM_TABLE_COLUMNS_CONFIG
        int.config_yaml[KEY_REPORT_ROW_LIMIT_CONFIG] = REPORT_ROW_LIMIT_CONFIG
        int.config_yaml[KEY_REPORT_ROW_REMOVE_COUNT] = REPORT_ROW_REMOVE_COUNT
        quote = Quote.get(1)
        self.report = IntegrationExportReport(int, quote, True)

    def _setup_with_order(self) -> None:
        int = Integration()
        int.config_yaml[KEY_INTEGRATION_REPORT_COLUMNS_CONFIG] = CUSTOM_TABLE_COLUMNS_CONFIG
        int.config_yaml[KEY_REPORT_ROW_LIMIT_CONFIG] = REPORT_ROW_LIMIT_CONFIG
        int.config_yaml[KEY_REPORT_ROW_REMOVE_COUNT] = REPORT_ROW_REMOVE_COUNT
        order = Order.get(1)
        self.report = IntegrationExportReport(int, order, True)

    def test_report_object_has_mandatory_columns_as_properties_for_quote(self):
        """
        testing mandatory columns are set in report object
        """
        self._setup_with_quote()

        self.assertIsNotNone(self.report.export_id)
        self.assertIsNotNone(self.report.quote_num)
        self.assertIsNotNone(self.report.quote_revision)

    def test_report_object_has_mandatory_columns_as_properties_for_order(self):
        """
        testing mandatory columns are set in report object
        """

        self._setup_with_order()

        self.assertIsNotNone(self.report.export_id)
        self.assertIsNotNone(self.report.order_num)

    def test_report_object_has_mandatory_columns_in_dict_for_quote(self):
        """
        testing mandatory columns are set in report object's dictionary representation of
        the custom table
        """

        self._setup_with_quote()

        # grabbing the column names in the report object's dict
        columns_in_dict = self.report._to_dict().keys()

        self.assertTrue(COLUMN_NAME_EXPORT_ID in columns_in_dict)
        self.assertTrue(COLUMN_NAME_QUOTE_NUM in columns_in_dict)
        self.assertTrue(COLUMN_NAME_QUOTE_REV in columns_in_dict)

    def test_report_object_has_mandatory_columns_in_dict_for_order(self):
        """
        testing mandatory columns are set in report object's dictionary representation of
        the custom table
        """

        self._setup_with_order()

        # grabbing the column names in the report object's dict
        columns_in_dict = self.report._to_dict().keys()

        self.assertTrue(COLUMN_NAME_EXPORT_ID in columns_in_dict)
        self.assertTrue(COLUMN_NAME_ORDER_NUM in columns_in_dict)

    def test_report_object_has_configured_columns_in_dict_for_quote(self):
        """
        testing configured columns are set in report object's dictionary representation of
        the custom table
        """

        self._setup_with_quote()

        # grabbing the column names in the report object's dict
        columns_in_dict = self.report._to_dict().keys()

        for configured_column_name in CUSTOM_TABLE_COLUMNS_CONFIG:
            self.assertTrue(configured_column_name in columns_in_dict)

    def test_report_object_has_configured_columns_in_dict_for_order(self):
        """
        testing configured columns are set in report object's dictionary representation of
        the custom table
        """

        self._setup_with_order()

        # grabbing the column names in the report object's dict
        columns_in_dict = self.report._to_dict().keys()

        for configured_column_name in CUSTOM_TABLE_COLUMNS_CONFIG:
            self.assertTrue(configured_column_name in columns_in_dict)

    def test_custom_table_has_all_mandatory_properties_for_quote(self):
        self._setup_with_quote()

        custom_table = self.report.custom_table

        # check the mandatory properties, will fail if the property does not exist
        custom_table.__getattribute__(COLUMN_NAME_EXPORT_ID)
        custom_table.__getattribute__(COLUMN_NAME_QUOTE_NUM)
        custom_table.__getattribute__(COLUMN_NAME_QUOTE_REV)

    def test_custom_table_has_all_mandatory_properties_for_order(self):
        self._setup_with_order()

        custom_table = self.report.custom_table

        # check the mandatory properties, will fail if the property does not exist
        custom_table.__getattribute__(COLUMN_NAME_EXPORT_ID)
        custom_table.__getattribute__(COLUMN_NAME_ORDER_NUM)

    def test_custom_table_has_all_configured_properties_for_quote(self):
        self._setup_with_quote()

        custom_table = self.report.custom_table

        # check the mandatory properties, will fail if the property does not exist
        for configured_column_name in CUSTOM_TABLE_COLUMNS_CONFIG:
            custom_table.__getattribute__(configured_column_name)

    def test_custom_table_has_all_configured_properties_for_order(self):
        self._setup_with_order()

        custom_table = self.report.custom_table

        # check the mandatory properties, will fail if the property does not exist
        for configured_column_name in CUSTOM_TABLE_COLUMNS_CONFIG:
            custom_table.__getattribute__(configured_column_name)
