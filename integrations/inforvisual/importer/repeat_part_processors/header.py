from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_utils import MOMWrapper, get_headers_from_methods
from inforvisual.models import (
    QuoteLine as InforVisualQuoteLine,
    Quote as InforVisualQuote,
    WorkOrder as InforVisualWorkOrder,
    Customer as InforVisualCustomer,
)
from baseintegration.utils.repeat_work_objects import Header, Account, Contact
from typing import Optional, List
from baseintegration.datamigration import logger


class HeaderImportProcessor(BaseImportProcessor):
    def _process(self, repeat_part_id: str, methods_of_manufacture: List[MOMWrapper]) -> list:
        logger.info(f"Creating repeat part headers from item ID: {repeat_part_id}")
        self.source_database = self._importer.source_database
        self.headers: List[Header] = []
        self.headers = get_headers_from_methods(
            methods_of_manufacture,
            get_template_header=self.get_template_work_order_header,
            get_estimated_header=self.get_quote_header,
            get_engineered_header=self.get_engineered_work_order_header,
            get_executed_header=self.get_executed_work_order_header)
        return self.headers

    def get_template_work_order_header(self, work_order: InforVisualWorkOrder) -> Header:
        return Header(
            type="template",
            erp_code=self.get_work_order_erp_code(work_order),
            created_date=int(work_order.create_date.timestamp()),
            account=None,
            contact=None,
            private_notes=work_order.user_1,  # TODO: Should we get notes from WorkorderBinary or SriWorkorderBinary?
        )

    def get_quote_header(self, quote_line: InforVisualQuoteLine) -> Header:
        corresponding_quote = quote_line.quote
        return Header(
            type="estimated",
            erp_code=f"{corresponding_quote.id}-{quote_line.line_no}",
            created_date=int(quote_line.create_date.timestamp()),
            account=self.get_account(corresponding_quote.customer),
            contact=self.get_contact_from_quote(corresponding_quote),
        )

    def get_engineered_work_order_header(self, work_order: InforVisualWorkOrder) -> Header:
        return Header(
            type="engineered",
            erp_code=self.get_work_order_erp_code(work_order),
            created_date=int(work_order.create_date.timestamp()),
            account=None,
            contact=None,
            private_notes=work_order.user_1,
        )

    def get_executed_work_order_header(self, work_order: InforVisualWorkOrder) -> Header:
        return Header(
            type="executed",
            erp_code=self.get_work_order_erp_code(work_order),
            created_date=int(work_order.create_date.timestamp()),
            account=None,
            contact=None,
            private_notes=work_order.user_1,
        )

    def get_account(self, cust: Optional[InforVisualCustomer]) -> Optional[Account]:
        if cust and cust.name:
            return Account(
                name=cust.name,
                erp_code=cust.id,
                phone=str(cust.contact_phone),
                url=str(cust.web_url),
            )

    def get_contact_from_quote(self, quote: InforVisualQuote) -> Optional[Contact]:
        if quote.contact_email:
            return Contact(
                first_name=quote.contact_first_name,
                last_name=quote.contact_last_name,
                email=quote.contact_email,
                phone=quote.contact_phone,
            )

    def get_work_order_erp_code(self, work_order: InforVisualWorkOrder) -> str:
        erp_code = f"{work_order.base_id}/{work_order.lot_id}"
        if work_order.split_id != '0':
            erp_code += f"-{work_order.split_id}"
        return erp_code
