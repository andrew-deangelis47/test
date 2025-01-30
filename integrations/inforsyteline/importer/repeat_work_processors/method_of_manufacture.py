from decimal import Decimal
from typing import List, Union, Callable

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import MethodOfManufacture, Operation, RequiredMaterials, Child, \
    CostingVariable, Part
from baseintegration.utils.repeat_work_utils import MOMWrapper
from baseintegration.datamigration import logger
from inforsyteline.importer.configuration import RepeatPartImportConfig
from inforsyteline.importer.repeat_work_utils import get_material_costing_variables, get_operation_costing_variables, \
    get_product_code

from inforsyteline.models import JobMst, ItemMst, JobmatlMst, ItempriceMst, JobrouteMst, WcMst, JrtresourcegroupMst, \
    JrtSchMst, CoitemMst


class MethodOfManufactureProcessor(BaseImportProcessor):
    def _process(self, repeat_part: Part, create_child_parts: bool) -> List[MOMWrapper]:
        logger.info(f"Creating repeat part methods of manufacture from Infor Syteline item ID: {repeat_part.part_number}")

        self.source_database = self._importer.source_database
        self.create_child_parts = create_child_parts
        self.repeat_part = repeat_part

        methods_of_manufacture = []

        methods_of_manufacture += self.get_template_methods_of_manufacture()
        methods_of_manufacture += self.get_estimated_methods_of_manufacture()
        methods_of_manufacture += self.get_engineered_methods_of_manufacture()
        methods_of_manufacture += self.get_executed_methods_of_manufacture()

        return methods_of_manufacture

    def get_template_methods_of_manufacture(self) -> List[MOMWrapper]:
        methods_of_manufacture = []
        template_job: JobMst = JobMst.objects.using(self.source_database)\
            .filter(type='S', item=self.repeat_part.part_number, mo_bom_alternate_id='Current').first()
        if template_job:
            methods_of_manufacture += self.get_template_methods_of_manufacture_from_job(template_job)
        else:
            # some parts (i.e. purchased components) correspond to job materials rather than jobs
            job_materials = JobmatlMst.objects.using(self.source_database).filter(item=self.repeat_part.part_number)
            for job_material in job_materials:
                job_material: JobmatlMst
                parent_job: JobMst = JobMst.objects.using(self.source_database)\
                    .filter(type='S', job=job_material.job, suffix=job_material.suffix,
                            mo_bom_alternate_id='Current').first()
                if parent_job:
                    methods_of_manufacture += self.get_template_methods_of_manufacture_from_job(
                        parent_job, job_material.matl_qty or 1, has_materials_and_operations=False)
        return methods_of_manufacture

    def get_template_methods_of_manufacture_from_job(self, job: JobMst, root_quantity=1,
                                                     has_materials_and_operations=True):
        methods_of_manufacture = []
        item_price_data: ItempriceMst = ItempriceMst.objects.using(self.source_database)\
            .filter(item=self.repeat_part.part_number).first()
        unit_price = 0
        if item_price_data:
            unit_price = item_price_data.unit_price1 or 0
        for root_job, quantity_per_root in self.get_root_template_jobs(job, root_quantity):
            required_materials = []
            children = []
            operations = []
            if has_materials_and_operations:
                required_materials, children = self.get_template_materials_and_children(job, quantity_per_root)
                operations = self.get_template_operations(job, quantity_per_root)
            root_job: JobMst
            mom = MethodOfManufacture(
                make_qty=quantity_per_root,
                requested_qty=quantity_per_root,
                unit_price=unit_price,
                total_price=unit_price * quantity_per_root,
                operations=operations,
                required_materials=required_materials,
                children=children
            )
            mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="template", root=root_job)
            methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    def get_estimated_methods_of_manufacture(self) -> List[MOMWrapper]:
        methods_of_manufacture = []
        estimated_jobs = JobMst.objects.using(self.source_database).filter(type='E', item=self.repeat_part.part_number)
        if estimated_jobs.exists():
            for estimated_job in estimated_jobs:
                methods_of_manufacture += self.get_estimated_methods_of_manufacture_from_job(
                    estimated_job, (estimated_job.qty_released or 1))
        else:
            # some parts (i.e. purchased components) correspond to job materials rather than jobs
            job_materials = JobmatlMst.objects.using(self.source_database).filter(item=self.repeat_part.part_number)
            for job_material in job_materials:
                job_material: JobmatlMst
                parent_job: JobMst = JobMst.objects.using(self.source_database)\
                    .filter(type='E', job=job_material.job, suffix=job_material.suffix).first()
                if parent_job:
                    quantity = (parent_job.qty_released or 1) * (job_material.matl_qty or 1)
                    methods_of_manufacture += self.get_estimated_methods_of_manufacture_from_job(
                        parent_job, quantity, has_materials_and_operations=False)
        return methods_of_manufacture

    def get_job_order_methods_of_manufacture(self, header_type, get_materials_and_children: Callable,
                                             get_operations: Callable) -> List[MOMWrapper]:
        methods_of_manufacture = []
        jobs: JobMst = JobMst.objects.using(self.source_database).filter(type='J', item=self.repeat_part.part_number)
        if jobs.exists():
            for job in jobs:
                methods_of_manufacture += self.get_job_order_methods_of_manufacture_from_job(
                    job, (job.qty_released or 1), header_type, get_materials_and_children, get_operations)
        else:
            # some parts (i.e. purchased components) correspond to job materials rather than jobs
            job_materials = JobmatlMst.objects.using(self.source_database).filter(item=self.repeat_part.part_number)
            for job_material in job_materials:
                job_material: JobmatlMst
                parent_job: JobMst = JobMst.objects.using(self.source_database)\
                    .filter(type='J', job=job_material.job, suffix=job_material.suffix).first()
                if parent_job:
                    quantity = (parent_job.qty_released or 1) * (job_material.matl_qty or 1)
                    methods_of_manufacture += self.get_job_order_methods_of_manufacture_from_job(
                        parent_job, quantity, header_type, get_materials_and_children, get_operations,
                        has_materials_and_operations=False)
        return methods_of_manufacture

    def get_job_order_methods_of_manufacture_from_job(
            self, job: JobMst, total_quantity, header_type,
            get_materials_and_children: Callable, get_operations: Callable, has_materials_and_operations=True):
        required_materials = []
        children = []
        operations = []
        if has_materials_and_operations:
            required_materials, children = get_materials_and_children(job)
            operations = get_operations(job)
        root_job: JobMst = self.get_root_job(job)
        unit_price = 0
        total_price = 0
        if root_job == job:
            if root_job.ord_type == 'O':
                # the job is tied to an order
                order_item: CoitemMst = CoitemMst.objects.using(self.source_database)\
                    .filter(co_num=root_job.ord_num, co_line=root_job.ord_line).first()
                if order_item:
                    unit_price = order_item.price
                    total_price = order_item.price * order_item.qty_ordered
            else:
                # the job is not tied to an order; use the item's standard price
                item_price_data: ItempriceMst = ItempriceMst.objects.using(self.source_database)\
                    .filter(item=root_job.item).first()
                if item_price_data:
                    unit_price = item_price_data.unit_price1 or 0
                    total_price = unit_price * total_quantity
        mom = MethodOfManufacture(
            make_qty=total_quantity,
            requested_qty=total_quantity,
            unit_price=unit_price,
            total_price=total_price,
            operations=operations,
            required_materials=required_materials,
            children=children
        )
        return [MOMWrapper(method_of_manufacture=mom, header_type=header_type, root=root_job)]

    def get_estimated_methods_of_manufacture_from_job(self, job: JobMst, total_quantity,
                                                      has_materials_and_operations=True):
        methods_of_manufacture = []
        required_materials = []
        children = []
        operations = []
        if has_materials_and_operations:
            required_materials, children = self.get_estimated_materials_and_children(job)
            operations = self.get_estimated_operations(job)
        root_job: JobMst = self.get_root_job(job)
        estimate_items = CoitemMst.objects.using(self.source_database)\
            .filter(ref_type='J', ref_num=root_job.job, ref_line_suf=root_job.suffix).all()
        for estimate_item in estimate_items:
            estimate_item: CoitemMst
            if root_job == job:
                unit_price = estimate_item.price
                total_price = estimate_item.price * estimate_item.qty_ordered
            else:
                unit_price = 0
                total_price = 0
            mom = MethodOfManufacture(
                make_qty=total_quantity,
                requested_qty=total_quantity,
                unit_price=unit_price,
                total_price=total_price,
                operations=operations,
                required_materials=required_materials,
                children=children
            )
            mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="estimated", root=estimate_item)
            methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    def get_engineered_methods_of_manufacture(self) -> List[MOMWrapper]:
        return self.get_job_order_methods_of_manufacture("engineered", self.get_engineered_materials_and_children,
                                                         self.get_engineered_operations)

    def get_executed_methods_of_manufacture(self) -> List[MOMWrapper]:
        return self.get_job_order_methods_of_manufacture("executed", self.get_executed_materials_and_children,
                                                         self.get_executed_operations)

    def get_template_materials_and_children(self, job: JobMst, quantity_per_root: Union[Decimal, int]):
        materials = []
        children = []
        job_materials = JobmatlMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        for job_material in job_materials:
            job_material: JobmatlMst
            child_item: ItemMst = ItemMst.objects.using(self.source_database).filter(item=job_material.item).first()
            if child_item and self.get_template_child_job(job_material, child_item):
                # it's a child part
                self.process_child_repeat_part(child_item.item)
                child = Child(
                    part_number=child_item.item,
                    revision=child_item.revision,
                    qty_per_parent=(job_material.matl_qty or 1)
                )
                children.append(child)
            else:
                # it's a material
                item_lot_size = (child_item.lot_size or 1) if child_item else 1
                lot_cost = job_material.units == 'L'

                # the below formulas are from https://docs.infor.com/csb/9.01.x/en-us/csbiolh/mergedprojects/sl_invprod/fields/t/type_item_master_cost_comparisoncost_detailstandard_cost.htm
                if lot_cost:
                    material_cost = (job_material.matl_qty or 1) * (job_material.cost or 0) / item_lot_size
                else:
                    material_cost = (job_material.matl_qty or 1) * (job_material.cost or 0)

                material = RequiredMaterials(
                    name=job_material.item,
                    notes=job_material.description,
                    total_cost=material_cost * quantity_per_root,
                    costing_variables=self.get_shop_operation_costing_variables_from_material(job_material)
                )
                materials.append(material)
        return materials, children

    def get_template_operations(self, job: JobMst, quantity_per_root: Union[Decimal, int]):
        operations = []
        job_operations = JobrouteMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        item: ItemMst = ItemMst.objects.using(self.source_database).filter(item=job.item).first()
        item_lot_size = (item.lot_size or 1) if item else 1
        for job_operation in job_operations:
            job_operation: JobrouteMst

            workcenter: WcMst = job_operation.wc
            if not workcenter:
                continue

            job_operation_schedule_details: JrtSchMst = JrtSchMst.objects.using(self.source_database).filter(
                job=job_operation.job, suffix=job_operation.suffix, oper_num=job_operation.oper_num).first()
            if not job_operation_schedule_details:
                continue

            # the below formulas are from https://docs.infor.com/csb/9.01.x/en-us/csbiolh/mergedprojects/sl_invprod/fields/l/labor_item_master_cost.htm
            setup_cost = ((job_operation.setup_rate or 0) * (job_operation_schedule_details.setup_hrs or 0) * (100 / (job_operation.efficiency or 100))) / item_lot_size
            labor_run_cost = (job_operation.run_rate_lbr or 0) * (job_operation_schedule_details.run_lbr_hrs or 0) * (100 / (job_operation.efficiency or 100))

            # the below formulas are from https://docs.infor.com/csb/9.01.x/en-us/csbiolh/mergedprojects/sl_invprod/fields/o/overhead_item_master_cost_comparisoncost_detailstandard_cost.htm
            fixed_overhead = ((job_operation_schedule_details.run_mch_hrs or 0) * (job_operation.fovhd_rate_mch or 0)) + \
                             (((job_operation_schedule_details.setup_hrs or 0) / item_lot_size) + (job_operation_schedule_details.run_lbr_hrs or 0)) * \
                             (job_operation.fixovhd_rate or 0)
            fixed_overhead *= (100 / (job_operation.efficiency or 100))  # missing from formulas
            variable_overhead = ((job_operation_schedule_details.run_mch_hrs or 0) * (job_operation.vovhd_rate_mch or 0)) + \
                                (((job_operation_schedule_details.setup_hrs or 0) / item_lot_size) + (job_operation_schedule_details.run_lbr_hrs or 0)) * \
                                (job_operation.varovhd_rate or 0)
            variable_overhead *= (100 / (job_operation.efficiency or 100))  # missing from formulas

            total_cost = (setup_cost + labor_run_cost + fixed_overhead + variable_overhead) * quantity_per_root

            operation = Operation(
                is_outside_service=False,
                name=workcenter.wc,
                notes=workcenter.description,
                position=job_operation.oper_num,
                runtime=job_operation_schedule_details.run_mch_hrs or 0,
                setup_time=job_operation_schedule_details.setup_hrs or 0,
                total_cost=total_cost,
                costing_variables=self.get_shop_operation_costing_variables_from_operation(job_operation, workcenter)
            )

            operations.append(operation)
        return operations

    def get_estimated_materials_and_children(self, job: JobMst):
        return self.get_engineered_materials_and_children(job)

    def get_estimated_operations(self, job: JobMst):
        return self.get_engineered_operations(job)

    def get_engineered_materials_and_children(self, job: JobMst):
        materials = []
        children = []
        job_materials = JobmatlMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        for job_material in job_materials:
            job_material: JobmatlMst
            child_item: ItemMst = ItemMst.objects.using(self.source_database).filter(item=job_material.item).first()
            child_job = self.get_child_job(job_material, child_item)
            lot_cost = job_material.units == 'L'

            # the below formulas are from https://docs.infor.com/csb/9.01.x/en-us/csbiolh/lsm1454144442969.html
            if lot_cost:
                material_cost = ((job_material.matl_qty or 1) / (1 - (job_material.scrap_fact or 0))) * (job_material.cost or 0)
            else:
                material_cost = ((job.qty_released or 1) * (job_material.matl_qty or 1) / (1 - (job_material.scrap_fact or 0))) \
                    * (job_material.cost or 0)
            fixed_material_overhead = material_cost * (job_material.fmatlovhd or 0)
            variable_material_overhead = material_cost * (job_material.vmatlovhd or 0)

            total_material_cost = material_cost + fixed_material_overhead + variable_material_overhead

            if child_job:
                # it's a child part
                self.process_child_repeat_part(child_item.item)
                if isinstance(child_job, JobMst):
                    # it's a manufactured/assembled component
                    child = Child(
                        part_number=child_item.item,
                        revision=child_item.revision,
                        qty_per_parent=((child_job.qty_released or 1) / (job.qty_released or 1))
                    )
                else:
                    # it's a purchased component
                    child = Child(
                        part_number=child_item.item,
                        revision=child_item.revision,
                        qty_per_parent=(job_material.matl_qty or 1)
                    )
                children.append(child)
            if not child_job or total_material_cost > 0:
                # it's a material
                material = RequiredMaterials(
                    name=job_material.item,
                    notes=job_material.description,
                    total_cost=total_material_cost,
                    costing_variables=self.get_shop_operation_costing_variables_from_material(job_material)
                )
                materials.append(material)
        return materials, children

    def get_engineered_operations(self, job: JobMst):
        operations = []
        job_operations = JobrouteMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        for job_operation in job_operations:
            job_operation: JobrouteMst

            workcenter: WcMst = job_operation.wc
            if not workcenter:
                continue

            job_operation_schedule_details: JrtSchMst = JrtSchMst.objects.using(self.source_database).filter(
                job=job.job, suffix=job.suffix, oper_num=job_operation.oper_num).first()
            if not job_operation_schedule_details:
                continue

            all_quantity_resources = JrtresourcegroupMst.objects.using(self.source_database).filter(
                job=job_operation.job, suffix=job_operation.suffix, oper_num=job_operation.oper_num)\
                .values_list('qty_resources', flat=True)
            quantity_resources = max(list(all_quantity_resources) or [1])

            efficiency = (job_operation.efficiency or 100) / 100

            # the below formulas are from https://docs.infor.com/csb/9.01.x/en-us/csbiolh/lsm1454144442969.html
            setup_time = (job_operation_schedule_details.setup_hrs or 0) / efficiency
            setup_cost = setup_time * (job_operation.setup_rate or 0)
            fixed_setup_overhead = setup_time * (job_operation.fixovhd_rate or 0)
            variable_setup_overhead = setup_time * (job_operation.varovhd_rate or 0)

            labor_time = (job.qty_released or 1) * (job_operation_schedule_details.run_lbr_hrs or 0) * quantity_resources
            run_cost = labor_time * (job_operation.run_rate_lbr or 0)
            fixed_overhead = labor_time * (job_operation.fixovhd_rate or 0)
            variable_overhead = labor_time * (job_operation.varovhd_rate or 0)

            machine_time = (job.qty_released or 1) * ((job_operation_schedule_details.run_mch_hrs or 0) / efficiency)
            machine_fixed_overhead = machine_time * (job_operation.fovhd_rate_mch or 0)  # there is a typo here in the syteline documentation
            machine_variable_overhead = machine_time * (job_operation.vovhd_rate_mch or 0)  # there is a typo here in the syteline documentation

            total_setup_cost = setup_cost + fixed_setup_overhead + variable_setup_overhead
            total_labor_cost = run_cost + fixed_overhead + variable_overhead
            total_machine_cost = machine_fixed_overhead + machine_variable_overhead
            total_cost = total_setup_cost + total_labor_cost + total_machine_cost

            operation = Operation(
                is_outside_service=False,
                name=workcenter.wc,
                notes=workcenter.description,
                position=job_operation.oper_num,
                runtime=machine_time,
                setup_time=setup_time,
                total_cost=total_cost,
                costing_variables=self.get_shop_operation_costing_variables_from_operation(job_operation, workcenter)
            )

            operations.append(operation)
        return operations

    def get_executed_materials_and_children(self, job: JobMst):
        materials = []
        children = []
        job_materials = JobmatlMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        for job_material in job_materials:
            job_material: JobmatlMst
            material_cost = job_material.a_cost or 0
            child_item: ItemMst = ItemMst.objects.using(self.source_database).filter(item=job_material.item).first()
            child_job = self.get_child_job(job_material, child_item)
            if child_job:
                # it's a child part
                self.process_child_repeat_part(child_item.item)
                if isinstance(child_job, JobMst):
                    # it's a manufactured/assembled component
                    child = Child(
                        part_number=child_item.item,
                        revision=child_item.revision,
                        qty_per_parent=((child_job.qty_released or 1) / (job.qty_released or 1))
                    )
                else:
                    # it's a purchased component
                    child = Child(
                        part_number=child_item.item,
                        revision=child_item.revision,
                        qty_per_parent=(job_material.matl_qty or 1)
                    )
                children.append(child)
            if not child_job or material_cost > 0:
                # it's a material
                material = RequiredMaterials(
                    name=job_material.item,
                    notes=job_material.description,
                    total_cost=material_cost,
                    costing_variables=self.get_shop_operation_costing_variables_from_material(job_material)
                )
                materials.append(material)
        return materials, children

    def get_executed_operations(self, job: JobMst):
        operations = []
        job_operations = JobrouteMst.objects.using(self.source_database).filter(job=job.job, suffix=job.suffix)
        for job_operation in job_operations:
            job_operation: JobrouteMst

            workcenter: WcMst = job_operation.wc
            if not workcenter:
                continue

            total_cost = (job_operation.setup_cost_t or 0) + (job_operation.fixovhd_t_mch or 0) + (job_operation.varovhd_t_mch or 0) \
                + (job_operation.run_cost_t_lbr or 0) + (job_operation.fixovhd_t_lbr or 0) + (job_operation.varovhd_t_lbr or 0)

            operation = Operation(
                is_outside_service=False,
                name=workcenter.wc,
                notes=workcenter.description,
                position=job_operation.oper_num,
                runtime=job_operation.run_hrs_t_mch or 0,
                setup_time=job_operation.setup_hrs_t or 0,
                total_cost=total_cost,
                costing_variables=self.get_shop_operation_costing_variables_from_operation(job_operation, workcenter)
            )

            operations.append(operation)
        return operations

    def get_template_child_job(self, child_material: JobmatlMst, child_item: ItemMst):
        config: RepeatPartImportConfig = self._importer.erp_config
        product_code = get_product_code(child_item, self.source_database)
        if product_code in config.material_product_codes:
            return None
        if product_code in config.purchased_component_product_codes:
            return child_material
        return JobMst.objects.using(self.source_database)\
            .filter(item=child_item.item, type='S', mo_bom_alternate_id='Current').first()

    def get_child_job(self, child_material: JobmatlMst, child_item: ItemMst):
        config: RepeatPartImportConfig = self._importer.erp_config
        if child_item:
            product_code = get_product_code(child_item, self.source_database)
            if product_code in config.material_product_codes:
                return None
            if product_code in config.purchased_component_product_codes:
                return child_material
        return JobMst.objects.using(self.source_database)\
            .filter(job=child_material.ref_num, suffix=child_material.ref_line_suf).first()

    def get_root_job(self, job: JobMst):
        job_material: JobmatlMst = JobmatlMst.objects.using(self.source_database)\
            .filter(ref_type='J', ref_num=job.job, ref_line_suf=job.suffix).first()
        if job_material:
            parent_job = JobMst.objects.using(self.source_database)\
                .filter(job=job_material.job, suffix=job_material.suffix).first()
            if parent_job:
                return self.get_root_job(parent_job)
        return job

    def get_root_template_jobs(self, job: JobMst, quantity_per_root: Union[Decimal, int] = 1):
        root_jobs = [(job, quantity_per_root)]
        job_materials = JobmatlMst.objects.using(self.source_database).filter(item=job.item)
        for job_material in job_materials:
            job_material: JobmatlMst
            material_quantity = job_material.matl_qty or 1
            parent_job: JobMst = JobMst.objects.using(self.source_database).filter(
                job=job_material.job, suffix=job_material.suffix, type='S', mo_bom_alternate_id='Current').first()
            if parent_job:
                root_jobs += self.get_root_template_jobs(parent_job, material_quantity)
        return root_jobs

    def process_child_repeat_part(self, item_number):
        self.repeat_part.type = "assembled"
        if self.create_child_parts:
            logger.info(f"Creating child parts for {item_number}")
            self._importer._process_repeat_part(item_number, create_child_parts=True)

    def get_shop_operation_costing_variables_from_material(self, job_material: JobmatlMst):
        costing_var_dict = get_material_costing_variables(job_material)
        return self.get_shop_operation_costing_variables(costing_var_dict)

    def get_shop_operation_costing_variables_from_operation(self, job_operation: JobrouteMst, work_center: WcMst):
        costing_var_dict = get_operation_costing_variables(job_operation, work_center)
        return self.get_shop_operation_costing_variables(costing_var_dict)

    def get_shop_operation_costing_variables(self, costing_vars: dict) -> List[CostingVariable]:
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
