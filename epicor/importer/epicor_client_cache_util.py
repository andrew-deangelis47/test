from epicor.importer.epicor_client_cache import EpicorClientCache
from baseintegration.utils import logger
from typing import Set


def create_epicor_client_cache(epicor_client_cache: EpicorClientCache, new_job_numbers_set: Set[str],
                               new_quote_numbers_set: Set[int], new_ewb_rev_sys_row_id_set: Set[str],
                               job_id_count_filter_limit: int, quote_id_count_filter_limit: int,
                               ewb_request_object_limit: int, page_size: int = 10) -> EpicorClientCache:
    epicor_client_cache.clear_cache()
    logger.info("Creating Epicor client cache for all related records in this batch.")
    epicor_client_cache.create_nested_job_entry_cache(new_job_numbers_set, job_id_count_filter_limit, page_size)
    epicor_client_cache.create_nested_quote_cache(new_quote_numbers_set, quote_id_count_filter_limit, page_size)
    epicor_client_cache.create_nested_ewb_rev_cache(new_ewb_rev_sys_row_id_set, ewb_request_object_limit, page_size)

    return epicor_client_cache
