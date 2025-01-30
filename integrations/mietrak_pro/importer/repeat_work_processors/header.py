from typing import Optional, List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import convert_datetime_to_utc
from baseintegration.utils.repeat_work_objects import Part, Header, Account, Contact, AddOn
from baseintegration.utils.repeat_work_utils import MOMWrapper, get_headers_from_methods
from mietrak_pro.importer.processors.account import AccountImportProcessor
from mietrak_pro.models import Item, Requestforquoteline, Party, Salesorder, Workorder, Workorderjob, Quote, Router
from baseintegration.datamigration import logger


class HeaderProcessor(BaseImportProcessor):
    def _process(self, repeat_part: Part, item: Item, methods_of_manufacture: List[MOMWrapper]):
        logger.info(f"Creating repeat part headers from Mie Trak Pro item ID: {item.pk}")
        repeat_part.headers = get_headers_from_methods(
            methods_of_manufacture,
            self.get_template_header, self.get_estimated_header,
            self.get_engineered_header, self.get_executed_header)
        return repeat_part

    @classmethod
    def get_template_header(cls, router: Router) -> Header:
        return Header(
            erp_code=str(router.pk),
            type="template",
            account=cls.get_account(router.customerfk),
            created_date=convert_datetime_to_utc(router.datestamp),
            private_notes=router.comment,
            methods_of_manufacture=[]
        )

    @classmethod
    def get_estimated_header(cls, quote: Quote) -> Header:
        rfq_line: Requestforquoteline = Requestforquoteline.objects.filter(quotefk=quote)\
            .select_related('requestforquotefk__buyerfk').first()
        if rfq_line:
            contact = cls.get_contact(rfq_line.requestforquotefk.buyerfk)
            add_ons = cls.get_add_ons(rfq_line)
        else:
            contact = None
            add_ons = []
        return Header(
            erp_code=str(quote.pk),
            type="estimated",
            account=cls.get_account(quote.customerfk),
            contact=contact,
            created_date=convert_datetime_to_utc(quote.datestamp),
            private_notes=quote.comment,
            add_ons=add_ons,
            methods_of_manufacture=[]
        )

    @classmethod
    def get_engineered_header(cls, work_order: Workorder) -> Header:
        return Header(
            erp_code=str(work_order.pk),
            type="engineered",
            account=cls.get_account(work_order.customerfk),
            contact=cls.get_contact_from_work_order(work_order),
            created_date=convert_datetime_to_utc(work_order.createdate),
            private_notes=work_order.manufacturingnotes,
            methods_of_manufacture=[]
        )

    @classmethod
    def get_executed_header(cls, work_order: Workorder) -> Header:
        return Header(
            erp_code=str(work_order.pk),
            type="executed",
            account=cls.get_account(work_order.customerfk),
            contact=cls.get_contact_from_work_order(work_order),
            created_date=convert_datetime_to_utc(work_order.closeddate) or 0,
            private_notes=work_order.manufacturingnotes,
            methods_of_manufacture=[]
        )

    @classmethod
    def get_account(cls, mtp_customer: Party) -> Optional[Account]:
        if mtp_customer:
            return Account(
                name=mtp_customer.name,
                erp_code=str(mtp_customer.pk),
                phone=mtp_customer.phone,
                url=mtp_customer.website
            )

    @classmethod
    def get_contact(cls, mtp_buyer: Party) -> Optional[Contact]:
        if mtp_buyer:
            first_name, last_name = AccountImportProcessor.get_contact_first_and_last_name(mtp_buyer)
            return Contact(
                email=mtp_buyer.email,
                first_name=first_name,
                last_name=last_name,
                notes=mtp_buyer.notes,
                phone=mtp_buyer.phone
            )

    @classmethod
    def get_add_ons(cls, rfq_line: Requestforquoteline) -> List[AddOn]:
        add_ons = []

        tooling_charge = rfq_line.toolingcharge
        if tooling_charge:
            add_ons.append(
                AddOn(
                    is_required=True,
                    name="Tooling Charge",
                    unit_price=tooling_charge,
                )
            )

        return add_ons

    @classmethod
    def get_contact_from_work_order(cls, work_order: Workorder) -> Contact:
        work_order_job: Workorderjob = Workorderjob.objects.filter(workorderfk=work_order).first()
        if work_order_job:
            sales_order: Salesorder = work_order_job.salesorderfk
            if sales_order:
                buyer: Party = sales_order.buyerfk
                return cls.get_contact(buyer)
