from datetime import datetime
from typing import List, Dict, Tuple, Optional, Union
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import convert_datetime_to_utc
from baseintegration.utils.repeat_work_objects import Header, Account, Contact
from baseintegration.utils import safe_get
from epicor.quote import QuoteHeader, QuoteContact, QuoteDetail
from epicor.job import JobEntry
from epicor.engineering_workbench import EWBRev
from epicor.customer import Customer
from epicor.customer import Contact as EpicorContact
from epicor.importer.utils import RepeatPartUtilObject, get_quote_detail_erp_code, construct_ewb_erp_code, QuoteMOMUtil


class HeaderImportProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info(f"Creating headers for repeat work part from Epicor with part number "
                    f"{repeat_part_util.repeat_part.part_number} and revision number "
                    f"{repeat_part_util.repeat_part.revision}")

        headers_by_key: Dict[Tuple[str, str], Header] = {}
        for mom_util_list in [repeat_part_util.quote_mom_utils, repeat_part_util.job_mom_utils,
                              repeat_part_util.ewb_mom_utils]:
            for mom_util in mom_util_list:
                mom, header_type, erp_code = (
                    mom_util.mom,
                    mom_util.type,
                    mom_util.erp_code,
                )
                header_key = (header_type, erp_code)
                header: Optional[Header] = headers_by_key.get(header_key)
                if not header:
                    if header_type == "estimated":
                        header = self.get_quote_header(mom_util)
                    elif header_type in ("engineered", "executed"):
                        header = self.get_job_header(mom_util.epicor_job)
                    elif header_type == "template":
                        header = self.get_ewb_header(mom_util.epicor_ewb_rev)
                    else:
                        raise ValueError(f"Invalid header type {header_type}")
                    headers_by_key[header_key] = header

                header.methods_of_manufacture.append(mom)

        headers: List[Header] = list(headers_by_key.values())
        logger.info(f"Created headers for Epicor repeat part with part number {repeat_part_util.repeat_part.part_number}")
        repeat_part_util.repeat_part.headers = headers
        return repeat_part_util

    def get_quote_header(self, mom_util: QuoteMOMUtil) -> Header:
        # customer: Optional[Customer] = self.get_customer(quote_detail.CustomerCustID)
        quote_detail: QuoteDetail = mom_util.epicor_quote_detail
        quote_contact: Optional[QuoteContact] = self.get_quote_contact(quote_detail.QuoteNum)

        quote_detail_header = Header(
            erp_code=get_quote_detail_erp_code(quote_detail),
            type="estimated",
            account=None,  # self.get_account(customer),
            contact=self.get_contact(quote_contact),
            created_date=self.get_valid_date_field(quote_detail),
            public_notes="",
            private_notes=f"{quote_detail.LineDesc}\n{quote_detail.QuoteComment}\n{quote_detail.LineType}",
            add_ons=mom_util.add_ons,
            methods_of_manufacture=[]
        )
        return quote_detail_header

    def get_job_header(self, job_entry: JobEntry) -> Header:
        # customer: Optional[Customer] = self.get_customer(job_entry.CustID)
        quote_contact: Optional[QuoteContact] = self.get_quote_contact(job_entry.QuoteNum)

        job_entry_header = Header(
            erp_code=job_entry.JobNum,
            type="engineered" if job_entry.JobComplete is False else "executed",
            account=None,  # self.get_account(customer),
            contact=self.get_contact(quote_contact),
            created_date=self.get_valid_date_field(job_entry),
            public_notes="",
            private_notes=f"{job_entry.PartDescription}\n{job_entry.PartNumPartDescription}\n{job_entry.ProdCodeDescription}\n{job_entry.CommentText}",
            add_ons=[],
            methods_of_manufacture=[]
        )
        return job_entry_header

    def get_ewb_header(self, ewb_rev: EWBRev) -> Header:
        ewb_header = Header(
            erp_code=construct_ewb_erp_code(ewb_rev),
            type="template",
            account=None,
            contact=None,
            created_date=self.get_valid_date_field(ewb_rev),
            public_notes="",
            private_notes=safe_get(ewb_rev, "RevDescription", ""),
            add_ons=[],
            methods_of_manufacture=[]
        )
        return ewb_header

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        filter_string: str = f"CustID eq {customer_id}"
        try:
            customer: Customer = Customer.get_first(filters={}, params={
                '$filter': filter_string
            })
            return customer
        except:
            return None

    def get_quote_contact(self, quote_num: str) -> Optional[QuoteContact]:
        try:
            quote_header: QuoteHeader = QuoteHeader.get_first(params={
                '$filter': f"QuoteNum eq '{quote_num}'"
            })
            quote_contact: QuoteContact = QuoteContact.get_first(params={
                '$filter': f"QuoteNum eq '{quote_header.QuoteNum}' and CustNum eq '{quote_header.CustNum}'"
            })
            return quote_contact
        except:
            return None

    def get_account(self, customer: Optional[Customer]) -> Optional[Account]:
        if customer is None:
            return None

        account = Account(
            name=customer.Name,
            erp_code=customer.CustID,
            phone=customer.PhoneNum,
            url=customer.CustURL
        )
        return account

    def get_contact(self, quote_contact: Optional[QuoteContact]) -> Optional[Contact]:
        if quote_contact is None:
            return None

        try:
            epicor_contact: EpicorContact = EpicorContact.get_first(params={
                '$filter': f"Company eq '{quote_contact.Company}' and CustNum eq '{quote_contact.CustNum}' and ConNum eq '{quote_contact.ConNum}'"
            })
            contact = Contact(
                email=epicor_contact.EMailAddress,
                first_name=epicor_contact.FirstName,
                last_name=epicor_contact.LastName,
                notes=epicor_contact.Comment,
                phone=epicor_contact.PhoneNum
            )
            return contact
        except:
            return None

    def get_valid_date_field(self, epicor_object: Union[QuoteDetail, JobEntry, EWBRev]):
        quote_date_fields = [
            "DateQuoted",
            "ChangeDate",
            "EntryDate",
            "ExpirationDate"
        ]
        job_date_fields = [
            "CreateDate",
            "StartDate"
            "ClosedDate",
            "JobCompletionDate",
            "LastChangedOn"
        ]
        ewb_rev_date_fields = [
            "EffectiveDate"
        ]
        if isinstance(epicor_object, QuoteDetail):
            date_fields = quote_date_fields
        elif isinstance(epicor_object, EWBRev):
            date_fields = ewb_rev_date_fields
        else:
            date_fields = job_date_fields

        for date_field in date_fields:
            date = safe_get(epicor_object, date_field, None)
            if date not in (None, '', ' '):
                date = date[:10]
                return convert_datetime_to_utc(datetime.strptime(date, '%Y-%m-%d'))
        return convert_datetime_to_utc(datetime.now())
