import datetime
from baseintegration.utils import safe_get
import jobboss.models as jb
from baseintegration.datamigration import logger
from . import JobBossProcessor
from paperless.objects.users import User
from paperless.custom_tables.custom_tables import CustomTable
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
PP_TO_JB_ESTIMATOR_MAPPING = None
from django.utils.timezone import make_aware


class SoHeaderProcessor(JobBossProcessor):
    def get_payment_details(self, order: Order, customer):
        terms = None
        if order.payment_details.payment_terms is not None:
            terms = order.payment_details.payment_terms.upper() \
                if order.payment_details.payment_type == 'purchase_order' \
                else 'Credit Card'
            if order.payment_details.payment_type == 'purchase_order' and \
                    customer.terms:
                terms = customer.terms
        return terms

    def get_notes(self, order: Order):
        notes = 'PP Quote #{}'.format(order.quote_number)
        if order.private_notes:
            notes += '\n{}'.format(order.private_notes)
        return notes

    def create_comments(self):
        ship_str = None
        # ship_str = order.shipping_option.summary(
        #     order.ships_on_dt, order.payment_details.payment_type) if order.shipping_option is not None else None
        return ship_str

    def get_estimator_name_from_custom_table_mapping(self):
        """
        Gets estimator mapping from custom table.
        """
        estim_mapping_table_name = self._exporter.erp_config.estimator_mapping_table_name
        estim_email = self._exporter.erp_config.estimator_email_column_name
        estim_jb_id = self._exporter.erp_config.estimator_jb_id_column_name
        if self.pp_to_jb_estimator_mapping is None:
            self.pp_to_jb_estimator_mapping = {}
            user_list = User.list()

            # TODO: the following is temporary code to backfill the Paperless users with erp codes from custom table
            try:
                estimator_mapping_table = CustomTable.get(estim_mapping_table_name)
                rows = estimator_mapping_table['rows']
                for row in rows:
                    self.pp_to_jb_estimator_mapping[row[estim_email].lower()] = row[estim_jb_id]
                    user_matches = list(filter(lambda user: (user.email.lower() == row[estim_email].lower()),
                                               user_list))
                    if len(user_matches) > 0:
                        user_to_backfill: User = user_matches[0]
                        user_to_backfill.erp_code = row[estim_jb_id]
                        user_to_backfill.update()
                logger.info(f"Successfully created estimator mapping from table: {estim_mapping_table_name}.")
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
            # TODO: end of temporary code

            for user in user_list:
                self.pp_to_jb_estimator_mapping[user.email.lower()] = user.erp_code
        return self.pp_to_jb_estimator_mapping

    @staticmethod
    def get_estimator_name(default_estimator, estimator, pp_to_jb_estimator_mapping):
        """
        "order_taken_by" must be an exact match for an Employee record id in JB, else it will cause a "Record Not Found"
        error in JobBOSS. The order_taken_by field can be "None" on the sales order for full functionality.
        """
        order_taken_by = jb.Employee.objects.filter(employee=default_estimator).last().employee
        if pp_to_jb_estimator_mapping:
            email = estimator.email.lower() if estimator is not None else None
            order_taken_by = pp_to_jb_estimator_mapping.get(email, order_taken_by)
        return order_taken_by

    def _process(self, order, customer, ship_to, contact):
        self.pp_to_jb_estimator_mapping = None

        if self._exporter.erp_config.should_update_quote_line_status and order.quote_erp_code:
            self.update_quote_line_status(order=order, rfq_number=order.quote_erp_code)

        if not self._exporter.erp_config.sales_orders_active:
            logger.info('Sales Orders are disabled.')
            return None

        # Get estimator mapping from custom table and set estim_name using first letter + last name convention
        estim_name = None
        if self._exporter.erp_config.enable_estimator_mapping:
            self.get_estimator_name_from_custom_table_mapping()
            estim_name = self.get_estimator_name(self._exporter.erp_config.default_estimator, order.estimator, self.pp_to_jb_estimator_mapping)

        now = make_aware(datetime.datetime.utcnow())
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        terms = self.get_payment_details(order, customer)
        notes = self.get_notes(order)
        comments = self.create_comments()
        status = self._exporter.erp_config.sales_order_default_status

        so_header = jb.SoHeader(
            customer=customer.customer,
            ship_to=safe_get(ship_to, 'address'),  # Usually filled in (jobboss Address ID)
            contact=contact.contact,  # Optional field
            order_taken_by=estim_name,  # Estim name must be "None" or match JobBOSS's convention (see above)
            ship_via=customer.ship_via,
            terms=terms[:15] if terms is not None else "Net 30 days",
            sales_tax_amt=0,
            sales_tax_rate=0,
            order_date=today,
            promised_date=order.ships_on_dt,
            customer_po=order.payment_details.purchase_order_number,
            status=status,
            total_price=order.payment_details.total_price.dollars,
            currency_conv_rate=1,
            trade_currency=1,
            fixed_rate=1,
            trade_date=today,
            note_text=notes,
            comment=comments,
            last_updated=now,
            source='System',
            prepaid_tax_amount=0,
            sales_rep=customer.sales_rep,
        )
        try:
            so_header.save_with_autonumber()
            logger.info(f'Created sales order {so_header.sales_order}')

        except Exception as e:
            logger.error(f"Failed to save SoHeader {so_header.sales_order}. [ERROR] - {e}")
            logger.error(so_header.__dict__)

        return so_header

    def update_quote_line_status(self, order: Order, rfq_number: str):
        if order.quote_erp_code is None:
            return
        try:
            rfq = jb.Rfq.objects.get(rfq=rfq_number)
            quote = Quote.get(id=order.quote_number, revision=order.quote_revision_number)
            for item in order.order_items:
                # TODO: handle cases where the same item is on the quote twice, could use position/line-number but need
                #  to consider addons, for now do a simple lookup for the quote line item via part number, mark it as won
                quote_item = next(filter(lambda x: x.id == item.quote_item_id, quote.quote_items))
                jb_quote = jb.Quote.objects.filter(part_number=quote_item.root_component.part_number,
                                                   rfq=rfq.rfq).first()
                jb_quote.status = 'Won'
                jb_quote.save()
                logger.info(f'Jobboss quote item to update - {jb_quote}')
        except:
            return
