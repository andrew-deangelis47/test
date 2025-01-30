from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import MethodOfManufacture
from epicor.quote import QuoteDetail, QuoteQuantity, QuoteAssembly
from epicor.job import JobEntry, JobAssembly
from epicor.engineering_workbench import EWBRev
from typing import List
from baseintegration.utils import logger
from epicor.importer.utils import (
    RepeatPartUtilObject,
    QuoteMOMUtil,
    JobMOMUtil,
    EWBMOMUtil,
    get_quote_detail_erp_code,
    construct_ewb_erp_code,
    safe_get
)
from epicor.importer.epicor_client_cache import EpicorClientCache


class MethodOfManufactureProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject, epicor_client_cache: EpicorClientCache):
        logger.info("MethodOfManufactureProcessor - Attempting to create MethodOfManufacture")

        if epicor_client_cache:
            self.epicor_client_cache: EpicorClientCache = epicor_client_cache
        else:
            self.epicor_client_cache: EpicorClientCache = repeat_part_util_object.epicor_client_cache

        self._create_quote_mom(repeat_part_util_object)
        self._create_job_mom(repeat_part_util_object)
        self._create_ewb_mom(repeat_part_util_object)

        return repeat_part_util_object

    def _create_quote_mom(self, repeat_part_util_object: RepeatPartUtilObject):
        """
        - Iterates epicor quote details
        - Gets quantities for each quote detail
        - Creates quote MOM for each quote quantity
        - Adds quote MOM utils to the repeat part util object for subsequent processing
        """
        for quote_assembly in repeat_part_util_object.epicor_quote_assemblies:
            quote_assembly: QuoteAssembly = quote_assembly
            epicor_quote_detail: QuoteDetail = self._get_root_quote_detail(quote_assembly, repeat_part_util_object)
            if not epicor_quote_detail:
                return None

            for epicor_quote_qty in epicor_quote_detail.QuoteQties:
                quantity = self._get_requested_qty(epicor_quote_qty)  # Make qtys are tied to operations/materials
                quantity_per_parent = safe_get(quote_assembly, "QtyPer", 1)
                quote_mom = MethodOfManufacture(
                    make_qty=quantity * quantity_per_parent,
                    requested_qty=quantity * quantity_per_parent,
                    unit_price=self._get_qty_specific_unit_price(epicor_quote_qty),
                    total_price=self._get_qty_specific_total_price(epicor_quote_qty, quantity),
                )

                quote_mom_util = QuoteMOMUtil(quote_mom, epicor_quote_detail, epicor_quote_qty, quote_assembly, "estimated", get_quote_detail_erp_code(epicor_quote_detail))
                repeat_part_util_object.quote_mom_utils.append(quote_mom_util)

    def _create_job_mom(self, repeat_part_util_object: RepeatPartUtilObject):
        """
        - Iterates epicor jobs
        - Creates job MOM for each job
        - Adds job MOM utils to the repeat part util object for subsequent processing
        """
        for epicor_job_assembly in repeat_part_util_object.epicor_job_assemblies:
            epicor_job: JobEntry = self._get_root_job(epicor_job_assembly, repeat_part_util_object)
            job_assembly: JobAssembly = epicor_job_assembly
            if not epicor_job:
                return

            job_mom = MethodOfManufacture(
                make_qty=int(epicor_job.ProdQty),
                requested_qty=int(epicor_job.OrderQty),
                requires_yield_adjustment=True,
                requires_markup_adjustment=True,
                unit_price=self.get_job_unit_price(job_assembly),
                total_price=float(job_assembly.TLETotalCost),
                operations=[],
                required_materials=[],
                children=[],
            )

            job_mom_util = JobMOMUtil(job_mom, epicor_job, job_assembly, "engineered", epicor_job.JobNum)
            repeat_part_util_object.job_mom_utils.append(job_mom_util)

    def _create_ewb_mom(self, repeat_part_util_object: RepeatPartUtilObject):
        for ewb_rev in repeat_part_util_object.epicor_ewb_revs:
            ewb_rev: EWBRev = ewb_rev

            ewb_mom = MethodOfManufacture(
                make_qty=int(1),  # EWB is quantity agnostic. Exists for engineering purposes only.
                requested_qty=int(1),  # EWB is quantity agnostic. Exists for engineering purposes only.
                unit_price=self.sum_ewb_rev_costs(ewb_rev),
                total_price=0,
            )

            ewb_mom_util = EWBMOMUtil(ewb_mom, ewb_rev, "template", construct_ewb_erp_code(ewb_rev))
            repeat_part_util_object.ewb_mom_utils.append(ewb_mom_util)

    def _get_quote_assemblies(self, epicor_quote_detail: QuoteDetail, repeat_part_util_object: RepeatPartUtilObject) \
            -> QuoteAssembly:
        for quote_assembly in repeat_part_util_object.epicor_quote_assemblies:
            if quote_assembly.QuoteNum == epicor_quote_detail.QuoteNum and \
                    (quote_assembly.QuoteLine == epicor_quote_detail.QuoteLine):
                return quote_assembly
        logger.info("No quote assembly exists for this part number.")

    def _get_job_assembly(self, epicor_job: JobEntry, repeat_part_util_object: RepeatPartUtilObject) -> JobAssembly:
        for job_assembly in repeat_part_util_object.epicor_job_assemblies:
            if job_assembly.JobNum == epicor_job.JobNum:
                return job_assembly
        logger.info("No job assembly exists for this part number.")

    def _get_root_job(self, epicor_job_assembly: JobAssembly, repeat_part_util_object: RepeatPartUtilObject):
        for job in repeat_part_util_object.epicor_job_entries:
            if epicor_job_assembly.JobNum == job.JobNum:
                return job
        params = {'$filter': f"JobNum eq '{epicor_job_assembly.JobNum}'"}
        jobs_list = JobEntry.get_paginated_results_with_params(params=params)
        return jobs_list[0]

    def _get_root_quote_detail(self, epicor_quote_assembly: QuoteAssembly, repeat_part_util_object: RepeatPartUtilObject):
        # Attempt to get quote detail from repeat part util object
        for quote_detail in repeat_part_util_object.epicor_quote_details:
            if (epicor_quote_assembly.QuoteNum == quote_detail.QuoteNum) and (
                    epicor_quote_assembly.QuoteLine == quote_detail.QuoteLine):
                return quote_detail

        logger.info("Cannot create a method of manufacture for this part. Missing quote detail which contains all "
                    "quantity information.")
        return None

    def _get_requested_qty(self, epicor_quote_qty: QuoteQuantity) -> int:
        return int(epicor_quote_qty.OurQuantity)

    def _get_qty_specific_unit_price(self, epicor_quote_qty: QuoteQuantity) -> float:
        return float(epicor_quote_qty.UnitPrice)

    def _get_qty_specific_total_price(self, epicor_quote_qty: QuoteQuantity, quantity: int) -> float:
        total_price = quantity * self._get_qty_specific_unit_price(epicor_quote_qty)
        return float(total_price)

    def sum_ewb_rev_costs(self, ewb_rev: EWBRev):
        # TODO: Figure out costing for EWB
        return 0

    def get_job_unit_price(self, job_assembly: JobAssembly) -> float:
        total_cost = float(safe_get(job_assembly, "TLETotalCost", 0))
        required_qty = float(safe_get(job_assembly, "RequiredQty", 0))
        unit_price = total_cost / required_qty if required_qty > 0 else 0
        return round(float(unit_price), 3)

    def get_quote_quantities_from_epicor_client_cache(self, quote_num: str, quote_line: str) -> List[QuoteQuantity]:
        quote_quantities_list: List[QuoteQuantity] = []
        for quote_detail in self.epicor_client_cache.nested_quote_detail_cache:
            if (quote_detail.QuoteNum == quote_num) and (quote_detail.QuoteLine == quote_line):
                quote_quantities_list = quote_detail.QuoteQties

        return quote_quantities_list
