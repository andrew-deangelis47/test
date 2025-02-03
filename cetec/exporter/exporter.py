from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from baseintegration.utils import safe_get
from cetec.utils import get_paperless_parts_operation_to_cetec_ordline_status_mapping, assemble_raw_material_json, \
    assemble_routing_data_for_component, assemble_placeholder_raw_material_json, \
    PAPERLESS_SHIPPING_TO_CETEC_SHPCDE_MAPPING, PAPERLESS_PAYMENT_TERMS_TO_CETEC_PAYMENT_TERMS_MAPPING
from cetec.exporter.config import CetecConfig
from baseintegration.datamigration import logger
import json
import requests
import time
import urllib
import random
from datetime import datetime, timedelta


class CetecOrderExporter(OrderExporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.erp_config = CetecConfig(
                url=self._integration.secrets["Cetec"]["url"],
                preshared_token=self._integration.secrets["Cetec"]["preshared_token"],
                import_source_name=self._integration.config_yaml["Cetec"]["import_source_name"],
                internal_customer_id=self._integration.config_yaml["Cetec"]["internal_customer_id"],
                internal_vendor_id=self._integration.config_yaml["Cetec"]["internal_vendor_id"],
                place_order=self._integration.config_yaml["Cetec"].get("place_order", True),
                default_trans_code=self._integration.config_yaml["Cetec"].get("default_trans_code", "SN"),
                default_work_center=self._integration.config_yaml["Cetec"].get("default_work_center", None)
            )
        else:
            self.erp_config = CetecConfig(
                url="https://testapi.com",
                default_trans_code="SN",
                default_work_center="test"
            )

    def _process_order(self, order: Order) -> bool:
        global PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING
        PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING = \
            get_paperless_parts_operation_to_cetec_ordline_status_mapping()

        url = self.erp_config.url
        preshared_token = self.erp_config.preshared_token
        import_source_name = self.erp_config.import_source_name

        logger.info('Processing order {}'.format(order.number))
        cetec_order_json = self.convert_paperless_order_to_cetec_order_json(order)

        headers = {
            'Content-Type': 'application/json'
        }

        # Create a BOM for each order item
        part_revision_definition_url = url + '/api/partrevisiondefinition'
        part_revision_definition_json = self.assemble_part_revision_definition_json(order)
        for order_item_bom_json in part_revision_definition_json:
            headers = {**headers, 'Version': '2.0'}
            order_item_bom_json['preshared_token'] = preshared_token
            print(json.dumps(order_item_bom_json))
            # We need to add retry logic because the Cetec API has been failing randomly, though infrequently
            # success = r.json().get('success', 0)
            success = 0
            for i in range(10):  # Retry a maximum of 10 times
                r = requests.post(part_revision_definition_url, headers=headers, json=order_item_bom_json, verify=False)
                status_code = r.status_code
                success = (status_code == 200)
                logger.info(f'Request success: {success}')
                if success:
                    logger.info(f"Request body is {r.text}")
                    break
                time.sleep(30)

        # Import the order
        request_params = {
            'preshared_token': preshared_token,
            'import_source_name': import_source_name,
        }
        encoded_params = urllib.parse.urlencode(request_params, quote_via=urllib.parse.quote)
        import_order_url = url + '/importjson/quotes'
        r = requests.post(import_order_url, params=encoded_params, headers=headers, json=cetec_order_json, verify=False)
        logger.info(f'Request URL: {r.request.url}')
        logger.info(f'Request JSON payload: {json.dumps(cetec_order_json)}')
        logger.info(f'Response status code: {r.status_code}')
        logger.info(f'Response content: {r.content}')
        # We need to add retry logic because the Cetec API has been failing randomly, though infrequently
        # success = r.json().get('success', 0)
        success = 0
        for i in range(10):  # Retry a maximum of 10 times
            r = requests.post(import_order_url, params=encoded_params, headers=headers, json=cetec_order_json, verify=False)
            success = r.json().get('success', 0)
            logger.info(f'Request success: {success}')
            if success:
                break
            time.sleep(30)
        try:
            self.success_message = f"Associated Cetec quote number is {r.json()['quotes'][0]}"
        except Exception:
            pass
        self.send_email(subject="New Cetec quote number generated from Paperless", body=f"Paperless order {order.number} has been moved into Cetec. {self.success_message}")

    def convert_paperless_order_to_cetec_order_json(self, order: Order):  # noqa: C901
        # Top level order data

        if not self._integration.test_mode:
            external_key = str(order.number) + str(random.randint(1, 1000))
        else:
            external_key = '53333'
        location = 'MN'

        # Customer, billing and shipping
        contact = order.contact
        if contact is not None:
            customer_name = contact.account.name if contact.account is not None else 'NO CUSTOMER ASSIGNED'
            customer_custnum = safe_get(contact, 'account.erp_code')
        else:
            customer_name = 'NO CUSTOMER ASSIGNED'
            customer_custnum = None
        logger.debug(f'customer_name is: {customer_name}')
        logger.debug(f'customer_id is: {customer_custnum}')

        billing_info = order.billing_info
        if billing_info is not None:
            billto_name = billing_info.attention
            billto_address_1 = billing_info.address1
            billto_address_2 = billing_info.address2
            billto_city = billing_info.city
            billto_state = billing_info.state
            billto_zip = billing_info.postal_code
        else:
            billto_name = ''
            billto_address_1 = ''
            billto_address_2 = ''
            billto_city = ''
            billto_state = ''
            billto_zip = ''

        shipping_info = order.shipping_info
        if shipping_info is not None:
            shipto_name = shipping_info.attention
            shipto_address_1 = shipping_info.address1
            shipto_address_2 = shipping_info.address2
            shipto_city = shipping_info.city
            shipto_state = shipping_info.state
            shipto_zip = shipping_info.postal_code
        else:
            shipto_name = ''
            shipto_address_1 = ''
            shipto_address_2 = ''
            shipto_city = ''
            shipto_state = ''
            shipto_zip = ''

        # Information about the carrier: UPS, Fedex, pickup, etc
        customers_carrier = order.shipping_option.customers_carrier if order.shipping_option is not None else ''  # One of ('ups', 'fedex')
        shipping_method = order.shipping_option.shipping_method if order.shipping_option is not None else ''  # One of ('early_am_overnight', 'next_day_air', 'second_day_air', 'ground')
        shipping_type = order.shipping_option.type if order.shipping_option is not None else ''  # One of ('pickup', 'customers_shipping_account', 'suppliers_shipping_account')
        if shipping_type == 'pickup':
            ship_via = PAPERLESS_SHIPPING_TO_CETEC_SHPCDE_MAPPING.get('pickup')
            shipping_instructions = ''
        else:
            if shipping_type == 'suppliers_shipping_account':
                customers_carrier = 'ups'
            ship_key = f'{customers_carrier}_{shipping_method}'
            ship_via = PAPERLESS_SHIPPING_TO_CETEC_SHPCDE_MAPPING.get(
                ship_key)
            shipping_instructions = ''
        if ship_via is None:
            ship_via = PAPERLESS_SHIPPING_TO_CETEC_SHPCDE_MAPPING.get('pickup')
        logger.info(f"Ship via is {ship_via}")

        # Look at the operation notes for any LOGISTICS | Shipping operations to see if this requires local delivery
        for order_item in order.order_items:
            for operation in order_item.root_component.shop_operations:
                if operation.notes is not None and operation.notes.startswith('Local Delivery |'):
                    ship_via = PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING.get('local_delivery')
                    break

        tax_collected = order.payment_details.tax_cost.dollars
        order_url = f'https://app.paperlessparts.com/orders/edit/{order.number}'
        processed_order_private_notes = order.private_notes.replace('\n',
                                                                    '<br>') if order.private_notes is not None else ''
        internal_comments = f'Order Number: <a href="{order_url}">{order.number}</a><br><br>{processed_order_private_notes}'
        if order.salesperson is not None:
            commission_note = f'Salesperson: {order.salesperson.first_name} {order.salesperson.last_name} ({order.salesperson.email})'

        else:
            commission_note = 'Salesperson not assigned'

        cetec_order_data = {
            "location": location,
            "shipto_name": shipto_name,
            "shipto_address_1": shipto_address_1,
            "shipto_address_2": shipto_address_2,
            "shipto_address_3": "",
            "shipto_address_4": "",
            "shipto_city": shipto_city,
            "shipto_state": shipto_state,
            "shipto_zip": shipto_zip,
            "billto_name": billto_name,
            "billto_address_1": billto_address_1,
            "billto_address_2": billto_address_2,
            "billto_address_3": "",
            "billto_address_4": "",
            "billto_city": billto_city,
            "billto_state": billto_state,
            "billto_zip": billto_zip,
            "external_key": external_key,
            "internal_comments": internal_comments,
            "commission_note": commission_note,
            "ship_via": ship_via,
            "shipping_instructions": shipping_instructions,
            "customer_taxtype": "1",
            "tax_collected": str(tax_collected),
            "place_order": self.erp_config.place_order,  # This must be set to True or else only a quote is created
            "internal_customer_id": self.erp_config.internal_customer_id,
            # TODO - this should be a config option, it will be 158 on PereDel's prod Cetec
            "internal_vendor_id": self.erp_config.internal_vendor_id,
            # TODO - this should be a config option, it will be 419 on PereDel's prod Cetec
        }

        # Handle customer ID
        if customer_custnum is not None:
            cetec_order_data['customer_custnum'] = customer_custnum
        cetec_order_data['customer_name'] = customer_name

        # Handle payment information
        payment_type = order.payment_details.payment_type
        if payment_type is not None:
            if payment_type == 'purchase_order':
                po_number = order.payment_details.purchase_order_number
                logger.info("Setting purchase order")
                cetec_order_data['po'] = po_number

                payment_terms = order.payment_details.payment_terms
                payment_terms_external_key = PAPERLESS_PAYMENT_TERMS_TO_CETEC_PAYMENT_TERMS_MAPPING.get(payment_terms)
                if payment_terms_external_key is not None:
                    cetec_order_data['terms_external_key'] = payment_terms_external_key
                else:
                    cetec_order_data['terms_description'] = payment_terms
            elif payment_type == 'credit_card':  # Credit cards
                cetec_order_data['payment_type_id'] = '4'
                cetec_order_data['prepayment_amount'] = 'FULL'
                cetec_order_data[
                    'prepayment_ref'] = f'{order.payment_details.card_brand}_{order.payment_details.card_last4}'

                payment_terms_external_key = PAPERLESS_PAYMENT_TERMS_TO_CETEC_PAYMENT_TERMS_MAPPING.get('Credit Card')
                cetec_order_data['terms_external_key'] = payment_terms_external_key
            else:
                pass

        # Handle Order line item data
        lines = []
        i = 0
        for order_item in order.order_items:
            part_number = self.get_part_number(order_item.root_component)
            prefix = self.get_prc_prefix(order_item.root_component)
            customer_part_number = self.get_customer_part_number(order_item.root_component)
            revision = self.get_revision(order_item.root_component)
            logger.info(f'Processing part number {part_number}; rev {revision}')

            sourcing_comments = order_item.private_notes if order_item.private_notes is not None else ''
            part_viewer_url = f'https://app.paperlessparts.com/parts/viewer/{order_item.root_component.part_uuid}'
            part_viewer_url_html = f'<a href="{part_viewer_url}">View Drawing</a>'
            sourcing_comments = f'{sourcing_comments}<br>Part viewer URL: {part_viewer_url_html}'
            if order_item.expedite_revenue is not None:
                sourcing_comments = f'{sourcing_comments}<br>Expedite revenue: {order_item.expedite_revenue.dollars}'
            sourcing_comments = self.add_part_complexity_to_sourcing_comments(order_item.root_component,
                                                                              sourcing_comments)  # TODO - verify this
            sourcing_comments = self.add_quote_link_to_sourcing_comments(order, sourcing_comments)
            sourcing_comments = self.add_job_shop_estimator_to_sourcing_comments(order_item, sourcing_comments)
            comments = order_item.public_notes if order_item.public_notes is not None else ''
            due_date = order.ships_on
            try:
                due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
                ship_datetime = due_datetime - timedelta(days=3)
                ship_date = datetime.strftime(ship_datetime, '%Y-%m-%d')
            except:
                ship_date = ''

            quantity = order_item.quantity
            resale = str(order_item.unit_price.dollars)

            cetec_line_data = {
                "prcpart": f'{prefix}{part_number}',
                "custpart": customer_part_number,
                "resale": resale,
                "cost": "0",
                "qty": quantity,
                "revision": revision,
                "description": "",
                "comments": comments,
                "sourcing_comments": sourcing_comments,
                "due_date": due_date,
                "ship_date": ship_date,
                "wip_date": "",
                "external_key": f"line_{i}",
                "transcode": self.erp_config.default_trans_code,  # Don't change this
            }
            lines.append(cetec_line_data)
            i = i + 1
            for add_on in order_item.ordered_add_ons:
                cetec_line_data = {
                    "prcpart": f"ZZZ {part_number}",
                    "custpart": customer_part_number,
                    "resale": float(add_on.price.dollars),
                    "cost": 0,
                    "qty": 1,
                    "revision": "",
                    "description": add_on.name,
                    "comments": add_on.notes,
                    "sourcing_comments": "",
                    "due_date": due_date,
                    "ship_date": ship_date,
                    "wip_date": "",
                    "external_key": f"line_{i}",
                    "transcode": "NN",  # Don't change this
                }
                lines.append(cetec_line_data)
                i = i + 1

        cetec_order_data['lines'] = lines

        cetec_order_data_list = [cetec_order_data]

        return cetec_order_data_list

    def assemble_part_revision_definition_json(self, order):
        order_items_part_revision_definition_json = []
        for order_item in order.order_items:
            order_item_bom_json = self.assemble_component_json(order_item, order_item.root_component)
            order_items_part_revision_definition_json.append(order_item_bom_json)
        return order_items_part_revision_definition_json

    def assemble_component_json(self, order_item, component):
        bom_definition = []
        for child_component_id in component.child_ids:
            # There is an implicit base case for this recursive function when a component has no children
            child_component = order_item.get_component(child_component_id)
            if child_component is None:
                continue  # This should never happen, but just in case this will avoid throwing an exception
            child_component_json = self.assemble_component_json(order_item, child_component)
            bom_definition.append(child_component_json)

        # Special case for manufactured components - manually add a raw material BOM component as a child
        if component.type == 'manufactured':
            child_raw_material_json = assemble_raw_material_json(component)
            if child_raw_material_json is not None:
                bom_definition.append(child_raw_material_json)
            else:
                child_raw_material_json = assemble_placeholder_raw_material_json(component)
                bom_definition.append(child_raw_material_json)

        part_number = self.get_part_number(component)
        revision = self.get_revision(component)
        prefix = self.get_prc_prefix(component)
        qty_per_top = component.innate_quantity  # TODO - is this the right quantity? Is it relative to the very top? Or just relative to its parent?
        quantity_for_outside_service_lead_times = component.deliver_quantity
        locations = assemble_routing_data_for_component(self.erp_config, component, quantity_for_outside_service_lead_times,
                                                        PAPERLESS_OPERATION_TO_CETEC_LOCATION_OPERATION_MAPPING)  # TODO - double check that this is the right quantity

        component_json = {
            'prcpart': f'{prefix}{part_number}',
            'revision_text': str(revision),
        }

        if not component.is_root_component:
            component_json['qty_per_top'] = qty_per_top

        # Only add bom_definition as a key if it is non-empty
        if bom_definition:
            component_json['bom_definition'] = bom_definition

        # Only add locations as a key if it is non-empty
        if locations:
            component_json['locations'] = locations

        return component_json

    def get_part_number(self, component):
        # Generate a random 16-digit part number in case the part_number is blank
        # We can't use a single default part number because assemblies are not allowed to be self-referential, so part
        # numbers must be unique
        import string
        random_part_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return component.part_number if component.part_number is not None else random_part_number

    def get_revision(self, component):
        return component.revision if component.revision is not None else ''

    def get_prc_prefix(self, component):
        return ""

    def add_part_complexity_to_sourcing_comments(self, component, sourcing_comments):
        for op in component.shop_operations:
            if op.operation_definition_name and op.operation_definition_name.startswith('Part Complexity'):
                # Include the part complexity in the sourcing comments for the ordline
                part_complexity = op.get_variable('Complexity')
                if part_complexity is not None:
                    sourcing_comments = f'{sourcing_comments}<br>Part complexity: {part_complexity}'
        return sourcing_comments

    def add_quote_link_to_sourcing_comments(self, order, sourcing_comments):
        if order.quote_revision_number is None:
            quote_number = order.quote_number
        else:
            quote_number = f'{order.quote_number}-{order.quote_revision_number}'
        quote_url = f'https://app.paperlessparts.com/quotes/edit/{quote_number}'

        sourcing_comments = f'{sourcing_comments}<br>' \
                            f'Quote Number: <a href="{quote_url}">{quote_number}</a>'
        return sourcing_comments

    def add_job_shop_estimator_to_sourcing_comments(self, order_item, sourcing_comments):
        for component in order_item.components:
            if component.type == 'purchased':
                continue
            for op in component.shop_operations:
                if op.operation_definition_name and op.operation_definition_name == 'Job Shop Estimator':
                    material_cost_percent_total_cost = op.get_variable('material cost % of total cost')
                    material_cost_percent_total_price = op.get_variable('material cost % of total price')
                    shop_rate = op.get_variable('shop rate')
                    sourcing_comments = f'{sourcing_comments}<br>' \
                                        f'Part Number: {component.part_number}<br>' \
                                        f'Material Cost % of Total Cost: {material_cost_percent_total_cost}<br>' \
                                        f'Material Cost % of Total Price: {material_cost_percent_total_price}<br>' \
                                        f'Shop Rate: {shop_rate}<br>'
        return sourcing_comments

    def get_customer_part_number(self, root_component):
        cust_part = ''
        for operation in root_component.shop_operations:
            if operation.operation_definition_name is not None and \
                    operation.operation_definition_name == 'Customer Part Number':
                cust_part_val = operation.get_variable('Customer Part Number')
                if cust_part_val is not None:
                    cust_part = cust_part_val
        return cust_part
