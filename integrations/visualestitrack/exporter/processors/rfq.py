import datetime as datetime

from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order
from paperless.objects.customers import Account

from visualestitrack.models import Requestforquote

ESTITRACK_CODE_LIMIT = 7


class CreateRFQ(BaseProcessor):
    """
    This class extends BaseProcessor from baseintegration and is used to create RFQ records into VisualEstiTrack.
    """

    def _process(self, order: Order) -> Requestforquote:
        rfq_id = f"{order.number}"

        code = None
        name = ''
        if order.contact.account is not None:
            name = order.contact.account.name
            if order.contact.account.erp_code is not None:
                if len(order.contact.account.erp_code) < ESTITRACK_CODE_LIMIT:
                    code = order.contact.account.erp_code
                else:
                    logger.warning(f'VisualEstiTrackExporter: erp_code "{order.contact.account.erp_code}" too '
                                   f'long(limit 6) for VisualEstiTrack setting it to empty')
        add1 = ''
        add2 = ''
        add3 = ''
        add4 = ''
        if order.shipping_info is not None:
            add1 = order.shipping_info.address1
            add2 = order.shipping_info.address2
            add3 = CreateRFQ.create_third_line_address_str(order.shipping_info.city, order.shipping_info.state,
                                                           order.shipping_info.postal_code)
            add4 = order.shipping_info.country
        else:
            account = Account.get(id=order.contact.account.id)
            if account.sold_to_address is not None:
                add1 = account.sold_to_address.address1
                add2 = account.sold_to_address.address2
                add3 = CreateRFQ.create_third_line_address_str(account.sold_to_address.city,
                                                               account.sold_to_address.state,
                                                               account.sold_to_address.postal_code)
                add4 = account.sold_to_address.country
        date = CreateRFQ.create_date_string(order.created_dt)
        sales_person_name = ''
        sales_person_email = ''
        if order.estimator is not None:
            sales_person_name = f"{order.estimator.first_name} {order.estimator.last_name}"
            sales_person_email = order.estimator.email
        request = Requestforquote(
            id=rfq_id,
            rfqdate=date,
            processed=False,
            customername=name,
            customercode=code,
            customeraddressline1=add1,
            customeraddressline2=add2,
            customeraddressline3=add3,
            customeraddressline4=add4,
            salespersonname=sales_person_name,
            salespersonemail=sales_person_email)
        request.save()
        return request

    @staticmethod
    def create_third_line_address_str(city: str, state: str, postal_code: str) -> str:
        return f"{city}, {state} {postal_code}"

    @staticmethod
    def create_date_string(date_time_str: datetime):
        return date_time_str.strftime("%Y-%m-%d")
