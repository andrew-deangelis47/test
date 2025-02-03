from typing import Any, Optional

from paperless.custom_tables.custom_tables import CustomTable
from baseintegration.datamigration import logger
from mietrak_pro.exporter.processors import MietrakProProcessor
from paperless.objects.customers import Account
from paperless.objects.orders import Order
from paperless.objects.users import User

from mietrak_pro.query.salesperson import get_party_salesperson_for_customer_by_salesperson, \
    get_salesperson_by_id, create_party_salesperson, get_order_salesperson_for_order_by_salesperson, \
    create_order_salesperson
from mietrak_pro.models import Party, Salesorder, Partysalesperson


class SalespersonProcessor(MietrakProProcessor):

    def _process(self, paperless_parts_entity: Any, mietrak_pro_entity: Any):
        raise NotImplementedError()

    def get_salesperson(self, salesperson_id):
        return get_salesperson_by_id(salesperson_id)

    def get_order_salesperson_id(self, order):
        salesperson_id = None
        if order.salesperson is not None:
            salesperson_email = order.salesperson.email
            salesperson_id = self.get_salesperson_id(salesperson_email)
        return salesperson_id

    def get_account_salesperson_id(self, account: Optional[Account]):
        salesperson_id = None
        if account is not None and account.salesperson is not None:
            salesperson_email = account.salesperson.email
            salesperson_id = self.get_salesperson_id(salesperson_email)
        return salesperson_id

    def get_salesperson_id(self, salesperson_email):
        PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING = \
            self.get_paperless_parts_salesperson_email_to_mietrak_pro_sales_id_mapping()
        salesperson_id = PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING.get(salesperson_email)
        return salesperson_id

    def get_paperless_parts_salesperson_email_to_mietrak_pro_sales_id_mapping(self):
        PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING = {}
        user_list = User.list()

        # TODO: the following is temporary code to backfill the Paperless users with erp codes from custom table
        try:
            if not self._exporter._integration.test_mode:
                table_name = 'sales_id_mapping'
            else:
                table_name = 'mietrak_sales_id_mapping'
            sales_id_mapping_table_details = CustomTable.get(table_name)
            rows = sales_id_mapping_table_details['rows']
            for row in rows:
                PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING[row['paperless_parts_username']] = \
                    row['mietrak_pro_salesperson_party_id']
                user_matches = list(filter(lambda user: (user.email == row['paperless_parts_username']),
                                           user_list))
                if len(user_matches) > 0:
                    user_to_backfill: User = user_matches[0]
                    user_to_backfill.erp_code = row['mietrak_pro_salesperson_party_id']
                    user_to_backfill.update()
        except Exception as e:
            logger.error(f'Encountered an error fetching the sales ID mapping: {e}')
        # TODO: end of temporary code

        for user in user_list:
            PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING[user.email] = user.erp_code
        return PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_MIETRAK_PRO_SALES_ID_MAPPING


class PartySalespersonProcessor(SalespersonProcessor):

    def _process(self, account: Optional[Account], customer: Party):
        party_salesperson = None

        account_salesperson_id = self.get_account_salesperson_id(account)
        if account_salesperson_id is not None:
            party_salesperson, is_party_salesperson_new = self.get_or_create_party_salesperson(customer,
                                                                                               account_salesperson_id)
        else:
            logger.info("account_salesperson_id is None")

        return party_salesperson

    def get_or_create_party_salesperson(self, customer: Party, salesperson_id: int):
        salesperson = get_salesperson_by_id(salesperson_id)
        if salesperson is None:
            logger.info(
                f'Could not find Salesperson with ID: {salesperson_id} - not assigning salesperson for this customer')
            # TODO - should this assign to a default salesperson record instead of failing silently?
            # TODO - it's better to let the user know that something went wrong
            return None, False

        party_salesperson = get_party_salesperson_for_customer_by_salesperson(customer, salesperson)
        is_party_salesperson_new = False

        if party_salesperson is not None:
            logger.info(
                f'Found existing Salesperson record with name {salesperson.name} assigned to customer {customer.name}')
        else:
            logger.info(
                f'No PartySalesperson record found with name {salesperson.name} assigned to customer {customer.name} - creating a salesperson')
            party_salesperson = create_party_salesperson(customer, salesperson)
            is_party_salesperson_new = True

        return party_salesperson, is_party_salesperson_new


class OrderSalespersonProcessor(SalespersonProcessor):

    def _process(self, order: Order, sales_order: Salesorder):
        order_salesperson = None

        if self._exporter.erp_config.should_use_mietrak_salesperson:
            logger.info('Use the default mietrak salesperson...')
            salespersonpk = sales_order.customerfk.partypk
            salespeople = Partysalesperson.objects.filter(partyfk=salespersonpk)
            for salesperson in salespeople:
                party = Party.objects.get(partypk=salesperson.salespersonfk_id)
                create_order_salesperson(sales_order, party, salesperson)
            return

        order_salesperson_id = self.get_order_salesperson_id(order)
        if order_salesperson_id is not None:
            order_salesperson, is_order_salesperson_new = self.get_or_create_order_salesperson(sales_order,
                                                                                               order_salesperson_id)

        return order_salesperson

    def get_or_create_order_salesperson(self, sales_order: Salesorder, salesperson_id: int):
        salesperson = get_salesperson_by_id(salesperson_id) if salesperson_id else None
        if salesperson is None:
            logger.info(
                f'Could not find Salesperson with ID: {salesperson_id} - not assigning salesperson for this sales order')
            # TODO - should this assign to a default salesperson record instead of failing silently?
            # TODO - it's better to let the user know that something went wrong
            return None, False

        order_salesperson = get_order_salesperson_for_order_by_salesperson(sales_order, salesperson)
        is_order_salesperson_new = False

        if order_salesperson is not None:
            logger.info(
                f'Found existing Salesperson record with name {salesperson.name} assigned to sales_order {sales_order.salesordernumber}')
        else:
            logger.info(
                f'No PartySalesperson record found with name {salesperson.name} assigned to sales_order {sales_order.salesordernumber} - creating a salesperson')
            order_salesperson = create_order_salesperson(sales_order, salesperson)
            is_order_salesperson_new = True

        return order_salesperson, is_order_salesperson_new
