from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import convert_datetime_to_utc
from baseintegration.utils.repeat_work_objects import Part, Header, Account
from baseintegration.utils.repeat_work_utils import get_headers_from_methods, MOMWrapper
from baseintegration.datamigration import logger
from inforsyteline.models import JobMst, CoitemMst, CustomerMst, CustaddrMst


class HeaderProcessor(BaseImportProcessor):
    def _process(self, repeat_part: Part, methods_of_manufacture: List[MOMWrapper]):
        logger.info(f"Creating repeat part headers from item ID: {repeat_part.part_number}")
        self.source_database = self._importer.source_database
        repeat_part.headers = get_headers_from_methods(
            methods_of_manufacture,
            self.get_template_header, self.get_estimated_header,
            self.get_engineered_header, self.get_executed_header)
        return repeat_part

    def get_template_header(self, template_job: JobMst):
        return Header(
            erp_code=template_job.item.strip(),
            type="template",
            created_date=convert_datetime_to_utc(template_job.createdate),
            private_notes=template_job.description
        )

    def get_estimated_header(self, estimate_item: CoitemMst) -> Header:
        erp_code = f"{estimate_item.co_num}-{estimate_item.co_line}"
        return Header(
            erp_code=erp_code.strip(),
            type="estimated",
            account=self.get_paperless_account_from_cust_num(estimate_item.cust_num),
            created_date=convert_datetime_to_utc(estimate_item.createdate),
            private_notes=estimate_item.description,
            add_ons=[],
        )

    def get_engineered_header(self, job: JobMst) -> Header:
        return Header(
            erp_code=job.job.strip(),
            type="engineered",
            account=self.get_paperless_account_from_cust_num(job.cust_num),
            created_date=convert_datetime_to_utc(job.createdate),
            private_notes=job.description,
            add_ons=[],
        )

    def get_executed_header(self, job: JobMst) -> Header:
        return Header(
            erp_code=job.job.strip(),
            type="executed",
            account=self.get_paperless_account_from_cust_num(job.cust_num),
            created_date=convert_datetime_to_utc(job.createdate),
            private_notes=job.description,
            add_ons=[],
        )

    def get_paperless_account_from_cust_num(self, cust_num: str):
        customer: CustomerMst = CustomerMst.objects.using(self.source_database).filter(cust_num=cust_num).first()
        customer_address: CustaddrMst = CustaddrMst.objects.using(self.source_database)\
            .filter(cust_num=cust_num).first()
        if customer and customer_address:
            return Account(
                name=customer_address.name,
                erp_code=cust_num,
                phone=customer.phone_1,
                url=customer_address.internet_url
            )
