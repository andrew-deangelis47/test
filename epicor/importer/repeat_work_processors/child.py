from baseintegration.utils import logger
from typing import List
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Child
from epicor.quote import QuoteDetail, QuoteAssembly
from epicor.job import JobEntry, JobAssembly
from epicor.engineering_workbench import EWBRev, EWBMaterial
from epicor.importer.utils import (
    RepeatPartUtilObject,
    QuoteMOMUtil,
    JobMOMUtil,
    EWBMOMUtil,
    construct_ewb_erp_code
)
from epicor.importer.epicor_client_cache import EpicorClientCache


class ChildProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info("ChildProcessor - Attempting to create Children")
        self.processed_children_list = self._importer.processed_children_list

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.children = self._get_quote_mom_children(quote_mom_util, repeat_part_util_object)

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.children = self._get_job_mom_children(job_mom_util, repeat_part_util_object)

        for ewb_mom_util in repeat_part_util_object.ewb_mom_utils:
            ewb_mom_util: EWBMOMUtil = ewb_mom_util
            ewb_mom_util.mom.children = self._get_ewb_mom_children(ewb_mom_util, repeat_part_util_object)

        return repeat_part_util_object

    def _get_quote_mom_children(self, quote_mom_util: QuoteMOMUtil, repeat_part_util_object: RepeatPartUtilObject
                                ) -> List[Child]:
        children: List[Child] = []
        epicor_quote_detail: QuoteDetail = quote_mom_util.epicor_quote_detail
        quote_id = self.get_unique_quote_id(str(epicor_quote_detail.QuoteNum), str(epicor_quote_detail.QuoteLine))
        children_quote_assemblies: List[QuoteAssembly] = repeat_part_util_object.epicor_child_quote_assemblies.get(
            quote_id, [])
        child_client_cache = repeat_part_util_object.epicor_client_cache

        for epicor_child in children_quote_assemblies:
            if (epicor_child.AssemblySeq == 0 and epicor_child.ParentAssemblySeq == 0) or (
                    quote_mom_util.quote_assembly.BomLevel >= epicor_child.BomLevel
            ):
                # The root component's parent assembly sequence is itself
                continue

            epicor_child: QuoteAssembly = epicor_child
            child_part_number = epicor_child.PartNum
            child_revision = epicor_child.RevisionNum
            self.process_child_repeat_part(f"{child_part_number}:_:{child_revision}", child_client_cache)

            child = Child(
                part_number=child_part_number,
                revision=child_revision,
                qty_per_parent=int(epicor_child.QtyPer)
            )
            children.append(child)

        return children

    def _get_job_mom_children(self, job_mom_util: JobMOMUtil, repeat_part_util_object: RepeatPartUtilObject) -> List[Child]:
        children: List[Child] = []
        epicor_job: JobEntry = job_mom_util.epicor_job
        children_job_assemblies: List[JobAssembly] = repeat_part_util_object.epicor_child_job_assemblies.get(
            epicor_job.JobNum, [])
        child_client_cache = repeat_part_util_object.epicor_client_cache

        for epicor_child in children_job_assemblies:
            epicor_child: JobAssembly = epicor_child
            if epicor_child.AssemblySeq == 0 or job_mom_util.job_assembly.BomLevel >= epicor_child.BomLevel:
                # The root component's parent assembly sequence is itself
                continue

            child_part_number = epicor_child.PartNum
            child_revision = epicor_child.RevisionNum
            self.process_child_repeat_part(f"{child_part_number}:_:{child_revision}", child_client_cache)

            child = Child(
                part_number=child_part_number,
                revision=child_revision,
                qty_per_parent=int(epicor_child.QtyPer)
            )
            children.append(child)

        return children

    def _get_ewb_mom_children(self, ewb_mom_util: EWBMOMUtil, repeat_part_util_object: RepeatPartUtilObject) -> List[Child]:
        children: List[Child] = []
        epicor_ewb_rev: EWBRev = ewb_mom_util.epicor_ewb_rev
        children_ewb_materials: List[EWBMaterial] = repeat_part_util_object.epicor_child_ewb_assemblies.get(
            construct_ewb_erp_code(epicor_ewb_rev), [])
        child_client_cache = repeat_part_util_object.epicor_client_cache

        for epicor_child in children_ewb_materials:
            epicor_child: EWBMaterial = epicor_child

            child_part_number = epicor_child.MtlPartNum
            child_revision = epicor_child.MtlRevisionNum
            self.process_child_repeat_part(f"{child_part_number}:_:{child_revision}", child_client_cache)

            child = Child(
                part_number=child_part_number,
                revision=child_revision,
                qty_per_parent=int(epicor_child.QtyPer)
            )
            children.append(child)

        return children

    def process_child_repeat_part(self, child_part_number: str, child_client_cache: EpicorClientCache):
        if child_part_number:
            logger.info(f"Creating child parts for {child_part_number}")
            self._importer._process_repeat_part(child_part_number, is_root=False, child_client_cache=child_client_cache)

    def get_unique_quote_id(self, quote_num: str, quote_line: str) -> str:
        return f"{quote_num}:_:{quote_line}"
