from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import Child, Part, Header
from jobboss.utils.repeat_work_utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, get_empty_string_if_none, \
    get_quote_erp_code
from baseintegration.utils import safe_get, logger
from typing import Union, List


class ChildProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject, create_child_parts: bool = False):
        self.create_child_parts = create_child_parts
        self.processed_children_list = self._importer.processed_children_list
        self.source_database = self._importer.source_database
        logger.info("ChildProcessor - Attempting to create Children")

        repeat_part: Part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.children = []
            self.get_quote_mom_children(quote_mom_util)
            self.get_mom_unit_cost(quote_mom_util, repeat_part)
            final_mom = self.build_json_mom_from_util(quote_mom_util)
            headers: List[Header] = repeat_part.headers
            for header in headers:
                if header.erp_code == get_quote_erp_code(quote_mom_util.jb_quote):
                    header.methods_of_manufacture.append(final_mom.to_json())

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.children = []
            self.get_job_mom_children(job_mom_util)
            self.get_mom_unit_cost(job_mom_util, repeat_part)
            final_mom = self.build_json_mom_from_util(job_mom_util)
            headers: List[Header] = repeat_part.headers
            for header in headers:
                if header.erp_code == job_mom_util.jb_job.top_lvl_job:
                    header.methods_of_manufacture.append(final_mom.to_json())

        return repeat_part.to_json()

    def build_json_mom_from_util(self, mom_util: Union[QuoteMOMUtil, JobMOMUtil]):
        for op in mom_util.operations:
            mom_util.mom.operations.append(op.to_json())
        for mat in mom_util.required_materials:
            mom_util.mom.required_materials.append(mat.to_json())
        for child in mom_util.children:
            mom_util.mom.children.append(child.to_json())
        return mom_util.mom

    def get_quote_mom_children(self, quote_mom_util: QuoteMOMUtil):
        jb_quote: jb.Quote = quote_mom_util.jb_quote
        logger.info(f"Attempting to create MOM Children for JobBOSS Quote: {jb_quote.quote}")
        parent_child_relationship = jb.BillOfQuotes.objects.using(self.source_database).filter(relationship_type="Component", parent_quote=jb_quote.quote)

        for relationship in parent_child_relationship:  # Each relationship is a child of THIS quote

            # Follow each relationship up the tree, multiplying by qty per parent until you reach the root
            # multiply that number by the root and you have your "true" qty
            logger.info("Attempting to recursively get the true assembly quantity.")
            self.root_component_multiplier = relationship.relationship_qty

            jb_child_quote: jb.Quote = relationship.component_quote
            child_part_number = safe_get(jb_child_quote, "part_number", None)
            child_rev_sql = safe_get(jb_child_quote, "rev", None)
            child_revision = get_empty_string_if_none(child_rev_sql)
            self.process_child_repeat_part(child_part_number, child_rev_sql)

            child = Child(
                part_number=child_part_number,
                revision=child_revision,
                qty_per_parent=int(relationship.relationship_qty),
            )
            quote_mom_util.children.append(child)

        child_purchased_components = jb.QuoteReq.objects.filter(quote=jb_quote.quote).exclude(type="R").all()
        for pc in child_purchased_components:
            child_part_number = safe_get(pc, "material", None)
            self.process_child_repeat_part(child_part_number)

            child = Child(
                part_number=child_part_number,
                revision="",
                qty_per_parent=int(safe_get(pc, "quantity_per", None)),
            )
            quote_mom_util.children.append(child)

        if len(parent_child_relationship) == 0 and len(child_purchased_components) == 0:
            self._importer.processed_children_list = []

    def get_job_mom_children(self, job_mom_util: JobMOMUtil):
        jb_job = job_mom_util.jb_job
        logger.info(f"Attempting to create MOM Children for JobBOSS Job: {jb_job.job}")
        parent_child_relationship = jb.BillOfJobs.objects.using(self.source_database).filter(relationship_type="Component", parent_job=jb_job.job)

        for relationship in parent_child_relationship:
            jb_child_job = relationship.component_job
            child_part_number = safe_get(jb_child_job, "part_number", None)
            child_rev_sql = safe_get(jb_child_job, "rev", None)
            child_revision = get_empty_string_if_none(child_rev_sql)
            self.process_child_repeat_part(child_part_number, child_rev_sql)

            child = Child(
                part_number=child_part_number,
                revision=child_revision,
                qty_per_parent=int(relationship.relationship_qty),
            )
            job_mom_util.children.append(child)

        child_purchased_components = jb.MaterialReq.objects.filter(job=jb_job.job).exclude(type="R").all()
        for pc in child_purchased_components:
            child_part_number = safe_get(pc, "material", None)
            self.process_child_repeat_part(child_part_number)

            child = Child(
                part_number=child_part_number,
                revision="",
                qty_per_parent=int(safe_get(pc, "quantity_per", None)),
            )
            job_mom_util.children.append(child)

            if len(parent_child_relationship) == 0 and len(child_purchased_components) == 0:
                self._importer.processed_children_list = []

    def get_mom_unit_cost(self, mom_util: Union[QuoteMOMUtil, JobMOMUtil], repeat_part: Part):
        logger.info("Summing MOM costs.")
        mom = mom_util.mom
        total_cost = 0
        for material in mom.required_materials:
            total_cost += material.total_cost
        for operation in mom.operations:
            total_cost += operation.total_cost
        mom.unit_cost = total_cost / mom.requested_qty if mom.requested_qty > 0 else 0

        if not repeat_part.is_root:
            # This allows for non-root parts to show costs in the costing preview in the Paperless UI
            mom.unit_price = mom.unit_cost
            mom.total_price = total_cost

    def process_child_repeat_part(self, child_part_number, child_rev=None):
        if self.create_child_parts and child_part_number:
            logger.info(f"Creating child parts for {child_part_number}")
            self._importer._process_repeat_part(
                (child_part_number, child_rev),
                create_child_parts=True,
            )
