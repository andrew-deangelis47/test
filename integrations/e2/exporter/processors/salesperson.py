from paperless.custom_tables.custom_tables import CustomTable
from baseintegration.datamigration import logger

from paperless.objects.users import User


class SalespersonProcessor:

    def process_salesperson(self, order):
        sales_id = self.get_sales_id(order)
        return sales_id

    def get_sales_id(self, order):
        sales_id = None
        if order.salesperson is not None:
            salesperson_email = order.salesperson.email
            PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING = \
                self.get_paperless_parts_salesperson_email_to_e2_sales_id_mapping()
            sales_id = PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING.get(salesperson_email)
        return sales_id

    def get_paperless_parts_salesperson_email_to_e2_sales_id_mapping(self):
        PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING = {}
        user_list = User.list()

        # TODO: the following is temporary code to backfill the Paperless users with erp codes from custom table
        try:
            sales_id_mapping_table_details = CustomTable.get('sales_id_mapping')
            rows = sales_id_mapping_table_details['rows']
            for row in rows:
                PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING[row['paperless_parts_username']] = \
                    row['e2_sales_id']
                user_matches = list(filter(lambda user: (user.email == row['paperless_parts_username']),
                                           user_list))
                if len(user_matches) > 0:
                    user_to_backfill: User = user_matches[0]
                    user_to_backfill.erp_code = row['e2_sales_id']
                    user_to_backfill.update()
        except Exception as e:
            logger.error(f'Encountered an error fetching the sales ID mapping: {e}')
        # TODO: end of temporary code

        for user in user_list:
            PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING[user.email] = user.erp_code
        return PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_E2_SALES_ID_MAPPING
