from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.utils.custom_table import HexImportCustomTable
from m1.importer.processors.accounts import AccountImportProcessor
from django.db import connection
from m1.models import Organizations


class M1AccountListener:
    identifier = "account_import"

    def __init__(self, integration):
        self._integration = integration

    def get_new(self, bulk=False):
        logger.info("Processing: Accounts")
        cursor = connection.cursor()
        try:
            last_processed_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(self.identifier)

            account_query = f"SELECT o.cmoorganizationid, " \
                            f"(SELECT MAX(rev_number) " \
                            f"FROM(VALUES(o.cmorowversion), (oc.cmcrowversion), (ol.cmlrowversion)) " \
                            f"AS UpdateDate(rev_number)) " \
                            f"AS rev_number " \
                            f"FROM Organizations as o " \
                            f"LEFT JOIN OrganizationContacts as oc ON o.cmoorganizationid = oc.cmcorganizationid " \
                            f"LEFT JOIN OrganizationLocations as ol ON o.cmoorganizationid = ol.cmlorganizationid " \
                            f"WHERE o.cmocustomerstatus = 2 " \
                            f"AND(o.cmorowversion > {last_processed_hex_counter} " \
                            f"OR oc.cmcrowversion > {last_processed_hex_counter} " \
                            f"OR ol.cmlrowversion > {last_processed_hex_counter}) " \
                            f"ORDER BY rev_number ASC"
            cursor.execute(account_query)
            account_query_set = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        p_list = []
        for item in account_query_set:
            p_list.append(item[0])
            last_processed_hex_counter = f'0x{item[1].hex()}'
        final_ordered_list = list(dict.fromkeys(p_list))
        logger.info(f'Accounts to update {len(final_ordered_list)}')
        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, last_processed_hex_counter)
        return final_ordered_list


class M1AccountImporter(AccountImporter):
    """An integration config specific to m1"""

    def _setup_erp_config(self):
        pass

    def _register_default_processors(self):
        self.register_processor(Organizations, AccountImportProcessor)

    def _register_listener(self):
        self.listener = M1AccountListener(self._integration)

    def _process_account(self, account_id: str):
        logger.info(f"Processing Account: {str(account_id)}")
        with self.process_resource(Organizations, account_id) as success:
            logger.info(f"Processed Account: {str(account_id)}")
            return success
