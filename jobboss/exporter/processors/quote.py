import jobboss.models as jb
import datetime
from baseintegration.datamigration import logger
from baseintegration.utils import update_quote_erp_code
from . import JobBossProcessor
from paperless.objects.quotes import Quote, Quantity
from jobboss.query.customer import get_or_create_customer
import uuid
from django.utils.timezone import make_aware
from paperless.client import PaperlessClient


class QuoteProcessor(JobBossProcessor):
    do_rollback = False
    quote_api_response = {}

    def _process(self, quote: Quote):
        self.quote_api_response = self.get_quote_from_api(quote)
        try:
            customer = get_or_create_customer(code=quote.customer.company.erp_code, name=quote.customer.company.business_name)
        except:
            customer = get_or_create_customer(code="MISC", name="Miscellaneous")
        contact_name = quote.contact.first_name + " " + quote.contact.last_name
        contact_name = contact_name[0:16]
        sales_rep_id, commission = self.get_sales_rep_id(quote.salesperson)
        quoted_by = self.get_quoted_by(quote.estimator)
        rfq = self.get_rfq()
        rfq = jb.Rfq(
            rfq=rfq,
            note_text=quote.number,
            customer=customer.customer,
            reference=contact_name,
            quote_date=make_aware(datetime.datetime.utcnow()),
            commission_pct=commission,
            status_date=quote.sent_date,
            rfq_date=make_aware(datetime.datetime.utcnow()),
            trade_currency=1,
            fixed_rate=1,
            certs_required=0,
            trade_date=make_aware(datetime.datetime.utcnow()),
            expiration_date=quote.expired_date,
            currency_conv_rate=1,
            quoted_by=quoted_by,
            submitted_date=make_aware(datetime.datetime.utcnow()),
            status="Pending",
            win_probability=80,
            sales_rep=sales_rep_id,
            source="System"
        )
        rfq.save()
        i = 1
        logger.info(f"Made rfq {rfq.rfq}")
        self._exporter.success_message = f"Associated JobBOSS quote number is {rfq.rfq}"
        for index, item in enumerate(quote.quote_items):
            workflow_status = self.get_workflow_status(index)
            quote_id = str(uuid.uuid4())
            q = jb.Quote(
                line=str(i),
                quote=quote_id,
                top_lvl_quote=quote_id,
                quoted_by=quoted_by,
                type="Regular",
                status=workflow_status,
                priority=5,
                assembly_level=0,
                quantity_per=0,
                certs_required=0,
                lead_days=0,
                last_updated=make_aware(datetime.datetime.utcnow()),
                rfq=rfq.rfq,
                part_number=item.root_component.part_number
            )
            q.save()
            logger.info(f"Saved quote {quote_id}")
            for quantity in item.root_component.quantities:
                quantity: Quantity = quantity
                logger.info(f"Total price is {float(quantity.total_price_with_required_add_ons.dollars)}")
                jb.QuoteQty.objects.create(
                    quote=q,
                    quote_qty=quantity.quantity,
                    yield_pct=100,
                    make_quantity=quantity.quantity,
                    est_setup_hrs=0,
                    est_run_hrs=0,
                    est_total_hrs=0,
                    est_labor=0,
                    est_service=0,
                    est_labor_burden=0,
                    est_ga_burden=0,
                    est_machine_burden=0,
                    labor_burden_markup_pct=0,
                    ga_burden_markup_pct=0,
                    machine_burden_markup_pct=0,
                    price_unit_conv=1,
                    decimal_places=2,
                    price_source=1,
                    locked_source=0,
                    unit_price=float(quantity.unit_price.dollars),
                    quoted_unit_price=float(quantity.unit_price.dollars),
                    total_price=float(quantity.total_price_with_required_add_ons.dollars),
                    price_uofm="ea",
                    order_unit="ea",
                    last_updated=make_aware(datetime.datetime.utcnow())
                )
            i = i + 1

        if self._exporter.erp_config.should_update_quote_erp_code_in_paperless_parts:
            new_erp_code = str(rfq.rfq)
            self._exporter._integration.paperless_config.should_write_to_paperless_parts = True
            update_quote_erp_code(self._exporter._integration, quote.number, quote.revision_number, new_erp_code)

    # gets overriden
    def get_quoted_by(self, estimator):
        return None

    # gets overriden
    def get_sales_rep_id(self, salesperson):
        return None, 0

    def get_rfq(self):
        auto_num = jb.AutoNumber.objects.filter(type="Quote").first()
        new_num = int(auto_num.last_nbr) + 1
        auto_num.last_nbr = str(new_num)
        auto_num.save()
        return new_num

    def get_workflow_status(self, index):
        status = self.quote_api_response["quote_items"][index]["workflow_status"]
        if 'no_quote' in status:
            return 'No Quote'
        else:
            return 'Active'

    def get_quote_from_api(self, quote):
        client = PaperlessClient.get_instance()
        quote = client.get_resource(
            id=quote.number,
            params={"quoteNumber": quote.number, "revision": quote.revision_number},
            resource_url='quotes/public/'
        )
        return quote
