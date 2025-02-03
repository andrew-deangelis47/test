from typing import List, Dict, Tuple, Optional
from datetime import datetime

from baseintegration.datamigration import logger
from baseintegration.utils import convert_datetime_to_utc, safe_get
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Header, Account, Contact
from e2.models import (
    Order,
    CustomerCode,
    Contacts as E2Contact,
    Quotedet,
    Quote,
    Estim,
    OrderDet, JobReq
)
from e2.importer.utils import RepeatPartUtilObject, JobMOMUtil, QuoteMOMUtil, TemplateMOMUtil


class HeaderImportProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info(f"Calculating headers for repeat work part from E2 with part number {repeat_part_util.e2_part.partno}")
        self.source_database = self._importer.source_database

        headers_by_key: Dict[Tuple[str, str], Header] = {}
        for mom_util in [*repeat_part_util.job_mom_utils, *repeat_part_util.quote_mom_utils, *repeat_part_util.template_mom_utils]:
            mom, header_type, erp_code = (
                mom_util.method_of_manufacture,
                mom_util.type,
                mom_util.erp_code,
            )
            header_key = (header_type, erp_code)
            header: Optional[Header] = headers_by_key.get(header_key)
            if not header:
                if header_type in ("engineered", "executed"):
                    header = self.get_job_header(mom_util)
                elif header_type == "estimated":
                    header = self.get_quote_header(mom_util)
                elif header_type == "template":
                    header = self.get_template_header(mom_util)
                else:
                    raise ValueError(f"Invalid header type {header_type}")
                headers_by_key[header_key] = header

            header.methods_of_manufacture.append(mom)

        headers: List[Header] = list(headers_by_key.values())
        logger.info(f"Created headers for E2 repeat part with part number {repeat_part_util.e2_part.partno}")
        repeat_part_util.repeat_part.headers = headers
        return repeat_part_util

    def get_job_header(self, job_mom_util: JobMOMUtil) -> Header:
        order_detail = job_mom_util.order_detail
        if order_detail:
            created_date = order_detail.estim_start_date
            order_no = order_detail.orderno
            private_notes = self.get_order_detail_header_notes(order_detail)
        else:
            job_requirement = job_mom_util.job_requirement
            created_date = job_requirement.dateprocessed
            order_no = job_requirement.orderno
            private_notes = self.get_job_requirement_header_notes(job_requirement)
        orders: List[Order] = Order.objects.using(self.source_database).filter(order_no=order_no)
        customer_code: Optional[str] = orders[0].customer_code if orders else None
        contact_name: Optional[str] = orders[0].purch_contact if orders else None
        job_requirement_header = Header(
            erp_code=job_mom_util.erp_code,
            type=job_mom_util.type,
            account=self.get_account_by_customer_code(customer_code),
            contact=self.get_contact_by_customer_code_and_name(customer_code, contact_name),
            created_date=convert_datetime_to_utc(created_date) if created_date else convert_datetime_to_utc(datetime.now()),
            public_notes="",
            private_notes=private_notes,
            add_ons=[],
            methods_of_manufacture=[]
        )
        return job_requirement_header

    def get_quote_header(self, quote_mom_util: QuoteMOMUtil) -> Header:
        quote_detail = quote_mom_util.quote_detail
        quotes: List[Quote] = Quote.objects.using(self.source_database).filter(quoteno=quote_detail.quoteno)
        quote: Quote = quotes[0] if quotes else None

        quote_detail_header = Header(
            erp_code=quote_mom_util.erp_code,
            type=quote_mom_util.type,
            account=self.get_account_by_customer_code(quote.custcode),
            contact=self.get_contact_by_customer_code_and_name(quote.custcode, quote.contactname),
            created_date=convert_datetime_to_utc(quote.dateent) if quote and quote.dateent else convert_datetime_to_utc(datetime.now()),
            public_notes="",
            private_notes=self.get_quote_detail_header_notes(quote_detail),
            add_ons=[],
            methods_of_manufacture=[]
        )
        return quote_detail_header

    def get_template_header(self, template_mom_util: TemplateMOMUtil) -> Header:
        template = template_mom_util.template
        template_header = Header(
            erp_code=template_mom_util.erp_code,
            type=template_mom_util.type,
            account=self.get_account_by_customer_code(template.custcode),
            contact=self.get_contact_by_customer_code(template.custcode),
            created_date=convert_datetime_to_utc(template.entdate) if template.entdate else convert_datetime_to_utc(datetime.now()),
            public_notes="",
            private_notes=self.get_template_header_notes(template),
            add_ons=[],
            methods_of_manufacture=[]
        )
        return template_header

    def get_account_by_customer_code(self, customer_code: Optional[str]) -> Optional[Account]:
        if customer_code is None:
            return None

        customer_codes: List[CustomerCode] = CustomerCode.objects.using(self.source_database).filter(customer_code=customer_code)
        if not customer_codes:
            return None
        customer_code: CustomerCode = customer_codes[0]

        account = Account(
            name=customer_code.customer_name,
            erp_code=customer_code.customer_code,
            phone=customer_code.phone,
            url=customer_code.website
        )
        return account

    def get_contact_by_customer_code_and_name(self, customer_code: Optional[str], contact_name: Optional[str]) -> Optional[Contact]:
        if customer_code is None and contact_name is None:
            return None
        elif contact_name is None:
            return self.get_contact_by_customer_code(customer_code)
        elif customer_code is None:
            return self.get_contact_by_name(contact_name)
        else:
            e2_contacts: List[E2Contact] = E2Contact.objects.using(self.source_database).filter(code=customer_code, contact=contact_name)
            return self.construct_paperless_contact(e2_contacts)

    def get_contact_by_customer_code(self, customer_code: Optional[str]) -> Optional[Contact]:
        if customer_code is None:
            return None
        e2_contacts: List[E2Contact] = E2Contact.objects.using(self.source_database).filter(code=customer_code)
        return self.construct_paperless_contact(e2_contacts)

    def get_contact_by_name(self, contact_name: Optional[str]) -> Optional[Contact]:
        if contact_name is None:
            return None
        e2_contacts: List[E2Contact] = E2Contact.objects.using(self.source_database).filter(contact=contact_name)
        return self.construct_paperless_contact(e2_contacts)

    def construct_paperless_contact(self, e2_contacts: List[E2Contact]) -> Optional[Contact]:
        if not e2_contacts:
            return None
        e2_contact: E2Contact = e2_contacts[0]
        full_contact_name = e2_contact.contact or ''
        contact_names: List[str] = full_contact_name.split(" ")

        contact = Contact(
            email=e2_contact.email,
            first_name=contact_names[0],
            last_name=contact_names[1] if len(contact_names) > 1 else "",
            notes=e2_contact.comments,
            phone=e2_contact.phone
        )
        return contact

    def get_job_requirement_header_notes(self, job_requirement: JobReq) -> str:
        notes = ""
        if safe_get(job_requirement, 'partdesc', False):
            notes += f"Part Description: {job_requirement.partdesc}\n"
        if safe_get(job_requirement, "prodcode", False):
            notes += f"Prod Code: {job_requirement.prodcode}\n"
        if safe_get(job_requirement, "workcode", False):
            notes += f"Work Code: {job_requirement.workcode}\n"
        return notes

    def get_order_detail_header_notes(self, order_detail: OrderDet) -> str:
        notes = ""
        if safe_get(order_detail, 'part_desc', False):
            notes += f"Part Description: {order_detail.part_desc}\n"
        if safe_get(order_detail, "prod_code", False):
            notes += f"Prod Code: {order_detail.prod_code}\n"
        if safe_get(order_detail, "work_code", False):
            notes += f"Work Code: {order_detail.work_code}\n"
        return notes

    def get_quote_detail_header_notes(self, quote_detail: Quotedet) -> str:
        notes = ""
        if safe_get(quote_detail, 'descrip', False):
            notes += f"Description: {quote_detail.descrip}\n"
        if safe_get(quote_detail, "workcode", False):
            notes += f"Work Code: {quote_detail.workcode}\n"
        if safe_get(quote_detail, "jobnotes", False):
            notes += f"Job Notes: {quote_detail.jobnotes}\n"
        return notes

    def get_template_header_notes(self, template: Estim) -> str:
        notes = ""
        if safe_get(template, 'descrip', False):
            notes += f"Description: {template.descrip}\n"
        if safe_get(template, "prodcode", False):
            notes += f"Prod Code: {template.prodcode}\n"
        return notes
