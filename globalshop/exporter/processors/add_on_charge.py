import decimal

from addon import AddOn
from baseintegration.datamigration import logger
from globalshop.customer import CustomerRecord
from paperless.custom_tables.custom_tables import CustomTable
from paperless.objects.orders import Order, OrderedAddOn, OrderItem

from globalshop.exporter.processors import GSProcessor


class AddOnProcessor(GSProcessor):
    do_rollback = False

    def _process(self, add_on: OrderedAddOn, order: Order, order_item: OrderItem, line_number: int, customer_record: CustomerRecord):
        logger.info(f'Add On {add_on}')
        logger.info(f'Line Number {line_number}')

        erp_code = None
        account_id = None

        contact = order.contact
        account = contact.account
        if account:
            # account: Account = Account.get(account_id)
            erp_code = account.erp_code
            account_id = account.id
        part_number = order_item.filename
        gss_part_number = add_on.name
        ext_part_number = add_on.name
        qty_ordered = add_on.quantity
        line_total_price = decimal.Decimal(add_on.price.raw_amount)
        line_unit_price = decimal.Decimal(add_on.price.raw_amount)
        description = f'ENGINEERING {part_number}'
        ship_dates_match = True
        order_item_ships_on = None
        for orderitem in order.order_items:
            if order_item_ships_on is None:
                order_item_ships_on = orderitem.ships_on
            if order_item_ships_on != orderitem.ships_on:
                ship_dates_match = False

        if ship_dates_match:
            order_due_date = order.ships_on[:10]
        else:
            order_due_date = '1900-01-01'
        order_date = order.created[:10]
        line_order_date = order.created[:10]
        line_promise_date = order_item.ships_on

        shipping_info = order.shipping_info

        ship_to_address_1 = shipping_info.address1 if shipping_info else ''
        ship_to_address_2 = shipping_info.address2 if shipping_info else ''
        ship_to_city = shipping_info.city if shipping_info else ''
        ship_to_state = shipping_info.state if shipping_info else ''
        ship_to_zip = shipping_info.postal_code if shipping_info else ''
        ship_to_country = shipping_info.country if shipping_info else ''

        ship_to_contact_name = f"{contact.first_name} {contact.last_name}"
        ship_to_contact_email = contact.email
        ship_id = shipping_info.facility_name if shipping_info else None
        if ship_id is not None:
            ship_to_address_1 = None
            ship_to_address_2 = None
            ship_to_city = None
            ship_to_state = None
            ship_to_zip = None
            ship_to_country = None

        billing_info = order.billing_info

        bill_to_address_1 = billing_info.address1 if billing_info else ''
        bill_to_address_2 = billing_info.address2 if billing_info else ''
        bill_to_city = billing_info.city if billing_info else ''
        bill_to_state = billing_info.state if billing_info else ''
        bill_to_zip = billing_info.postal_code if billing_info else ''
        bill_to_country = billing_info.country if billing_info else ''

        customer_po = order.payment_details.purchase_order_number if order.payment_details.purchase_order_number else ''
        customer_part = ''
        part_um = 'EA'
        product_line = add_on.get_variable(self._exporter.erp_config.product_line_var)
        if product_line:
            product_line = product_line.value
        logger.info(f'product line - {product_line}')

        AddOn.insert(gss_customer_no=erp_code,
                     ext_customer_no=str(account_id),
                     line_number=line_number,
                     external_order_no=str(order.number),
                     gss_part_number=gss_part_number,
                     ext_part_number=ext_part_number,
                     qty_ordered=qty_ordered,
                     line_total_price=line_total_price,
                     line_unit_price=line_unit_price,
                     order_due_date=order_due_date,
                     order_date=order_date,
                     line_order_date=line_order_date,
                     line_promise_date=line_promise_date,
                     ship_to_id=ship_id,
                     ship_to_address_1=ship_to_address_1,
                     ship_to_address_2=ship_to_address_2,
                     ship_to_city=ship_to_city,
                     ship_to_state=ship_to_state,
                     ship_to_zip=ship_to_zip,
                     ship_to_country=ship_to_country,
                     ship_to_contact_email=ship_to_contact_email,
                     ship_to_contact_name=ship_to_contact_name,
                     bill_to_address_1=bill_to_address_1,
                     bill_to_address_2=bill_to_address_2,
                     bill_to_city=bill_to_city,
                     bill_to_zip=bill_to_zip,
                     bill_to_state=bill_to_state,
                     bill_to_country=bill_to_country,
                     customer_po=customer_po,
                     part_description=description,
                     customer_part=customer_part,
                     product_line=product_line,
                     part_um=part_um)
        logger.info("Additional Charge added to SO")

    def get_sales_id(self, order):
        sales_id = None
        if order.salesperson is not None:
            salesperson_email = order.salesperson.email
            PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_GSS_SALES_ID_MAPPING = \
                self.get_paperless_parts_salesperson_email_to_gss_sales_id_mapping()
            sales_id = PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_GSS_SALES_ID_MAPPING.get(salesperson_email)
        return sales_id

    def get_paperless_parts_salesperson_email_to_gss_sales_id_mapping(self):
        PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_GSS_SALES_ID_MAPPING = {}

        # TODO: the following is temporary code to backfill the Paperless users with erp codes from custom table
        try:
            sales_id_mapping_table_details = CustomTable.get('sales_id_mapping')
            rows = sales_id_mapping_table_details['rows']
            for row in rows:
                PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_GSS_SALES_ID_MAPPING[row['paperless_parts_username']] = \
                    row['gss_salesperson_id']
        except Exception as e:
            logger.error(f'Encountered an error fetching the sales ID mapping: {e}')
        return PAPERLESS_PARTS_SALESPERSON_EMAIL_TO_GSS_SALES_ID_MAPPING
