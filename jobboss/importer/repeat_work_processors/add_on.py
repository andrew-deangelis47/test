from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import AddOn, Part
from jobboss.utils.repeat_work_utils import get_empty_string_if_none, RepeatPartUtilObject, RfqUtil, JobUtil
from baseintegration.utils import safe_get
from baseintegration.utils import logger


class AddOnProcessor(BaseImportProcessor):
    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("AddOnProcessor - Attempting to create AddOns")
        self.source_database = self._importer.source_database

        repeat_part: Part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        for rfq_util in repeat_part_util_object.rfq_utils:
            rfq_util: RfqUtil = rfq_util
            for header in rfq_util.repeat_part_headers:
                header.add_ons = self.create_quote_add_ons(rfq_util)
                repeat_part.headers.append(header)

        for job_util in repeat_part_util_object.job_utils:
            job_util: JobUtil = job_util
            job_util.repeat_part_header.add_ons = self.create_job_add_ons(job_util)
            repeat_part.headers.append(job_util.repeat_part_header)

        return repeat_part_util_object

    def create_quote_add_ons(self, rfq_util: RfqUtil):
        jb_rfq_number = rfq_util.jb_rfq.rfq
        logger.info(f"Creating AddOn(s) from JobBOSS Quote: {jb_rfq_number}")
        add_ons = []
        jb_addl_charges = jb.QuoteAddlCharge.objects.using(self.source_database).filter(quote=jb_rfq_number)
        for addl_charge in jb_addl_charges:
            add_on = AddOn(
                is_required=True,
                name=addl_charge.description if addl_charge.description else "ADD ON",
                notes=get_empty_string_if_none(safe_get(addl_charge, "note_text", None)),
                unit_price=float(safe_get(addl_charge, "est_price", 0)),
                use_component_quantities=False,
            )
            add_ons.append(add_on.to_json())
        return add_ons

    def create_job_add_ons(self, job_util: JobUtil):
        jb_job_number = job_util.jb_job.job
        logger.info(f"Creating AddOn(s) from JobBOSS Job: {jb_job_number}")
        add_ons = []
        jb_addl_charges = jb.AdditionalCharge.objects.using(self.source_database).filter(job=jb_job_number)
        for addl_charge in jb_addl_charges:
            add_on = AddOn(
                is_required=True,
                name=addl_charge.description if addl_charge.description else "ADD ON",
                notes=get_empty_string_if_none(safe_get(addl_charge, "note_text", None)),
                unit_price=float(safe_get(addl_charge, "est_price", 0)),
                use_component_quantities=False,
            )
            add_ons.append(add_on.to_json())
        return add_ons
