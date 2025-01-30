from typing import List, Optional

from baseintegration.utils import convert_datetime_to_utc
from baseintegration.utils.repeat_work_objects import Part, Header, Account, Contact, AddOn
from baseintegration.utils.repeat_work_utils import get_headers_from_methods, MOMWrapper
from m2m.importer.processors.base import BaseM2MImportProcessor
from m2m.models import Qtitem, Slcdpmx, Qtmast, Syphon, Jomast, Somast
from baseintegration.datamigration import logger
from m2m.utils.repeat_work_utils import get_estimated_erp_code, PartData, TemplateRoot


class HeaderProcessor(BaseM2MImportProcessor):
    def _process(self, repeat_part: Part, part_data: PartData, methods_of_manufacture: List[MOMWrapper]):
        self.source_database = self._importer.source_database
        logger.info(f"Creating repeat part headers from M2M item ID: {part_data.id()}")
        repeat_part.headers = get_headers_from_methods(
            methods_of_manufacture,
            self.get_template_header, self.get_estimated_header,
            self.get_engineered_header, self.get_executed_header)
        return repeat_part

    def get_template_header(self, item_data: TemplateRoot):
        item = item_data.item
        bom = item_data.bom
        erp_code = f"{item.fpartno.strip()}::::{item.frev.strip()}"
        return Header(
            erp_code=erp_code,
            type="template",
            created_date=convert_datetime_to_utc(bom.fdlastrev),
            private_notes=item.fdescript
        )

    def get_estimated_header(self, quote_item: Qtitem) -> Header:
        quote: Qtmast = Qtmast.objects.using(self.source_database).filter(fquoteno=quote_item.fquoteno).first()
        if quote:
            account = self._get_account(quote.fcustno)
            contact = self._get_contact_from_quote(quote)
            created_date = convert_datetime_to_utc(quote.fquotedate)
        else:
            account = None
            contact = None
            created_date = convert_datetime_to_utc(quote_item.fctpdate)
        return Header(
            erp_code=get_estimated_erp_code(quote_item),
            type="estimated",
            account=account,
            contact=contact,
            created_date=created_date,
            private_notes=quote_item.fdescmemo,
            add_ons=self._get_add_ons_from_quote_item(quote_item),
        )

    def get_engineered_header(self, job: Jomast) -> Header:
        sales_order: Somast = Somast.objects.using(self.source_database).filter(fsono=job.fsono).first()
        return Header(
            erp_code=job.fjobno,
            type="engineered",
            account=self._get_account_from_sales_order(sales_order),
            contact=self._get_contact_from_sales_order(sales_order),
            created_date=convert_datetime_to_utc(job.fopen_dt),
            private_notes=job.fjob_mem,
            add_ons=self._get_add_ons_from_job(job),
        )

    def get_executed_header(self, job: Jomast) -> Header:
        sales_order: Somast = Somast.objects.using(self.source_database).filter(fsono=job.fsono).first()
        return Header(
            erp_code=job.fjobno,
            type="executed",
            account=self._get_account_from_sales_order(sales_order),
            contact=self._get_contact_from_sales_order(sales_order),
            created_date=convert_datetime_to_utc(job.fact_rel),
            private_notes=job.fjob_mem,
            add_ons=self._get_add_ons_from_job(job),
        )

    def _get_contact_from_quote(self, quote: Qtmast) -> Optional[Contact]:
        contact = self._get_contact(quote.contactnum)
        return contact or Contact(
            email="",
            first_name=self.generate_normalized_value(quote.fcfname),
            last_name=self.generate_normalized_value(quote.fquoteto),
            phone=self.generate_normalized_value(quote.fphone)
        )

    def _get_account_from_sales_order(self, sales_order: Somast) -> Optional[Account]:
        if sales_order:
            return self._get_account(sales_order.fcustno)

    def _get_contact_from_sales_order(self, sales_order: Somast) -> Optional[Contact]:
        if sales_order:
            contact = self._get_contact(sales_order.contactnum)
            return contact or Contact(
                email="",
                first_name=self.generate_normalized_value(sales_order.fcfname),
                last_name=self.generate_normalized_value(sales_order.fcontact),
                phone=self.generate_normalized_value(sales_order.fphone)
            )

    def _get_account(self, customer: str) -> Optional[Account]:
        if customer:
            m2m_account: Slcdpmx = Slcdpmx.objects.using(self.source_database).filter(fcustno=customer).first()
            if m2m_account:
                return Account(
                    name=self.generate_normalized_value(m2m_account.fcompany),
                    erp_code=str(m2m_account.fcustno),
                    phone=self.generate_normalized_value(m2m_account.fphone),
                    url=self.generate_normalized_value(m2m_account.furl)
                )

    def _get_contact(self, contact_number: str) -> Optional[Contact]:
        if contact_number:
            contact: Syphon = Syphon.objects.using(self.source_database).filter(number=contact_number).first()
            if contact:
                phone = self.generate_normalized_value(contact.fcnumber) \
                    or self.generate_normalized_value(contact.phonework) \
                    or self.generate_normalized_value(contact.phonemobile) \
                    or self.generate_normalized_value(contact.phonehome)
                return Contact(
                    email=self.generate_normalized_value(contact.fcemail),
                    first_name=self.generate_normalized_value(contact.fcfname),
                    last_name=self.generate_normalized_value(contact.fcontact),
                    notes=self.generate_normalized_value(contact.fmnotes),
                    phone=phone
                )

    @classmethod
    def _get_add_ons_from_quote_item(cls, quote_item: Qtitem) -> List[AddOn]:
        return []

    @classmethod
    def _get_add_ons_from_job(cls, job: Jomast) -> List[AddOn]:
        return []
