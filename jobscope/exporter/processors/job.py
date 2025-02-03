from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem
from baseintegration.datamigration import logger
from baseintegration.utils import set_blank_to_default_value
from jobscope.utils import get_part_number_and_name


class JobProcessor(BaseProcessor):

    def _process(self, order: Order, customer: dict) -> None:
        logger.info(f"Creating job for order {order.number}")
        shipping_address_1 = order.shipping_info.address1 if order.shipping_info is not None else customer.get("addressLine1")
        shipping_address_2 = order.shipping_info.address2 if order.shipping_info is not None else customer.get("addressLine2")
        shipping_attention = order.shipping_info.business_name if order.shipping_info is not None else "N/A"
        shipping_city = order.shipping_info.city if order.shipping_info is not None else customer.get("city")
        shipping_state = order.shipping_info.state if order.shipping_info is not None else customer.get("state")
        shipping_country = order.shipping_info.country if order.shipping_info is not None else customer.get("country")
        shipping_postal_code = order.shipping_info.postal_code if order.shipping_info is not None else customer.get("postalCode")

        billing_address_1 = order.billing_info.address1 if order.billing_info is not None else customer.get("addressLine1")
        billing_address_2 = order.billing_info.address2 if order.billing_info is not None else customer.get("addressLine2")
        billing_attention = order.billing_info.attention if order.billing_info is not None else "N/A"
        billing_city = order.billing_info.city if order.billing_info is not None else customer.get("city")
        billing_state = order.billing_info.state if order.billing_info is not None else customer.get("state")
        billing_country = order.billing_info.country if order.billing_info is not None else customer.get("country")
        billing_postal_code = order.billing_info.postal_code if order.billing_info is not None else customer.get("postalCode")
        po_ref = order.payment_details.purchase_order_number if order.payment_details is not None else "N/A"

        # if customer doesn't have values, set to N/A

        shipping_address_1 = set_blank_to_default_value(shipping_address_1, "N/A")
        shipping_address_2 = set_blank_to_default_value(shipping_address_2, "-")
        shipping_city = set_blank_to_default_value(shipping_city, "Morgantown")
        shipping_state = set_blank_to_default_value(shipping_state, "PA")
        shipping_country = set_blank_to_default_value(shipping_country, "USA")
        shipping_postal_code = set_blank_to_default_value(shipping_postal_code, "19543")

        billing_address_1 = set_blank_to_default_value(billing_address_1, "N/A")
        billing_address_2 = set_blank_to_default_value(billing_address_2, "-")
        billing_city = set_blank_to_default_value(billing_city, "Morgantown")
        billing_state = set_blank_to_default_value(billing_state, "PA")
        billing_country = set_blank_to_default_value(billing_country, "USA")
        billing_postal_code = set_blank_to_default_value(billing_postal_code, "19543")

        po_ref = set_blank_to_default_value(po_ref, "N/A")
        payment_terms_code = set_blank_to_default_value(customer.get("paymentTermsCode"), "N30")
        canadian_exempt_tax_fed = set_blank_to_default_value(customer.get("canadianTaxExemptFed"), "")
        canadian_exempt_tax_exempt_prov = set_blank_to_default_value(customer.get("canadianTaxExemptProv"), "")
        customer_name = set_blank_to_default_value(customer.get("customerName"), "N/A")
        company_code = set_blank_to_default_value(customer.get("companyCode"), "04")
        # default customer to hillside if customer was not found
        customer_number = set_blank_to_default_value(customer.get("customerNumber"), "001545")
        if customer_number == "001545":
            description = "Customer was set to Hillside Custom because we could not find a matching customer in " \
                          "Jobscope from Paperless. Please fix "
        else:
            description = set_blank_to_default_value(order.private_notes, "")
        job = self._exporter.client.create_job(customer_number,
                                               description,
                                               shipping_address_1,
                                               shipping_address_2,
                                               shipping_attention,
                                               shipping_city,
                                               shipping_state,
                                               shipping_country,
                                               shipping_postal_code,
                                               billing_address_1,
                                               billing_address_2,
                                               billing_attention,
                                               billing_city,
                                               billing_state,
                                               billing_country,
                                               billing_postal_code,
                                               order.created_dt,
                                               order.ships_on_dt,
                                               po_ref,
                                               "CM",
                                               "WIP",
                                               100.0,
                                               "NB",
                                               "-",
                                               "USD",
                                               payment_terms_code,
                                               canadian_exempt_tax_fed,
                                               canadian_exempt_tax_exempt_prov,
                                               customer_name,
                                               company_code)
        job_number = job["jobNumber"]
        self._exporter.success_message = f"Associated Jobscope job number is {job_number}"
        self.create_line_items(order, job_number)

    def create_line_items(self, order: Order, job_number: str):
        line_item_no = 1
        for line_item in order.order_items:
            line_item: OrderItem = line_item
            logger.info(f"Creating line item {str(line_item_no)} for order {str(order.number)}")
            mrp_status = "-"
            canadian_fed_tax_code = "N/A"
            canadian_prov_tax_code = "N/A"
            cost_account = ""
            description = line_item.description if line_item.description is not None else line_item.root_component.description
            description = set_blank_to_default_value(description, "N/A")[0:40]
            location = self._exporter._integration.config_yaml["Jobscope"]["location_code"]
            material_cost_account = "N/A"
            finish_code = ""
            position_number = "N/A"
            receiving_part_number = "N/A"
            revision_level = "-"
            suggested_order_action = "N/A"
            work_order = "N/A"
            part_number, _ = get_part_number_and_name(line_item.root_component)
            if not self._exporter._integration.test_mode:
                psm = self._exporter.client.get_part(part_number)["psm"]
            else:
                psm = "P"
            self._exporter.client.create_job_line_item(job_number=job_number,
                                                       line_item_no=line_item_no,
                                                       accept_warnings=True,
                                                       part_number=part_number,
                                                       revision=line_item.root_component.revision,
                                                       psm=psm,
                                                       quantity=line_item.quantity,
                                                       unit_price=float(line_item.unit_price.dollars),
                                                       uom="EA",
                                                       mrp_status=mrp_status,
                                                       canadian_fed_tax_code=canadian_fed_tax_code,
                                                       canadian_prov_tax_code=canadian_prov_tax_code,
                                                       cost_account=cost_account,
                                                       description=description,
                                                       location_code=location,
                                                       material_cost=material_cost_account,
                                                       finish_code=finish_code,
                                                       position_number=position_number,
                                                       receiving_part_number=receiving_part_number,
                                                       revision_level=revision_level,
                                                       suggested_order_action=suggested_order_action,
                                                       work_order=work_order)
            line_item_no += 1
