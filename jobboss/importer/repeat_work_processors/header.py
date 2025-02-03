from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import Header
from jobboss.utils.repeat_work_utils import RepeatPartUtilObject, RfqUtil, JobUtil, get_quote_erp_code,\
    get_empty_string_if_none
from baseintegration.utils import safe_get, logger
from typing import List, Union
from datetime import datetime, timezone


class HeaderProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("HeaderProcessor - Attempting to create Headers")
        self.source_database = self._importer.source_database

        repeat_part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        repeat_part.headers = []
        repeat_part.account = []
        repeat_part.contact = []

        self.create_repeat_quote_from_jb_rfq(repeat_part_util_object)
        self.create_repeat_job_from_jb_job(repeat_part_util_object)
        self.create_header_from_jb_job_hardware(repeat_part_util_object)
        self.create_header_from_jb_quote_hardware(repeat_part_util_object)

        return repeat_part_util_object

    def create_repeat_quote_from_jb_rfq(self, repeat_part_util_object: RepeatPartUtilObject):
        """
        Creates the "quote header" information for each of the unique part number's unique quote header instances.
        Handles for the possibility of the same unique part number appearing twice on the same quote header.
        """
        logger.info("Creating quote header from JobBOSS RFQ.")

        jb_quotes_list = repeat_part_util_object.jb_quotes_queryset
        unique_rfq_dict = self.get_unique_rfq_list(jb_quotes_list)

        for jb_rfq, jb_quote_items in unique_rfq_dict.items():
            # Create RfQUtil to prevent needing to query the Rfq table later.
            rfq_util = RfqUtil(jb_rfq)
            rfq_util.jb_quotes = jb_quote_items
            repeat_part_util_object.rfq_utils.append(rfq_util)

            # Iterate quote items to create a Paperless Header object for each
            for jb_quote in jb_quote_items:
                quote_header = Header(
                    erp_code=get_quote_erp_code(jb_quote),
                    type=self.get_header_type_from_quote_or_job(jb_quote),
                    created_date=self.convert_datetime_to_utc(safe_get(jb_rfq, "quote_date", None)),
                    public_notes=get_empty_string_if_none(safe_get(jb_quote, "comment", None)),
                    private_notes=get_empty_string_if_none(safe_get(jb_quote, "note_text", None)),
                    add_ons=[],
                )
                rfq_util.repeat_part_headers.append(quote_header)

    def create_repeat_job_from_jb_job(self, repeat_part_util_object: RepeatPartUtilObject):
        """
        Creates the "Job" information for each unique part number's job instances.
        """
        logger.info("Creating quote header from JobBOSS Job.")

        for jb_job in repeat_part_util_object.jb_jobs_queryset:
            repeat_job = Header(
                erp_code=str(jb_job.top_lvl_job),
                type=self.get_header_type_from_quote_or_job(jb_job),
                created_date=self.convert_datetime_to_utc(safe_get(jb_job, "order_date", None)),
                public_notes=get_empty_string_if_none(safe_get(jb_job, "comment", None)),
                private_notes=get_empty_string_if_none(safe_get(jb_job, "note_text", None)),
                add_ons=[],
            )
            # Jobs will only ever have one header
            job_util = JobUtil(jb_job, repeat_job)
            repeat_part_util_object.job_utils.append(job_util)

    def create_header_from_jb_quote_hardware(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("Creating header from quote hardware.")

        for jb_hardware in repeat_part_util_object.jb_quote_hardware_queryset:
            jb_hardware: jb.QuoteReq = jb_hardware
            jb_quote: jb.Quote = jb_hardware.quote
            jb_rfq = jb.Rfq.objects.using(self.source_database).filter(rfq=jb_quote.rfq).first()

            if not jb_rfq:
                logger.info("Quote hardware not associated with an RFQ, not creating header")
                continue

            quote_header = Header(
                erp_code=get_quote_erp_code(jb_quote),
                type=self.get_header_type_from_quote_or_job(jb_quote),
                created_date=self.convert_datetime_to_utc(safe_get(jb_rfq, "quote_date", None)),
                public_notes=get_empty_string_if_none(safe_get(jb_quote, "comment", None)),
                private_notes=get_empty_string_if_none(safe_get(jb_quote, "note_text", None)),
                add_ons=[],
            )
            rfq_util = RfqUtil(jb_rfq)
            rfq_util.repeat_part_headers.append(quote_header)
            repeat_part_util_object.rfq_utils.append(rfq_util)

    def create_header_from_jb_job_hardware(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("Creating header from job hardware.")
        for jb_hardware in repeat_part_util_object.jb_job_hardware_queryset:
            jb_hardware: jb.MaterialReq = jb_hardware
            jb_job: jb.Job = jb_hardware.job

            repeat_job = Header(
                erp_code=str(jb_job.top_lvl_job),
                type=self.get_header_type_from_quote_or_job(jb_job),
                created_date=self.convert_datetime_to_utc(safe_get(jb_job, "order_date", None)),
                public_notes=get_empty_string_if_none(safe_get(jb_job, "comment", None)),
                private_notes=get_empty_string_if_none(safe_get(jb_job, "note_text", None)),
                add_ons=[],
            )
            # Jobs will only ever have one header
            job_util = JobUtil(jb_job, repeat_job)
            repeat_part_util_object.job_utils.append(job_util)

    def get_unique_rfq_list(self, jb_quotes_list: List[jb.Quote]):
        """
        If a quote appears more than once on a single RFQ, we want all of those quotes to be HeaderItems on the same
        RFQ/Header, instead of having a duplicate RFQ/Header.

        This function ensures that if two jb "Quote" objects return the same jb RFQ object twice, it will be appended to
        a list belonging to the RFQ, instead of processing another RFQ as a duplicate quote header.
        """
        unique_rfq_dict = {}

        for jb_quote in jb_quotes_list:
            jb_rfq = jb.Rfq.objects.using(self.source_database).filter(rfq=jb_quote.rfq).first()
            if unique_rfq_dict.get(jb_rfq, False):
                unique_rfq_dict[jb_rfq].append(jb_quote)
            else:
                unique_rfq_dict[jb_rfq] = [jb_quote]

        return unique_rfq_dict

    def convert_datetime_to_utc(self, datetime_object):
        if not isinstance(datetime_object, datetime):
            return None
        utc_timestamp = datetime_object.replace(tzinfo=timezone.utc).timestamp()
        return int(utc_timestamp)

    def get_header_type_from_quote_or_job(self, quote_or_job_object: Union[jb.Quote, jb.Job]) -> str:
        object_status = safe_get(quote_or_job_object, "status", None)
        if object_status and object_status.lower() == "template":
            return "template"
        elif isinstance(quote_or_job_object, jb.Quote):
            return "estimated"
        return "engineered"
