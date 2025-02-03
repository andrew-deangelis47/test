from datetime import datetime, timezone
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import Part
from jobboss.utils.repeat_work_utils import get_repeat_part_type_from_jb_quote_or_job, \
    get_empty_string_if_none, RepeatPartUtilObject
from typing import Union


class RepeatPartProcessor(BaseImportProcessor):

    def _process(self, repeat_part_number: Union[str, tuple[str, str]]):
        part_number, revision = self.deconstruct_part_number_and_revision(repeat_part_number)
        logger.info(f"\n\nProcessing repeat part number: {part_number} revision: {revision}")
        source_database = self._importer.source_database

        # Execute all queries to identify where the part exists
        jb_quotes_queryset = jb.Quote.objects.using(source_database).filter(part_number=part_number, rev=revision)
        jb_jobs_queryset = jb.Job.objects.using(source_database).filter(part_number=part_number, rev=revision)
        # Note hardware materials do not have revisions
        jb_quote_hardware_queryset = jb.QuoteReq.objects.using(source_database).filter(material=part_number)
        jb_job_hardware_queryset = jb.MaterialReq.objects.using(source_database).filter(material=part_number)

        # Instantiate util object to store important information for later use
        repeat_part_util_object = RepeatPartUtilObject(
            jb_quotes_queryset=jb_quotes_queryset,
            jb_jobs_queryset=jb_jobs_queryset,
            jb_quote_hardware_queryset=jb_quote_hardware_queryset,
            jb_job_hardware_queryset=jb_job_hardware_queryset,
        )

        if isinstance(repeat_part_util_object.origin_jb_part, jb.Quote):
            logger.info("Creating repeat part from JobBOSS Quote.")
            repeat_part = self.create_repeat_part_from_jb_quote(repeat_part_util_object.origin_jb_part)
        elif isinstance(repeat_part_util_object.origin_jb_part, jb.Job):
            logger.info("Creating repeat part from JobBOSS Job.")
            repeat_part = self.create_repeat_part_from_jb_job(repeat_part_util_object.origin_jb_part)
        elif isinstance(repeat_part_util_object.origin_jb_part, jb.QuoteReq):
            logger.info("Creating repeat part from JobBOSS QuoteReq.")
            repeat_part = self.create_repeat_part_from_jb_quote_hardware(repeat_part_util_object.origin_jb_part)
        elif isinstance(repeat_part_util_object.origin_jb_part, jb.MaterialReq):
            logger.info("Creating repeat part from JobBOSS MaterialReq.")
            repeat_part = self.create_repeat_part_from_jb_job_hardware(repeat_part_util_object.origin_jb_part)
        else:
            logger.info(f"No records found for part number: '{part_number}' rev: '{revision}'")
            raise ValueError(f"No records found for part number: '{part_number}' rev: '{revision}'")

        repeat_part_util_object.repeat_part = repeat_part

        return repeat_part_util_object

    def deconstruct_part_number_and_revision(self, repeat_part_number: Union[str, tuple[str, str]]):
        # Check if part number and rev were both supplied
        if isinstance(repeat_part_number, tuple):
            return repeat_part_number

        # Only part number is supplied, so we need to find the first matching rev
        source_database = self._importer.source_database

        jb_quote: jb.Quote = jb.Quote.objects.using(source_database).filter(part_number=repeat_part_number).first()
        if jb_quote:
            return repeat_part_number, jb_quote.rev

        jb_job = jb.Job.objects.using(source_database).filter(part_number=repeat_part_number).first()
        if jb_job:
            return repeat_part_number, jb_job.rev

        return repeat_part_number, ""

    def create_repeat_part_from_jb_quote(self, jb_quote: jb.Quote):
        logger.info(f"Creating repeat part from Jobboss quote ID: {jb_quote.quote}")

        repeat_part = Part(
            part_number=str(jb_quote.part_number),
            revision=get_empty_string_if_none(jb_quote.rev),
            type=get_repeat_part_type_from_jb_quote_or_job(jb_quote),
            erp_name="jobboss",
            is_root=self.get_is_root(jb_quote),
            import_date=self.convert_datetime_to_utc(datetime.now()),
            filename=str(jb_quote.part_number),
            description=get_empty_string_if_none(jb_quote.description)
        )

        return repeat_part

    def create_repeat_part_from_jb_job(self, jb_job: jb.Job):
        logger.info(f"Creating repeat part from Jobboss job ID: {jb_job.job}")
        repeat_part = Part(
            part_number=str(jb_job.part_number),
            revision=get_empty_string_if_none(jb_job.rev),
            type=get_repeat_part_type_from_jb_quote_or_job(jb_job),
            erp_name="jobboss",
            is_root=self.get_is_root(jb_job),
            import_date=self.convert_datetime_to_utc(datetime.now()),
            filename=str(jb_job.part_number),
            description=get_empty_string_if_none(jb_job.description)
        )

        return repeat_part

    def get_is_root(self, jb_object: Union[jb.Job, jb.Quote]) -> bool:
        if jb_object.assembly_level == 0:
            return True
        return False

    def create_repeat_part_from_jb_quote_hardware(self, jb_quote_req: jb.QuoteReq):
        logger.info(f"Creating repeat part from Jobboss QuoteReq ID: {jb_quote_req.material}")
        repeat_part = Part(
            part_number=str(jb_quote_req.material),
            revision="",  # Hardware materials don't have revisions in JB
            type="purchased",
            erp_name="jobboss",
            import_date=self.convert_datetime_to_utc(datetime.now()),
            filename=str(jb_quote_req.material),
            description=get_empty_string_if_none(jb_quote_req.description)
        )

        return repeat_part

    def create_repeat_part_from_jb_job_hardware(self, jb_material_req: jb.MaterialReq):
        logger.info(f"Creating repeat part from Jobboss QuoteReq ID: {jb_material_req.material}")
        repeat_part = Part(
            part_number=str(jb_material_req.material),
            revision="",  # Hardware materials don't have revisions in JB
            type="purchased",
            erp_name="jobboss",
            import_date=self.convert_datetime_to_utc(datetime.now()),
            filename=str(jb_material_req.material),
            description=get_empty_string_if_none(jb_material_req.description)
        )

        return repeat_part

    def convert_datetime_to_utc(self, datetime_object):
        if not isinstance(datetime_object, datetime):
            return None
        utc_timestamp = datetime_object.replace(tzinfo=timezone.utc).timestamp()
        return int(utc_timestamp)
