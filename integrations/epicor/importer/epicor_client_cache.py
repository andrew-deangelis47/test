from epicor.job import JobEntry
from epicor.quote import QuoteHeader, QuoteAssembly
from epicor.engineering_workbench import EWBRev
from typing import List, Tuple, Set
from baseintegration.utils import logger


class EpicorClientCache:
    def __init__(self):
        self.total_repeat_part_count = 0
        self.nested_job_entry_cache: List[JobEntry] = []
        self.nested_quote_header_cache: List[QuoteHeader] = []
        self.nested_quote_assembly_cache: List[QuoteAssembly] = []
        self.nested_ewb_rev_cache: List[EWBRev] = []

    def clear_cache(self):
        logger.info("Clearing Epicor client cache...")
        self.nested_job_entry_cache = []
        self.nested_quote_header_cache = []
        self.nested_quote_assembly_cache = []
        self.nested_ewb_rev_cache = []
        logger.info("Cache is cleared.")

    def create_nested_job_entry_cache(self, job_number_list: Set[str], job_request_object_limit: int, page_size: int = 10):
        filter_string = ""
        for count, job_number in enumerate(job_number_list, start=1):
            filter_string += f"(JobNum eq '{job_number}') or "
            if count % job_request_object_limit == 0:
                job_entries_list: List[JobEntry] = JobEntry.get_all_nested_job_data_by_job_number(
                    filter_string[:-4], page_size)
                self.nested_job_entry_cache.extend(job_entries_list)
                filter_string = ""
            elif count == len(job_number_list):
                job_entries_list: List[JobEntry] = JobEntry.get_all_nested_job_data_by_job_number(
                    filter_string[:-4], page_size)
                self.nested_job_entry_cache.extend(job_entries_list)

    def create_nested_quote_cache(self, quote_number_list: Set[int], quote_request_object_limit: int, page_size: int = 10):
        filter_string = ""
        for count, quote_number in enumerate(quote_number_list, start=1):
            filter_string += f"(QuoteNum eq {quote_number}) or "
            if count % quote_request_object_limit == 0:
                nested_quote_headers: List[QuoteHeader] = QuoteHeader.get_quote_header_nested_data_by_quote_num(
                    filter_string[:-4], page_size)
                self.nested_quote_header_cache.extend(nested_quote_headers)
                filter_string = ""
            elif count == len(quote_number_list):
                nested_quote_headers: List[QuoteHeader] = QuoteHeader.get_quote_header_nested_data_by_quote_num(
                    filter_string[:-4], page_size)
                self.nested_quote_header_cache.extend(nested_quote_headers)

        quote_assembly_tuples_list: List[Tuple[int, int]] = []
        for nested_quote_header in self.nested_quote_header_cache:
            for quote_detail in nested_quote_header.QuoteDtls:
                quote_assembly_tuples_list.append((quote_detail.QuoteNum, quote_detail.QuoteLine))

        filter_string = ""
        for count, assm_tuple in enumerate(quote_assembly_tuples_list, start=1):
            filter_string += f"(QuoteNum eq {assm_tuple[0]} and QuoteLine eq {assm_tuple[1]}) or "
            if count % quote_request_object_limit == 0:
                quote_assemblies_list: List[QuoteAssembly] = \
                    QuoteAssembly.get_quote_assemblies_nested_data_by_quote_num_line_num(filter_string[:-4],
                                                                                         page_size)
                self.nested_quote_assembly_cache.extend(quote_assemblies_list)
                filter_string = ""
            elif count == len(quote_assembly_tuples_list):
                quote_assemblies_list: List[
                    QuoteAssembly] = QuoteAssembly.get_quote_assemblies_nested_data_by_quote_num_line_num(
                    filter_string[:-4], page_size)
                self.nested_quote_assembly_cache.extend(quote_assemblies_list)

    def create_nested_ewb_rev_cache(self, ewb_sys_row_id_list: Set[str], ewb_request_object_limit: int, page_size: int = 10):
        filter_string = ""
        for count, ewb_row_id in enumerate(ewb_sys_row_id_list, start=1):
            filter_string += f"(SysRowID eq {ewb_row_id}) or "
            if count % ewb_request_object_limit == 0:
                ewb_revs_list: List[EWBRev] = EWBRev.get_all_nested_ewb_rev_data_by_sys_row_id(
                    filter_string[:-4], page_size)
                self.nested_ewb_rev_cache.extend(ewb_revs_list)
                filter_string = ""
            elif count == len(ewb_sys_row_id_list):
                ewb_revs_list: List[EWBRev] = EWBRev.get_all_nested_ewb_rev_data_by_sys_row_id(
                    filter_string[:-4], page_size)
                self.nested_ewb_rev_cache.extend(ewb_revs_list)
