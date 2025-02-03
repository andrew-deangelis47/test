from decimal import Decimal

from django.db.models import QuerySet, Q

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_utils import MOMWrapper
from inforvisual.importer.repeat_part_processors.repeat_work_utils import get_material_costing_variables, \
    get_operation_costing_variables, PartData, get_part_id_from_requirement, is_part_id_from_requirement, \
    get_requirement_from_part_id
from inforvisual.models import (
    QuoteLine as InforVisualQuoteLine,
    QuotePrice as InforVisualQuotePrice,
    Requirement as InforVisualRequirement,
    WorkOrder as InforVisualWorkOrder,
    Operation as InforVisualOperation,
    Part as InforVisualPart,
    ShopResource as InforVisualShopResource,
    PartSite,
    CustOrderLine,
    DemandSupplyLink,
)
from baseintegration.utils.repeat_work_objects import (
    MethodOfManufacture,
    Operation,
    Child,
    RequiredMaterials, CostingVariable,
)
from typing import Optional, List, Callable
from baseintegration.integration import logger


class MOMImportProcessor(BaseImportProcessor):
    def _process(self, repeat_part_id: str, create_child_parts: bool) -> (list, PartData):
        logger.info(f"Creating repeat part methods of manufacture from item ID: {repeat_part_id}")
        self.source_database = self._importer.source_database
        self.create_child_parts = create_child_parts
        self.part_data = PartData()
        self.moms = []

        is_from_requirement = is_part_id_from_requirement(repeat_part_id)
        if is_from_requirement:
            self.create_moms_from_requirement(repeat_part_id)
        else:
            # iterate through root engineering masters
            self.create_engineering_master_root_moms(repeat_part_id)

            # iterate through root quotes
            self.create_quote_line_root_moms(repeat_part_id)

            # iterate through root work orders
            self.create_work_order_root_moms(repeat_part_id)

            # create moms for any work orders that are non-root
            self.create_non_root_moms(repeat_part_id)

        return self.moms, self.part_data

    def create_moms_from_requirement(self, part_id):
        requirement = get_requirement_from_part_id(part_id)
        if requirement:
            self.create_non_root_moms_from_requirement(requirement)

    def create_engineering_master_root_moms(self, repeat_part_id: str) -> None:
        work_orders: QuerySet[InforVisualWorkOrder] = InforVisualWorkOrder.objects.using(self.source_database)\
            .filter(part_id=repeat_part_id, type="M", sub_id='0')
        for work_order in work_orders:
            self.part_data.is_root = True
            self.create_template_work_order_mom(work_order, root_work_order=work_order,
                                                quantity=work_order.desired_qty)

    def create_template_work_order_mom(self, work_order: InforVisualWorkOrder, root_work_order: InforVisualWorkOrder,
                                       quantity: Decimal) -> None:
        if not quantity:
            quantity = 1
        operations = self.form_engineered_shop_operations_from_wo(work_order)
        materials, children = self.form_materials_and_children_from_work_order(
            work_order, self.get_engineered_material_cost)
        part_site: PartSite = PartSite.objects.using(self.source_database).filter(part_id=work_order.part_id).first()
        if part_site:
            unit_price = part_site.unit_price or 0
        else:
            total_cost = self.get_total_estimated_cost_from_work_order(work_order)
            unit_price = total_cost / quantity
        mom = MethodOfManufacture(
            make_qty=quantity,
            requested_qty=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
            operations=operations,
            required_materials=materials,
            children=children,
        )
        mom_wrapper = MOMWrapper(mom, "template", root_work_order)
        self.moms.append(mom_wrapper)

    def create_quote_moms(
            self,
            work_order: InforVisualWorkOrder,
            root_quote_line: InforVisualQuoteLine,
            root_work_order: InforVisualWorkOrder,
            quantity_per_root: Decimal = Decimal(1)):
        quote_prices: QuerySet[InforVisualQuotePrice] = InforVisualQuotePrice.objects.using(self.source_database)\
            .filter(quote_id=root_quote_line.quote_id, quote_line_no=root_quote_line.line_no)
        for quote_price in quote_prices:
            root_quantity = quote_price.qty
            root_work_order_quantity = root_work_order.desired_qty or 1
            operations = self.form_quote_shop_operations_from_wo(work_order, root_quantity, root_work_order_quantity)

            def get_estimated_material_cost(requirement: InforVisualRequirement):
                # you can view cost totals in Manufacturing Window -> Costs
                material_cost = requirement.est_material_cost + requirement.est_service_cost + \
                    requirement.est_labor_cost + requirement.est_burden_cost
                material_cost_per_root = material_cost / root_work_order_quantity
                return material_cost_per_root * root_quantity

            materials, children = self.form_materials_and_children_from_work_order(
                work_order, get_estimated_material_cost)
            quantity = root_quantity * quantity_per_root
            mom = MethodOfManufacture(
                make_qty=quantity,
                requested_qty=quantity,
                unit_price=quote_price.unit_price,
                total_price=quote_price.unit_price * quote_price.qty,
                operations=operations,
                required_materials=materials,
                children=children,
            )
            mom_wrapper = MOMWrapper(mom, "estimated", root_quote_line)
            self.moms.append(mom_wrapper)

    def create_quote_line_root_moms(self, repeat_part_id: str) -> None:
        quote_lines: QuerySet[InforVisualQuoteLine] = InforVisualQuoteLine.objects.using(self.source_database)\
            .filter(Q(part_id=repeat_part_id) | Q(customer_part_id=repeat_part_id))
        for quote_line in quote_lines:
            self.part_data.is_root = True
            if quote_line.workorder_base_id is None:
                logger.info(f'Quote Line for {repeat_part_id} on Quote: {quote_line.quote} has no work order. '
                            f'Skipping!')
                continue

            work_order = self.get_quoted_work_order(quote_line)
            self.create_quote_moms(work_order, quote_line, root_work_order=work_order)

    def create_work_order_root_moms(self, repeat_part_id: str) -> None:
        work_orders = InforVisualWorkOrder.objects.using(self.source_database)\
            .filter(part_id=repeat_part_id, type="W", sub_id='0')
        for work_order in work_orders:
            self.part_data.is_root = True
            self.create_engineered_work_order_mom(work_order, root_work_order=work_order,
                                                  quantity=work_order.desired_qty)
            self.create_executed_work_order_mom(work_order, root_work_order=work_order,
                                                quantity=work_order.desired_qty)

    def create_engineered_work_order_mom(self, work_order: InforVisualWorkOrder, root_work_order: InforVisualWorkOrder,
                                         quantity: Decimal) -> None:
        if not quantity:
            quantity = Decimal(0)
        operations = self.form_engineered_shop_operations_from_wo(work_order)
        materials, children = self.form_materials_and_children_from_work_order(
            work_order, self.get_engineered_material_cost)
        unit_price = self.get_work_order_unit_price(work_order)
        mom = MethodOfManufacture(
            make_qty=quantity,
            requested_qty=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
            operations=operations,
            required_materials=materials,
            children=children,
        )
        mom_wrapper = MOMWrapper(mom, "engineered", root_work_order)
        self.moms.append(mom_wrapper)

    def create_executed_work_order_mom(self, work_order: InforVisualWorkOrder, root_work_order: InforVisualWorkOrder,
                                       quantity: Decimal) -> None:
        if not quantity:
            quantity = Decimal(0)
        operations = self.form_executed_shop_operations_from_wo(work_order)
        materials, children = self.form_materials_and_children_from_work_order(
            work_order, self.get_executed_material_cost)
        unit_price = self.get_work_order_unit_price(work_order)
        mom = MethodOfManufacture(
            make_qty=quantity,
            requested_qty=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
            operations=operations,
            required_materials=materials,
            children=children,
        )
        mom_wrapper = MOMWrapper(mom, "executed", root_work_order)
        self.moms.append(mom_wrapper)

    def get_work_order_unit_price(self, work_order: InforVisualWorkOrder):
        demand_supply_link: DemandSupplyLink = DemandSupplyLink.objects.using(self.source_database).filter(
            demand_type='CO',
            supply_type='WO',
            supply_base_id=work_order.base_id,
            supply_lot_id=work_order.lot_id,
            supply_split_id=work_order.split_id,
            supply_sub_id=work_order.sub_id
        ).first()
        if demand_supply_link:
            cust_order_id = demand_supply_link.demand_base_id
            cust_order_line_no = demand_supply_link.demand_seq_no
            cust_order_line: CustOrderLine = CustOrderLine.objects.using(self.source_database)\
                .filter(cust_order_id=cust_order_id, line_no=cust_order_line_no).first()
            if cust_order_line:
                return cust_order_line.unit_price
        return 0

    def form_materials_and_children_from_work_order(
            self, work_order: Optional[InforVisualWorkOrder], get_material_cost: Callable) \
            -> (List[RequiredMaterials], List[Child]):
        if work_order is None:
            return [], []
        materials = []
        children = []
        requirements = self.get_requirements_from_wo(work_order)
        for requirement in requirements:
            part: InforVisualPart = requirement.part
            part_id = get_part_id_from_requirement(requirement)
            child_work_order = self.get_child_work_order_from_requirement(requirement)
            if child_work_order is not None:
                self.process_child_repeat_part(part_id)
                child = Child(
                    part_number=part_id,
                    revision=part.revision_id if part else "",
                    qty_per_parent=requirement.qty_per,
                )
                children.append(child)
            else:
                costing_var_dict = get_material_costing_variables(requirement)
                material = RequiredMaterials(
                    name=part_id,
                    notes=part.description if part else "",  # TODO: should we get notes from RequirementBinary or SriRequirementBinary?
                    total_cost=get_material_cost(requirement),
                    costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(material)
        return materials, children

    @staticmethod
    def get_engineered_material_cost(requirement: InforVisualRequirement):
        material_cost = requirement.est_material_cost + requirement.est_service_cost + \
            requirement.est_labor_cost + requirement.est_burden_cost
        return material_cost

    @staticmethod
    def get_executed_material_cost(requirement: InforVisualRequirement):
        material_cost = requirement.act_material_cost + requirement.act_service_cost + \
            requirement.act_labor_cost + requirement.act_burden_cost
        return material_cost

    def form_quote_shop_operations_from_wo(
        self, work_order: Optional[InforVisualWorkOrder], quote_line_quantity: Decimal,
            root_work_order_quantity: Decimal) -> List[Operation]:
        if work_order is None:
            return []
        operations = []
        for infor_visual_operation in self.get_operations_from_wo(work_order):
            run_hours_per_root = infor_visual_operation.run_hrs / (root_work_order_quantity or 1)
            run_hours = run_hours_per_root * quote_line_quantity
            cost = infor_visual_operation.est_atl_lab_cost + infor_visual_operation.est_atl_bur_cost \
                + infor_visual_operation.est_atl_ser_cost
            cost_per_root = cost / (root_work_order_quantity or 1)
            total_cost = cost_per_root * quote_line_quantity
            resource: InforVisualShopResource = infor_visual_operation.resource
            costing_var_dict = get_operation_costing_variables(infor_visual_operation)
            operation = Operation(
                is_outside_service=resource.type == 'C',
                name=resource.id,
                notes=resource.description,  # TODO: should we get notes from OperationBinary or SriOperationBinary?
                position=infor_visual_operation.sequence_no,
                runtime=run_hours,
                setup_time=infor_visual_operation.setup_hrs,
                total_cost=total_cost,
                costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
            )
            operations.append(operation)
        return operations

    def form_engineered_shop_operations_from_wo(self, work_order: Optional[InforVisualWorkOrder]) -> List[Operation]:
        if work_order is None:
            return []
        operations = []
        for infor_visual_operation in self.get_operations_from_wo(work_order):
            total_cost = infor_visual_operation.est_atl_lab_cost + infor_visual_operation.est_atl_bur_cost \
                + infor_visual_operation.est_atl_ser_cost
            resource: InforVisualShopResource = infor_visual_operation.resource
            costing_var_dict = get_operation_costing_variables(infor_visual_operation)
            operation = Operation(
                is_outside_service=resource.type == 'C',
                name=resource.id,
                notes=resource.description,
                position=infor_visual_operation.sequence_no,
                runtime=infor_visual_operation.run_hrs,
                setup_time=infor_visual_operation.setup_hrs,
                total_cost=total_cost,
                costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
            )
            operations.append(operation)
        return operations

    def form_executed_shop_operations_from_wo(self, work_order: Optional[InforVisualWorkOrder]) -> List[Operation]:
        if work_order is None:
            return []
        operations = []
        for infor_visual_operation in self.get_operations_from_wo(work_order):
            total_cost = infor_visual_operation.act_atl_lab_cost + infor_visual_operation.act_atl_bur_cost \
                + infor_visual_operation.act_atl_ser_cost
            resource: InforVisualShopResource = infor_visual_operation.resource
            costing_var_dict = get_operation_costing_variables(infor_visual_operation)
            operation = Operation(
                is_outside_service=resource.type == 'C',
                name=resource.id,
                notes=resource.description,
                position=infor_visual_operation.sequence_no,
                runtime=infor_visual_operation.run_hrs,
                setup_time=infor_visual_operation.setup_hrs,
                total_cost=total_cost,
                costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
            )
            operations.append(operation)
        return operations

    def get_operations_from_wo(
        self, wo: InforVisualWorkOrder
    ) -> QuerySet[InforVisualOperation]:
        return InforVisualOperation.objects.using(self.source_database).filter(
            workorder_type=wo.type,
            workorder_base=wo.base_id,
            workorder_sub=wo.sub_id,
            workorder_split=wo.split_id,
            workorder_lot=wo.lot_id,
        ).order_by("sequence_no")

    def get_requirements_from_wo(
        self, wo: InforVisualWorkOrder
    ) -> QuerySet[InforVisualRequirement]:
        return InforVisualRequirement.objects.using(self.source_database).filter(
            workorder_type=wo.type,
            workorder_base=wo.base_id,
            workorder_sub=wo.sub_id,
            workorder_split=wo.split_id,
            workorder_lot=wo.lot_id,
        )

    def get_quoted_work_order(
        self, quote_line: InforVisualQuoteLine
    ) -> Optional[InforVisualWorkOrder]:
        return InforVisualWorkOrder.objects.using(self.source_database).filter(
            type=quote_line.workorder_type,
            base_id=quote_line.workorder_base_id,
            lot_id=quote_line.workorder_lot_id,
            split_id=quote_line.workorder_split_id,
            sub_id=quote_line.workorder_sub_id,
        ).first()

    def create_non_root_moms(self, repeat_part_id: str) -> None:
        # first, get all instances where the part is used as a subcomponent
        reqs = InforVisualRequirement.objects.using(self.source_database).filter(
            part__id=repeat_part_id, part__purchased="N"
        )
        for req in reqs:
            self.create_non_root_moms_from_requirement(req)

    def create_non_root_moms_from_requirement(self, requirement: InforVisualRequirement):
        work_order: Optional[InforVisualWorkOrder] = self.get_child_work_order_from_requirement(requirement)
        if not work_order:
            logger.info(
                f"Could not find work order for {requirement.workorder_base}, skipping"
            )
            return

        # for the subcomponent work order, get all the ancestor work orders for that subcomponent
        ancestor_wos: List[InforVisualWorkOrder] = []
        self.get_ancestor_work_orders_from_wo(work_order, ancestor_wos)
        for ancestor_wo in ancestor_wos:
            # for each root ancestor, add a MoM for this subcomponent
            if work_order.type == 'M':
                self.create_template_work_order_mom(
                    work_order, root_work_order=ancestor_wo, quantity=requirement.calc_qty)
            elif work_order.type == 'W':
                self.create_engineered_work_order_mom(
                    work_order, root_work_order=ancestor_wo, quantity=requirement.calc_qty)
                self.create_executed_work_order_mom(
                    work_order, root_work_order=ancestor_wo, quantity=requirement.calc_qty)
            self.create_quoted_moms_per_ancestor_wo(
                work_order, root_work_order=ancestor_wo, quantity=requirement.calc_qty)

    def create_quoted_moms_per_ancestor_wo(
        self, work_order: InforVisualWorkOrder, root_work_order: InforVisualWorkOrder, quantity: Decimal
    ):
        if not quantity:
            quantity = Decimal(0)
        quantity_per_root = quantity / (root_work_order.desired_qty or 1)
        ancestor_quote_lines = InforVisualQuoteLine.objects.using(self.source_database).filter(
            workorder_type=root_work_order.type,
            workorder_base_id=root_work_order.base_id,
            workorder_split_id=root_work_order.split_id,
            workorder_lot_id=root_work_order.lot_id,
            workorder_sub_id=root_work_order.sub_id,
        )
        for root_quote_line in ancestor_quote_lines:
            self.create_quote_moms(work_order,
                                   root_quote_line=root_quote_line,
                                   root_work_order=root_work_order,
                                   quantity_per_root=quantity_per_root)

    def get_wo_from_requirement(
        self, req: InforVisualRequirement
    ) -> Optional[InforVisualWorkOrder]:
        return InforVisualWorkOrder.objects.using(self.source_database).filter(
            type=req.workorder_type,
            base_id=req.workorder_base,
            lot_id=req.workorder_lot,
            split_id=req.workorder_split,
            sub_id=req.workorder_sub,
        ).first()

    def get_child_work_order_from_requirement(self, requirement: InforVisualRequirement) \
            -> Optional[InforVisualWorkOrder]:
        if requirement.subord_wo_sub is None:
            return None
        return InforVisualWorkOrder.objects.using(self.source_database).filter(
            type=requirement.workorder_type,
            base_id=requirement.workorder_base,
            lot_id=requirement.workorder_lot,
            split_id=requirement.workorder_split,
            sub_id=requirement.subord_wo_sub,
        ).first()

    def get_ancestor_work_orders_from_wo(
        self,
        child_work_order: InforVisualWorkOrder,
        ancestor_wos: List[InforVisualWorkOrder],
    ) -> None:
        child_mfg_reqs = InforVisualRequirement.objects.using(self.source_database).filter(
            Q(part__purchased="N") | Q(part=None),
            workorder_type=child_work_order.type,
            workorder_base=child_work_order.base_id,
            workorder_split=child_work_order.split_id,
            workorder_lot=child_work_order.lot_id,
            subord_wo_sub=child_work_order.sub_id
        )
        if child_mfg_reqs.count() == 0:
            return
        for child_req in child_mfg_reqs:
            parent_wo = self.get_wo_from_requirement(child_req)
            if not parent_wo:
                logger.info(
                    f"Could not find work order for {child_req.workorder_base}, skipping"
                )
                continue
            if parent_wo.sub_id == '0':
                ancestor_wos.append(parent_wo)
            else:
                self.get_ancestor_work_orders_from_wo(parent_wo, ancestor_wos)

    def get_total_estimated_cost_from_work_order(
        self, work_order: InforVisualWorkOrder
    ) -> Decimal:
        return work_order.est_material_cost + work_order.est_burden_cost + work_order.est_labor_cost + \
            work_order.est_service_cost

    @classmethod
    def _get_shop_operation_costing_variables(cls, costing_vars: dict) -> List[CostingVariable]:
        pp_costing_vars = []
        for pp_var_name, (value, value_type) in costing_vars.items():
            if value_type is bool:
                value_type = str
            if value is not None:
                pp_costing_vars.append(
                    CostingVariable(
                        label=pp_var_name,
                        value=value_type(value)
                    )
                )
        return pp_costing_vars

    def process_child_repeat_part(self, part_id):
        self.part_data.part_type = "assembled"
        if self.create_child_parts:
            logger.info(f"Creating child parts for {part_id}")
            self._importer._process_repeat_part(part_id, create_child_parts=True)
