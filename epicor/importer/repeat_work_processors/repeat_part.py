from typing import List, Tuple, Union, Dict, Set
import datetime
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Part as RepeatPart
from epicor.job import JobEntry, JobAssembly
from epicor.engineering_workbench import EWBRev, EWBMaterial
from epicor.quote import QuoteDetail, QuoteAssembly, QuoteDetailSearch
from epicor.importer.utils import RepeatPartUtilObject, get_ewb_unique_identifier, split_entity_id
from epicor.importer.epicor_client_cache import EpicorClientCache
from epicor.importer.epicor_client_cache_util import create_epicor_client_cache
from epicor.importer.utils import create_id_separated_part_number_and_revision_string, construct_ewb_erp_code
from operator import itemgetter


class RepeatPartImportProcessor(BaseImportProcessor):

    def _process(self, repeat_part_number: str, epicor_client_cache: EpicorClientCache, bulk=False,
                 is_root=True) -> Union[RepeatPartUtilObject, None]:
        try:
            part_num, revision_num = split_entity_id(repeat_part_number)
        except ValueError:
            return None
        logger.info(f"Processing repeat work part from Epicor with part number {part_num} and revision number"
                    f" {revision_num}")

        # Create Epicor client cache to ensure all nested entities can be found
        if epicor_client_cache is None and is_root is True:
            epicor_client_cache = self.create_cache_for_single_part_number(repeat_part_number, part_num, revision_num)

        job_entries, job_assemblies, child_job_assembly_dict = self.get_job_entries_from_cached_data(
            epicor_client_cache, part_num, revision_num)
        quote_assemblies, quote_details = self.get_quote_assemblies_from_cached_data(
            epicor_client_cache, part_num, revision_num)
        child_quote_assembly_dict = self.get_quote_child_assemblies_from_cached_data(
            epicor_client_cache, quote_assemblies)
        ewb_revs, ewb_assemblies, child_ewb_assembly_dict = self.get_ewb_revs_from_cached_data(
            epicor_client_cache, part_num, revision_num)

        is_root = self.part_is_root(job_entries, quote_details, ewb_revs)
        repeat_part_type = self.get_repeat_part_type(child_job_assembly_dict, child_quote_assembly_dict,
                                                     child_ewb_assembly_dict)

        repeat_part = RepeatPart(
            part_number=part_num,
            revision=revision_num,
            erp_name="epicor",
            is_root=is_root,
            import_date=int(datetime.datetime.now().timestamp()),
            headers=[],  # Headers are added in subsequent processor
            type=repeat_part_type,
            size_x=0.0,
            size_y=0.0,
            size_z=0.0,
            area=0.0,
            thickness=0.0,
            filename=part_num
        )

        # Create the util part with all the possible instances in which the specified part number exists
        repeat_part_util = RepeatPartUtilObject(repeat_part, job_entries, job_assemblies,
                                                child_job_assembly_dict, quote_details, quote_assemblies,
                                                child_quote_assembly_dict, ewb_revs, ewb_assemblies,
                                                child_ewb_assembly_dict)
        if repeat_part_util.epicor_client_cache is None:
            repeat_part_util.epicor_client_cache = epicor_client_cache

        logger.info(f"Created repeat part object for Epicor part number: {part_num}, revision number {revision_num}")
        return repeat_part_util

    def part_is_root(self, job_entries: List[JobEntry], quote_details: List[QuoteDetail], ewb_revs: List[EWBRev]):
        if len(job_entries) > 0 or len(quote_details) > 0 or len(ewb_revs) > 0:
            # If the part number appears as a "line item" or EWB revision, it is treated as root for UI search purposes
            # A root part number will always have a line item/EWB revision, therefore, all other instances are non-root
            return True
        return False

    def get_repeat_part_type(self, child_job_assembly_dict: dict, child_quote_assembly_dict: dict,
                             child_ewb_assembly_dict: dict):
        """
        There is always 1 assembly object per quote/job. Only if there are multiple belonging to the same quote or job
        instance will the part be considered an assembly. Purchased components are treated as material operations.
        """
        for key, items in child_job_assembly_dict.items():
            if len(items) > 1:
                return "assembled"
        for key, items in child_quote_assembly_dict.items():
            if len(items) > 1:
                return "assembled"
        for key, items in child_ewb_assembly_dict.items():
            if len(items) > 1:
                return "assembled"
        return "manufactured"

    def get_child_job_assembly_mapping(self, job_assemblies: List[JobAssembly]) -> dict:
        child_job_assembly_dict: dict = {}

        for job_assembly in job_assemblies:
            job_num: str = job_assembly.JobNum
            child_job_assemblies: List[JobAssembly] = JobAssembly.get_child_job_assemblies_by_parent_assembly(
                job_num, job_assembly.AssemblySeq)
            child_job_assembly_dict[job_num] = child_job_assemblies

        return child_job_assembly_dict

    def get_child_quote_assembly_mapping(self, quote_assemblies: List[QuoteAssembly]) -> dict:
        child_quote_assembly_dict: dict = {}

        for quote_assemby in quote_assemblies:
            quote_num: str = quote_assemby.QuoteNum
            quote_line: int = quote_assemby.QuoteLine
            child_job_assemblies: List[QuoteAssembly] = QuoteAssembly.get_child_quote_assemblies_by_parent_assembly(
                quote_num, quote_line, quote_assemby.AssemblySeq)
            child_quote_assembly_dict[quote_num] = child_job_assemblies

        return child_quote_assembly_dict

    def get_child_ewb_assembly_mapping(self, ewb_assemblies: List[EWBMaterial]) -> dict:
        child_ewb_assembly_dict: dict = {}

        for ewb_assembly in ewb_assemblies:
            ewb_part_number: str = ewb_assembly.PartNum
            ewb_revision: str = ewb_assembly.RevisionNum
            child_job_assemblies: List[EWBMaterial] = EWBMaterial.get_child_ewb_assemblies_by_parent_assembly(
                ewb_part_number, ewb_revision, ewb_assembly.MtlSeq)
            child_ewb_assembly_dict[get_ewb_unique_identifier(ewb_part_number, ewb_revision)] = child_job_assemblies

        return child_ewb_assembly_dict

    def get_job_entries_from_cached_data(self, epicor_client_cache: EpicorClientCache, part_num: str, revision: str
                                         ) -> Tuple[List[JobEntry], List[JobAssembly], Dict[str, List[JobAssembly]]]:
        job_entries_list: List[JobEntry] = []
        job_assemblies_list: List[JobAssembly] = []
        job_child_assembly_index: Dict[str, List[JobAssembly]] = {}

        for i, job_entry in enumerate(epicor_client_cache.nested_job_entry_cache):

            # Add relevant jobs for this particular part number in processing
            if job_entry.PartNum == part_num and job_entry.RevisionNum == revision:
                job_entries_list.append(job_entry)

            # Add relevant job assemblies for this particular part number in processing
            for job_assembly in job_entry.JobAsmbls:
                if job_assembly.PartNum == part_num and job_assembly.RevisionNum == revision:
                    job_assemblies_list.append(job_assembly)

                    # Determine which of the job's assemblies are direct children of the "in-process" assembly
                    for child_assembly in job_entry.JobAsmbls:
                        if (child_assembly.Parent == job_assembly.AssemblySeq) and (child_assembly.AssemblySeq > 0)\
                                and (child_assembly.BomLevel > job_assembly.BomLevel):
                            if job_child_assembly_index.get(job_assembly.JobNum, None) is None:
                                job_child_assembly_index[job_assembly.JobNum] = [child_assembly]
                            else:
                                job_child_assembly_index[job_assembly.JobNum].append(child_assembly)

        return job_entries_list, job_assemblies_list, job_child_assembly_index

    def get_ewb_revs_from_cached_data(self, epicor_client_cache: EpicorClientCache, part_num: str, revision: str
                                      ) -> Tuple[List[EWBRev], List[EWBMaterial], Dict[str, List[EWBMaterial]]]:
        ewb_revs_list: List[EWBRev] = []
        ewb_assemblies_list: List[EWBMaterial] = []
        child_ewb_assembly_dict: Dict[str, List[EWBMaterial]] = {}
        for i, ewb_rev in enumerate(epicor_client_cache.nested_ewb_rev_cache):

            # Add relevant EWB revs for this particular part number in processing
            if ewb_rev.PartNum == part_num and ewb_rev.RevisionNum == revision:
                if self.check_if_ewb_rev_is_assembly(ewb_rev) is True:
                    return ewb_revs_list, ewb_assemblies_list, child_ewb_assembly_dict
                ewb_revs_list.append(ewb_rev)

            # Add relevant EWB assemblies for this particular part number in processing
            for ewb_assembly in ewb_rev.ECOMtls:
                is_assembly = True if ewb_assembly.PullAsAsm is True and ewb_assembly.ViewAsAsm is True else False
                if is_assembly:
                    ewb_assemblies_list.append(ewb_assembly)
                    if child_ewb_assembly_dict.get(construct_ewb_erp_code(ewb_rev), None) is None:
                        child_ewb_assembly_dict[construct_ewb_erp_code(ewb_rev)] = [ewb_assembly]
                    else:
                        child_ewb_assembly_dict[construct_ewb_erp_code(ewb_rev)].append(ewb_assembly)

        return ewb_revs_list, ewb_assemblies_list, child_ewb_assembly_dict

    def get_quote_assemblies_from_cached_data(self, epicor_client_cache: EpicorClientCache, part_num: str, revision: str
                                              ) -> Tuple[List[QuoteAssembly], List[QuoteDetail]]:
        quote_assemblies_list: List[QuoteAssembly] = []
        for quote_assembly in epicor_client_cache.nested_quote_assembly_cache:
            if quote_assembly.PartNum == part_num and quote_assembly.RevisionNum == revision:
                quote_assemblies_list.append(quote_assembly)

        quote_details_list: List[QuoteDetail] = []
        for quote_header in epicor_client_cache.nested_quote_header_cache:
            for quote_detail in quote_header.QuoteDtls:
                for quote_assembly in quote_assemblies_list:
                    if (quote_detail.QuoteNum == quote_assembly.QuoteNum) and (
                            quote_detail.QuoteLine == quote_assembly.QuoteLine):
                        quote_details_list.append(quote_detail)

        return quote_assemblies_list, quote_details_list

    def get_quote_child_assemblies_from_cached_data(self, epicor_client_cache: EpicorClientCache,
                                                    processing_quote_assemblies: List[QuoteAssembly]
                                                    ) -> Dict[str, List[QuoteAssembly]]:
        quote_child_assembly_dict: Dict[str, List[QuoteAssembly]] = {}

        for cached_quote_assembly in epicor_client_cache.nested_quote_assembly_cache:
            for quote_assembly in processing_quote_assemblies:
                if (cached_quote_assembly.QuoteNum == quote_assembly.QuoteNum) and (
                        cached_quote_assembly.QuoteLine == quote_assembly.QuoteLine) and (
                        cached_quote_assembly.ParentAssemblySeq == quote_assembly.AssemblySeq):

                    quote_id = self.get_unique_quote_id(str(quote_assembly.QuoteNum), str(quote_assembly.QuoteLine))

                    if quote_child_assembly_dict.get(quote_id, None) is None:
                        quote_child_assembly_dict[quote_id] = [cached_quote_assembly]
                    else:
                        quote_child_assembly_dict[quote_id].append(cached_quote_assembly)

        return quote_child_assembly_dict

    def get_unique_quote_id(self, quote_num: str, quote_line: str) -> str:
        return f"{quote_num}:_:{quote_line}"

    def create_mapping_of_part_numbers_to_quote_numbers(self, quote_details: List[QuoteDetailSearch]):
        for quote_detail in quote_details:
            part_number = create_id_separated_part_number_and_revision_string(quote_detail)
            if self.part_number_to_quote_number_mapping.get(part_number, None):
                self.part_number_to_quote_number_mapping[part_number].update([quote_detail.QuoteNum])
            else:
                self.part_number_to_quote_number_mapping[part_number] = set()
                self.part_number_to_quote_number_mapping[part_number].update([quote_detail.QuoteNum])

    def get_batch_of_new_quote_numbers(self, repeat_part_number) -> Set[int]:
        final_set_of_quote_numbers: Set[int] = set()
        try:
            final_set_of_quote_numbers = itemgetter(repeat_part_number)(self.part_number_to_quote_number_mapping)
        except KeyError as e:
            logger.info(f"No quotes exist for part number {e}")
        return final_set_of_quote_numbers

    def create_mapping_of_part_numbers_to_job_numbers(self, job_entries: List[JobEntry]):
        for job_entry in job_entries:
            part_number = create_id_separated_part_number_and_revision_string(job_entry)
            if self.part_number_to_job_number_mapping.get(part_number, None):
                self.part_number_to_job_number_mapping[part_number].update([job_entry.JobNum])
            else:
                self.part_number_to_job_number_mapping[part_number] = set()
                self.part_number_to_job_number_mapping[part_number].update([job_entry.JobNum])

    def create_mapping_of_part_numbers_to_ewb_sys_row_ids(self, ewb_revs: List[EWBRev]):
        for ewb_rev in ewb_revs:
            part_number = create_id_separated_part_number_and_revision_string(ewb_rev)
            if self.part_number_to_ewb_rev_sys_row_id_mapping.get(part_number, None):
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number].update([ewb_rev.SysRowID])
            else:
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number] = set()
                self.part_number_to_ewb_rev_sys_row_id_mapping[part_number].update([ewb_rev.SysRowID])

    def get_batch_of_new_job_numbers(self, repeat_part_number) -> Set[str]:
        final_set_of_job_numbers: Set[str] = set()
        try:
            final_set_of_job_numbers = itemgetter(repeat_part_number)(self.part_number_to_job_number_mapping)
        except KeyError as e:
            logger.info(f"No jobs exist for part number {e}")
        return final_set_of_job_numbers

    def get_batch_of_new_ewb_rev_sys_row_ids(self, repeat_part_number) -> Set[str]:
        final_set_of_ewb_rev_sys_row_ids: Set[str] = set()
        try:
            final_set_of_ewb_rev_sys_row_ids = itemgetter(repeat_part_number)(self.part_number_to_ewb_rev_sys_row_id_mapping)
        except KeyError as e:
            logger.info(f"No EWB Revs exist for part number {e}")
        return final_set_of_ewb_rev_sys_row_ids

    def create_cache_for_single_part_number(self, repeat_part_number: str, part_num: str, revision_num: str):
        self.part_number_to_quote_number_mapping: Dict[str, Set[int]] = {}
        quote_details: List[QuoteDetailSearch] = QuoteDetailSearch.get_quote_details(part_num, revision_num)
        self.create_mapping_of_part_numbers_to_quote_numbers(quote_details)
        new_quote_numbers_set = self.get_batch_of_new_quote_numbers(repeat_part_number)

        self.part_number_to_job_number_mapping: Dict[str, Set[str]] = {}
        job_entries: List[JobEntry] = JobEntry.get_job_entries(part_num, revision_num)
        self.create_mapping_of_part_numbers_to_job_numbers(job_entries)
        new_job_numbers_set = self.get_batch_of_new_job_numbers(repeat_part_number)

        self.part_number_to_ewb_rev_sys_row_id_mapping: Dict[str, Set[str]] = {}
        ewb_revs: List[EWBRev] = EWBRev.get_ewb_revs(part_num, revision_num)
        self.create_mapping_of_part_numbers_to_ewb_sys_row_ids(ewb_revs)
        new_ewb_rev_sys_row_id_set = self.get_batch_of_new_ewb_rev_sys_row_ids(repeat_part_number)

        epicor_client_cache = create_epicor_client_cache(
            EpicorClientCache(), new_job_numbers_set, new_quote_numbers_set, new_ewb_rev_sys_row_id_set, 10, 10, 10)

        return epicor_client_cache

    def check_if_ewb_rev_is_assembly(self, ewb_rev: EWBRev) -> bool:
        """
        We cannot get the nested details (operations and materials) for child EWBRevs from Epicor's API.
        This function disqualifies any EWB parts that contain child mfg components.
        """
        for child_material in ewb_rev.ECOMtls:
            if child_material.PullAsAsm is True:
                return True
        return False
