from typing import List, Union, Optional

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get
from baseintegration.utils.repeat_work_objects import MethodOfManufacture
from e2.models import (
    OrderDet,
    Releases,
    JobReq,
    Quotedet,
    Estim,
    Materials
)
from e2.importer.utils import (
    RepeatPartUtilObject,
    JobMOMUtil,
    QuoteMOMUtil,
    TemplateMOMUtil,
    get_quote_detail_erp_code,
    ESTIM_NUM_PRICES
)


class MethodOfManufactureProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info(f"Calculating methods of manufacture for repeat work part from E2 with part number {repeat_part_util.e2_part.partno}")
        self.source_database = self._importer.source_database
        self.repeat_part_util = repeat_part_util

        self.create_job_moms()
        self.create_template_moms(repeat_part_util.e2_part.partno)
        self.create_quote_moms()

        return repeat_part_util

    def create_job_moms(self):
        part_no = self.repeat_part_util.e2_part.partno
        order_dets: List[OrderDet] = OrderDet.objects.using(self.source_database).filter(part_no=part_no)
        for order_detail in order_dets:
            self.create_job_mom_for_order_detail(order_detail, order_detail.qty_ordered or 1, order_detail.qty_to_make or 1, order_detail.unit_price or 0)
        job_requirements: List[JobReq] = JobReq.objects.using(self.source_database).filter(partno=part_no)
        for job_req in job_requirements:
            self.create_job_mom_for_job_requirement(job_req)

    def create_job_mom_for_order_detail(self, order_detail: OrderDet, requested_quantity: int, make_quantity: int, unit_price: float):
        if not order_detail.job_no:
            return None
        root_order_detail = order_detail
        visited_order_details = set()
        while root_order_detail.master_job_no:
            if root_order_detail.pk in visited_order_details:
                raise ValueError("Cycle detected in order assembly")
            visited_order_details.add(root_order_detail.pk)
            root_order_detail = OrderDet.objects.using(self.source_database).filter(job_no=root_order_detail.master_job_no).first()
            if not root_order_detail:
                return None
        job_mom = MethodOfManufacture(
            make_qty=make_quantity,
            requested_qty=requested_quantity,
            unit_price=unit_price,
            total_price=requested_quantity * unit_price,
            operations=[],
            required_materials=[],
            children=[]
        )
        releases: List[Releases] = Releases.objects.using(self.source_database).filter(
            orderno=root_order_detail.orderno,
            jobno=root_order_detail.job_no,
            partno=root_order_detail.part_no
        )
        header_type = "engineered" if len(releases) == 0 else "executed"
        job_mom_util = JobMOMUtil(
            method_of_manufacture=job_mom,
            type=header_type,
            erp_code=root_order_detail.job_no,
            order_detail=order_detail
        )
        logger.info(f"Created job MoM util for E2 repeat part {self.repeat_part_util.e2_part.partno} and root job {root_order_detail.job_no}")
        self.repeat_part_util.job_mom_utils.append(job_mom_util)
        return job_mom_util

    def create_job_mom_for_job_requirement(self, job_requirement: JobReq):
        quantity = job_requirement.qty2buy or 1
        unit_price = job_requirement.price or 0
        order_detail = OrderDet.objects.using(self.source_database).filter(job_no=job_requirement.jobno).first()
        if order_detail:
            job_mom_util = self.create_job_mom_for_order_detail(order_detail, quantity, quantity, unit_price)
            if job_mom_util:
                job_mom_util.order_detail = None
                job_mom_util.job_requirement = job_requirement

    def create_quote_moms(self):
        """
        - Iterates through the E2 quote details for this repeat part
        - Gets quantities for each quote detail
        - Creates a method of manufacture for each quote detail
        - Adds quote MOM utils to the repeat part util object for subsequent processing
        """

        part_number = self.repeat_part_util.e2_part.partno
        logger.info(f"Calculating quote methods of manufacture for repeat work part from E2 with part number {part_number}")
        quote_details: List[Quotedet] = Quotedet.objects.using(self.source_database).filter(partno=part_number)

        for quote_detail in quote_details:
            for quantity, price in self.iterate_quantity_breaks(quote_detail):
                quote_mom = MethodOfManufacture(
                    make_qty=quantity,
                    requested_qty=quantity,
                    unit_price=price,
                    total_price=price * quantity,
                    operations=[],
                    required_materials=[],
                    children=[]
                )
                quote_mom_util = QuoteMOMUtil(quote_mom, quote_detail, "estimated", get_quote_detail_erp_code(quote_detail))
                logger.info(
                    f"Created quote MoM util for E2 repeat part with part number {part_number}: {vars(quote_mom_util)}")
                self.repeat_part_util.quote_mom_utils.append(quote_mom_util)

    def create_template_moms(self, part_no: str, quantity_for_child: int = 1, unit_price: Optional[float] = None):
        part: Estim = Estim.objects.using(self.source_database).filter(partno=part_no).first()
        if not part:
            return

        parent_part_numbers = Materials.objects.using(self.source_database).filter(subpartno=part_no).values_list('partno', flat=True)

        for quantity, price in self.iterate_quantity_breaks(part):
            quantity *= quantity_for_child
            unit_price_for_quantity = price if unit_price is None else unit_price
            template_mom = MethodOfManufacture(
                make_qty=quantity,
                requested_qty=quantity,
                unit_price=unit_price_for_quantity,
                total_price=unit_price_for_quantity * quantity,
                operations=[],
                required_materials=[],
                children=[]
            )
            template_mom_util = TemplateMOMUtil(template_mom, part, "template", part_no)
            logger.info(f"Created template MoM util for E2 repeat part with part number {part_no}: {vars(template_mom_util)}")
            self.repeat_part_util.template_mom_utils.append(template_mom_util)
            for parent_part_no in parent_part_numbers:
                logger.info(f"Base Part {self.repeat_part_util.repeat_part.part_number}. Traversing up assembly from {part_no} to {parent_part_no}")
                self.create_template_moms(parent_part_no, quantity_for_child, unit_price)

    @staticmethod
    def iterate_quantity_breaks(obj: Union[Estim, Quotedet]):
        for price_num in range(1, ESTIM_NUM_PRICES + 1):
            quantity: int = safe_get(obj, f"qty{price_num}", 0) or 0
            price: float = safe_get(obj, f"price{price_num}", 0) or 0
            if quantity == 0 or price == 0:
                if price_num == 1:
                    quantity = quantity or 1
                else:
                    break
            yield quantity, price
