from decimal import Decimal
from typing import List, Union, Callable

from baseintegration.utils.repeat_work_objects import MethodOfManufacture, Operation, RequiredMaterials, Child, \
    CostingVariable, Part
from baseintegration.utils.repeat_work_utils import MOMWrapper
from m2m.importer.processors.base import BaseM2MImportProcessor
from m2m.models import Qtitem, Qtpest, Qtdbom, Qtdrtg, Inwork, Inboms, Inbomm, Inrtgs, Inmastx, Jomast, \
    Sorels, Jodbom, Jodrtg, MaJobmaterialsummary, MaJoblaborsummary, Joitem
from baseintegration.datamigration import logger
from m2m.utils.repeat_work_utils import get_operation_costing_variables, \
    get_estimated_quote_material_costing_variables, get_estimated_standard_material_costing_variables, PartData, \
    get_engineered_material_costing_variables, JobMaterialData, JobData, get_first_cached, get_first_in_queryset, \
    TemplateRoot


class MethodOfManufactureProcessor(BaseM2MImportProcessor):
    def _process(self, repeat_part: Part, part_data: PartData, create_child_parts: bool) -> List[MOMWrapper]:
        self.source_database = self._importer.source_database
        logger.info(f"Creating repeat part methods of manufacture from M2M item ID: {part_data.id()}")

        self.create_child_parts = create_child_parts
        self.repeat_part = repeat_part

        methods_of_manufacture = []

        methods_of_manufacture += self.get_template_methods_of_manufacture(part_data)
        methods_of_manufacture += self.get_estimated_methods_of_manufacture(part_data)
        methods_of_manufacture += self.get_engineered_methods_of_manufacture(part_data)
        methods_of_manufacture += self.get_executed_methods_of_manufacture(part_data)

        return methods_of_manufacture

    def get_template_methods_of_manufacture(self, part_data: PartData) -> List[MOMWrapper]:
        methods_of_manufacture = []

        item: Inmastx = part_data.entry
        if type(item) is not Inmastx:
            return []

        routing_steps = Inrtgs.objects.using(self.source_database).filter(fpartno=item.fpartno, fcpartrev=item.frev)
        child_boms = Inboms.objects.using(self.source_database).filter(
            fparent=part_data.part_number, fparentrev=part_data.revision)
        root_items_with_quantities = self._get_root_items(item)
        for (root, quantity_per_root) in root_items_with_quantities:
            total_quantity = quantity_per_root  # for template type, root quantity will always be 1
            total_price = item.f2totcost
            unit_price = total_price / (total_quantity or 1)
            operations = self._get_operations(routing_steps, total_quantity)
            required_materials, children = self.get_materials_and_children_from_standard_bom(
                child_boms, total_quantity)
            mom = MethodOfManufacture(
                requested_qty=total_quantity,
                make_qty=total_quantity,
                unit_price=unit_price,
                total_price=total_price,
                operations=operations,
                required_materials=required_materials,
                children=children,
            )
            mom_wrapper = MOMWrapper(mom, "template", root)
            methods_of_manufacture.append(mom_wrapper)

        return methods_of_manufacture

    def get_estimated_methods_of_manufacture(self, part_data: PartData) -> List[MOMWrapper]:
        methods_of_manufacture = []
        methods_of_manufacture += self._get_estimated_methods_of_manufacture_from_quote_boms(part_data)
        methods_of_manufacture += self._get_estimated_methods_of_manufacture_from_standard_boms(part_data)
        return methods_of_manufacture

    def _get_estimated_methods_of_manufacture_from_quote_boms(self, part_data: PartData) -> List[MOMWrapper]:
        """
        This will get MOMs for all quote items containing the part that DO NOT have
        "Use Standard Boms And Routings" checked. Such quote items will have quote-specific BOMs and routings.
        """
        methods_of_manufacture = []

        # first find all child boms
        quote_boms = Qtdbom.objects.using(self.source_database).filter(
            fbompart=part_data.part_number, fbomrev=part_data.revision) \
            .exclude(flevel=' 0')

        # now find all root boms
        quote_items = Qtitem.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision)
        for quote_item in quote_items:
            quote_item: Qtitem
            root_bom_lines = Qtdbom.objects.using(self.source_database).filter(
                fquoteno=quote_item.fquoteno, finumber=quote_item.finumber, flevel=' 0')
            quote_boms |= root_bom_lines

        for quote_bom in quote_boms:
            quote_bom: Qtdbom
            is_root = int(quote_bom.flevel) == 0
            root_quote_item: Qtitem = Qtitem.objects.using(self.source_database).filter(
                fquoteno=quote_bom.fquoteno, finumber=quote_bom.finumber) \
                .first()
            if root_quote_item:
                quote_bom_is_component = self._quote_bom_line_is_component(quote_bom)
                should_process = is_root or quote_bom_is_component
                if should_process:
                    quantity_per_root = Decimal((quote_bom.fextqty or 1) / (root_quote_item.festqty or 1))
                    methods_of_manufacture += self._get_estimated_methods_of_manufacture_for_quote_item(
                        part_data, root_quote_item, quantity_per_root, is_root, quote_bom)

        return methods_of_manufacture

    def _get_estimated_methods_of_manufacture_from_standard_boms(self, part_data: PartData) \
            -> List[MOMWrapper]:
        """
        This will get MOMs for all quote items containing the part that DO have "Use Standard Boms And Routings"
        checked. Such quote items use the item master's standard BOMs and routings.
        """
        methods_of_manufacture = []

        item: Inmastx = part_data.entry
        if type(item) is not Inmastx:
            return []

        standard_bom_lines = Inboms.objects.using(self.source_database).filter(
            fcomponent=item.fpartno, fcomprev=item.frev)
        for standard_bom_line in standard_bom_lines:
            standard_bom_line: Inboms
            should_process = self._standard_bom_line_is_component(standard_bom_line, item)
            if should_process:
                root_quote_items_with_quantities = self._get_root_quote_items(standard_bom_line)
                for (root_quote_item, quantity_per_root) in root_quote_items_with_quantities:
                    methods_of_manufacture += self._get_estimated_methods_of_manufacture_for_quote_item(
                        part_data, root_quote_item, quantity_per_root, is_root=False)

        return methods_of_manufacture

    def _get_estimated_methods_of_manufacture_for_quote_item(self, part_data, root_quote_item, quantity_per_root,
                                                             is_root, quote_bom=None):
        use_standard_bom_and_routing = root_quote_item.fstandpart and not root_quote_item.fdet_bom
        if use_standard_bom_and_routing:
            routing_steps = Inrtgs.objects.using(self.source_database).filter(
                fpartno=part_data.part_number, fcpartrev=part_data.revision)
            child_boms = Inboms.objects.using(self.source_database).filter(
                fparent=part_data.part_number, fparentrev=part_data.revision)
        elif quote_bom:
            routing_steps = Qtdrtg.objects.using(self.source_database).filter(
                fquoteno=quote_bom.fquoteno, finumber=quote_bom.finumber, fbominum=quote_bom.fbominum)
            child_boms = Qtdbom.objects.using(self.source_database).filter(
                fquoteno=quote_bom.fquoteno, finumber=quote_bom.finumber, fparinum=quote_bom.fbominum)
        else:
            return []
        methods_of_manufacture = []
        quote_item_quantities = Qtpest.objects.using(self.source_database).filter(
            fquoteno=root_quote_item.fquoteno, fenumber=root_quote_item.fenumber)
        for quote_item_quantity in quote_item_quantities:
            quote_item_quantity: Qtpest
            root_quantity = quote_item_quantity.fquantity or 1
            total_quantity = quantity_per_root * root_quantity
            if is_root:
                unit_price = quote_item_quantity.funetprice
                total_price = quote_item_quantity.funettxnpric
            else:
                unit_price = 0
                total_price = 0
            operations = self._get_operations(routing_steps, total_quantity)
            if use_standard_bom_and_routing:
                required_materials, children = self.get_materials_and_children_from_standard_bom(
                    child_boms, total_quantity)
            else:
                required_materials, children = self.get_estimated_materials_and_children_from_quote_bom(
                    child_boms, total_quantity)
            mom = MethodOfManufacture(
                requested_qty=total_quantity,
                make_qty=total_quantity,
                unit_price=unit_price,
                total_price=total_price,
                operations=operations,
                required_materials=required_materials,
                children=children,
            )
            mom_wrapper = MOMWrapper(mom, "estimated", root_quote_item)
            methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    def _get_root_quote_items(self, bom_line: Inboms, running_quantity=1, quantity_frozen=False) \
            -> List[tuple[Qtitem, int]]:
        """
        Returns a list of (root quote item, quantity of bom line per 1 root quote item)
        """
        quote_items = []
        if not quantity_frozen:
            running_quantity *= (bom_line.fqty or 1)
        if not bom_line.flextend:
            # if "extend" is not checked, then this is the total quantity of the material, regardless of the quantities
            # of its ancestors
            quantity_frozen = True
        parent_part = bom_line.fparent
        parent_rev = bom_line.fparentrev
        standard_bom = Inbomm.objects.using(self.source_database).filter(fpartno=parent_part, fcpartrev=parent_rev)\
            .first()
        if standard_bom:
            found_quote_items = Qtitem.objects.using(self.source_database).filter(
                fstandpart=True, fpartno=parent_part, fpartrev=parent_rev)
            for found_quote_item in found_quote_items:
                found_quote_item: Qtitem
                quote_items.append((found_quote_item, running_quantity))
        parent_bom_lines = Inboms.objects.using(self.source_database).filter(
            fcomponent=parent_part, fcomprev=parent_rev)
        for parent_bom_line in parent_bom_lines:
            parent_bom_line: Inboms
            quote_items += self._get_root_quote_items(parent_bom_line, running_quantity, quantity_frozen)
        return quote_items

    def _get_root_items(self, item: Inmastx, running_quantity=1, quantity_frozen=False) \
            -> List[tuple[TemplateRoot, int]]:
        """
        Returns a list of (root item, quantity of item per 1 root item)
        """
        items = []
        standard_bom = Inbomm.objects.using(self.source_database).filter(fpartno=item.fpartno, fcpartrev=item.frev)\
            .first()
        if standard_bom:
            template_root = TemplateRoot(item, standard_bom)
            items.append((template_root, running_quantity))
        bom_lines = Inboms.objects.using(self.source_database).filter(
            fcomponent=item.fpartno, fcomprev=item.frev)
        for bom_line in bom_lines:
            bom_line: Inboms
            quantity = running_quantity
            if not quantity_frozen:
                quantity *= (bom_line.fqty or 1)
            new_quantity_frozen = quantity_frozen
            if not bom_line.flextend:
                # if "extend" is not checked, then this is the total quantity of the material, regardless of the
                # quantities of its ancestors
                new_quantity_frozen = True
            parent_item: Inmastx = Inmastx.objects.filter(fpartno=bom_line.fparent, frev=bom_line.fparentrev).first()
            if parent_item:
                items += self._get_root_items(parent_item, quantity, new_quantity_frozen)
        return items

    def get_estimated_materials_and_children_from_quote_bom(
            self, child_boms, total_quantity: int) -> (List[RequiredMaterials], List[Child]):
        """
        We get the materials and children in a single method to reduce the number of queries.
        """
        children = []
        materials = []
        for child_bom in child_boms:
            child_bom: Qtdbom
            quantity_per_parent = child_bom.ftotqty
            is_child = self._quote_bom_line_is_component(child_bom)
            if is_child:
                self.process_child_repeat_part(child_bom.fbompart, child_bom.fbomrev)
                child = Child(
                    part_number=self.generate_normalized_value(child_bom.fbompart),
                    revision=self.generate_normalized_value(child_bom.fbomrev),
                    qty_per_parent=quantity_per_parent,
                )
                children.append(child)
            total_cost = child_bom.fmatlcost * quantity_per_parent
            if child_bom.flextend:
                total_cost *= total_quantity
            is_material = not is_child or total_cost > 0  # some child components have material costs
            if is_material:
                costing_var_dict = get_estimated_quote_material_costing_variables(child_bom)
                material = RequiredMaterials(
                    name=self.generate_normalized_value(child_bom.fbompart),
                    notes=self.generate_normalized_value(child_bom.fbomdesc),
                    total_cost=total_cost,
                    costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(material)
        return materials, children

    def get_materials_and_children_from_standard_bom(self, child_boms, total_quantity: int) \
            -> (List[RequiredMaterials], List[Child]):
        """
        We get the materials and children in a single method to reduce the number of queries.
        """
        children = []
        materials = []
        for child_bom in child_boms:
            child_bom: Inboms
            quantity_per_parent = child_bom.fqty
            item: Inmastx = Inmastx.objects.using(self.source_database).filter(
                fpartno=child_bom.fcomponent, frev=child_bom.fcomprev).first()
            if item:
                is_child = self._standard_bom_line_is_component(child_bom, item)
                if is_child:
                    self.process_child_repeat_part(item.fpartno, item.frev)
                    child = Child(
                        part_number=self.generate_normalized_value(item.fpartno),
                        revision=self.generate_normalized_value(item.frev),
                        qty_per_parent=quantity_per_parent,
                    )
                    children.append(child)
                total_cost = item.f2matlcost * quantity_per_parent
                if child_bom.flextend:
                    total_cost *= total_quantity
                is_material = not is_child or total_cost > 0  # some child components have material costs
                if is_material:
                    costing_var_dict = get_estimated_standard_material_costing_variables(child_bom, item)
                    material = RequiredMaterials(
                        name=self.generate_normalized_value(child_bom.fcomponent),
                        notes=self.generate_normalized_value(child_bom.fbommemo),
                        total_cost=total_cost,
                        costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
                    )
                    materials.append(material)
        return materials, children

    def get_engineered_methods_of_manufacture(self, part_data: PartData):
        jobs = Jomast.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision, ftype="C")
        return self._get_job_methods_of_manufacture(
            part_data, jobs, "engineered", self.get_engineered_operations, self._get_engineered_material_data)

    def get_engineered_operations(self, job: Jomast) -> List[Operation]:
        routing_steps = Jodrtg.objects.using(self.source_database).filter(fjobno=job.fjobno)
        return self._get_operations(routing_steps, 1)

    @classmethod
    def _get_engineered_material_data(cls, job: Jomast, bom_line: Jodbom):
        quantity_per_parent = bom_line.ftotqty
        material_cost = bom_line.fmatlcost * quantity_per_parent
        if bom_line.flextend:
            material_cost *= job.fquantity
        return JobMaterialData(
            type="engineered",
            quantity_per_parent=quantity_per_parent,
            material_cost=material_cost
        )

    def get_executed_methods_of_manufacture(self, part_data: PartData):
        jobs = Jomast.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision, ftype="C",
            fstatus__in=["CLOSED", "COMPLETED", "RELEASED"])
        return self._get_job_methods_of_manufacture(
            part_data, jobs, "executed", self.get_executed_operations, self._get_executed_material_data)

    def get_executed_operations(self, job: Jomast) -> List[Operation]:
        operations = []

        # The below query is slightly concerning since we use an f-string in a raw SQL query.
        # We use an f-string over parameters here because it is much faster.
        # Since job is guaranteed to be an existing job in M2M, and we do not write to jobs,
        # it is not much of a security risk.
        job_summary_query = f"SELECT * FROM MA_JobLaborSummary WHERE jobno = '{job.fjobno}'"

        routing_steps = MaJoblaborsummary.objects.using(self.source_database).raw(job_summary_query)
        routing_step_estimates = Jodrtg.objects.using(self.source_database).filter(fjobno=job.fjobno)
        for routing_step in routing_steps:
            routing_step: MaJoblaborsummary
            work_center: Inwork = get_first_cached(Inwork, fcpro_id=routing_step.workcenterid)
            if work_center:
                op_name = self.generate_normalized_value(work_center.fcpro_name)
            else:
                op_name = self.generate_normalized_value(routing_step.workcentername)
            is_outside_service = routing_step.workcenterid.upper().startswith("SUB")
            setup_time = routing_step.actualsetuphours
            run_time = routing_step.actualprodhours
            setup_cost = routing_step.actualsetupcost
            prod_cost = routing_step.actualprodcost
            cost = setup_cost + prod_cost + routing_step.actualoverheadcost
            routing_step_estimate = get_first_in_queryset(routing_step_estimates, foperno=routing_step.operationno)
            if routing_step_estimate:
                costing_var_dict = get_operation_costing_variables(routing_step_estimate, work_center)
            else:
                costing_var_dict = {}
            operation = Operation(
                is_finish=False,
                is_outside_service=is_outside_service,
                name=op_name,
                notes=self.generate_normalized_value(routing_step.description),
                position=routing_step.operationno,
                runtime=run_time,
                setup_time=setup_time,
                total_cost=cost,
                costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
            )
            operations.append(operation)
        return operations

    def _get_executed_material_data(self, job: Jomast, bom_line: Jodbom):
        # The below query is slightly concerning since we use an f-string in a raw SQL query.
        # We use an f-string over parameters here because it is much faster.
        # Since job is guaranteed to be an existing job in M2M, and bom_line is guaranteed to be an existing
        # job BOM line, and we do not write to jobs or their BOMs, it is not much of a security risk.
        material_summary_query = f"SELECT * FROM MA_JobMaterialSummary WHERE jobno = '{job.fjobno}' " \
                                 f"AND partno = '{bom_line.fbompart}'"

        material_summaries = MaJobmaterialsummary.objects.raw(material_summary_query)
        material_summaries_count = len(material_summaries)
        if material_summaries_count > 0:
            if material_summaries_count > 1:
                # filter result even further
                preferred_material_summaries = [m for m in material_summaries if m.actualquantity > 0]
                material_summaries = preferred_material_summaries or material_summaries
            material_summary: MaJobmaterialsummary = material_summaries[0]
            quantity_per_parent = (material_summary.actualquantity or 1) / (job.fquantity or 1)
            material_cost = material_summary.actualmaterialcost
        else:
            quantity_per_parent = 1
            material_cost = 0
        return JobMaterialData(
            type="executed",
            quantity_per_parent=quantity_per_parent,
            material_cost=material_cost
        )

    def _get_root_job(self, job: Jomast) -> Jomast:
        parent_job_number = job.fsub_from
        if not parent_job_number.strip():  # this means the job has no parent, i.e. it's the root
            return job
        parent_job = Jomast.objects.using(self.source_database).filter(fjobno=parent_job_number).first()
        return self._get_root_job(parent_job)

    def _get_operations(self, routing_steps: List[Union[Qtdrtg, Inrtgs, Jodrtg]], total_quantity: int) \
            -> List[Operation]:
        operations = []
        for routing_step in routing_steps:
            work_center: Inwork = get_first_cached(Inwork, fcpro_id=routing_step.fpro_id)
            if work_center:
                op_name = self.generate_normalized_value(work_center.fcpro_name)
            else:
                op_name = self.generate_normalized_value(routing_step.fpro_id)
            is_outside_service = routing_step.fpro_id.upper().startswith("SUB")
            quantity = routing_step.foperqty * total_quantity
            setup_time = routing_step.fsetuptime
            run_time = routing_step.fuprodtime * quantity
            if is_outside_service:
                total_cost = routing_step.fusubcost * quantity + routing_step.ffixcost
            else:
                hours = run_time + setup_time
                rate = routing_step.fulabcost + routing_step.fuovrhdcos
                total_cost = rate * hours + routing_step.fothrcost
            costing_var_dict = get_operation_costing_variables(routing_step, work_center)
            operation = Operation(
                is_finish=False,
                is_outside_service=is_outside_service,
                name=op_name,
                notes=self.generate_normalized_value(routing_step.fopermemo),
                position=routing_step.foperno,
                runtime=run_time,
                setup_time=setup_time,
                total_cost=total_cost,
                costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
            )
            operations.append(operation)
        return operations

    def _get_job_methods_of_manufacture(
            self, part_data: PartData, jobs: List[Jomast], mom_type: str,
            get_operations: Callable[[Jomast], List[Operation]],
            get_material_data: Callable[[Jomast, Jodbom], JobMaterialData]
    ):
        methods_of_manufacture = []
        job_items = Joitem.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision)
        for job in jobs:
            job: Jomast
            root_job = self._get_root_job(job)
            job_item: Joitem = get_first_in_queryset(job_items, fjobno=job.fjobno)
            if job_item:
                job_data = self._get_job_data(job, job_item)
                operations = get_operations(job)
                required_materials, children = self._get_job_materials_and_children(job, get_material_data)
                mom = MethodOfManufacture(
                    requested_qty=job_data.quantity,
                    make_qty=job_data.quantity,
                    unit_price=job_data.unit_price,
                    total_price=job_data.total_price,
                    operations=operations,
                    required_materials=required_materials,
                    children=children,
                )
                mom_wrapper = MOMWrapper(mom, mom_type, root_job)
                methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    def _get_job_data(self, job: Jomast, job_item: Joitem) -> JobData:
        quantity = job.fquantity or 1
        sales_order_data: Sorels = Sorels.objects.using(self.source_database).filter(
            fsono=job_item.fsono, finumber=job_item.finumber).first()
        if sales_order_data:
            unit_price = sales_order_data.funetprice
            total_price = sales_order_data.funetprice * quantity
        else:
            unit_price = 0
            total_price = 0
        return JobData(
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )

    def _get_job_materials_and_children(
            self, job: Jomast, get_material_data: Callable[[Jomast, Jodbom], JobMaterialData]) \
            -> (List[RequiredMaterials], List[Child]):
        """
        We get the materials and children in a single method to reduce the number of queries.
        """
        children = []
        materials = []
        child_boms = Jodbom.objects.using(self.source_database).filter(fjobno=job.fjobno)
        for child_bom in child_boms:
            child_bom: Jodbom
            material_data = get_material_data(job, child_bom)
            is_child = self._job_bom_line_is_component(child_bom)
            if is_child:
                self.process_child_repeat_part(child_bom.fbompart, child_bom.fbomrev)
                child = Child(
                    part_number=self.generate_normalized_value(child_bom.fbompart),
                    revision=self.generate_normalized_value(child_bom.fbomrev),
                    qty_per_parent=material_data.quantity_per_parent,
                )
                children.append(child)
            is_material = not is_child or material_data.material_cost > 0  # some child components have material costs
            if is_material:
                costing_var_dict = get_engineered_material_costing_variables(child_bom)
                material = RequiredMaterials(
                    name=self.generate_normalized_value(child_bom.fbompart),
                    notes=self.generate_normalized_value(child_bom.fstdmemo),
                    total_cost=material_data.material_cost,
                    costing_variables=self._get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(material)
        return materials, children

    def process_child_repeat_part(self, part_number, revision):
        self.repeat_part.type = "assembled"
        if self.create_child_parts:
            logger.info(f"Creating child parts for {part_number} - {revision}")
            self._importer._process_repeat_part((part_number, revision), create_child_parts=True)

    def _quote_bom_line_is_component(self, quote_bom_line: Qtdbom) -> bool:
        """
        Returns whether the given BOM line represents a component, rather than a material.
        """
        has_children = Qtdbom.objects.using(self.source_database).filter(
            fquoteno=quote_bom_line.fquoteno, finumber=quote_bom_line.finumber,
            fparinum=quote_bom_line.fbominum).exists()
        return self._is_component(quote_bom_line.fbomsource, has_children)

    def _standard_bom_line_is_component(self, standard_bom_line: Inboms, item: Inmastx) -> bool:
        """
        Returns whether the given BOM line represents a component, rather than a material.
        """
        has_children = Inboms.objects.using(self.source_database).filter(
            fparent=standard_bom_line.fcomponent, fparentrev=standard_bom_line.fcomprev).exists()
        return self._is_component(item.fsource, has_children)

    def _job_bom_line_is_component(self, job_bom_line: Jodbom) -> bool:
        """
        Returns whether the given BOM line represents a component, rather than a material.
        """
        sub_job_no = job_bom_line.fsub_job
        is_sub_job = bool(sub_job_no.strip())
        # verify that the sub job actually exists as a job; if not, treat it as a material
        if is_sub_job and not Jomast.objects.using(self.source_database).filter(fjobno=sub_job_no).exists():
            return False
        return self._is_component(job_bom_line.fbomsource, is_sub_job)

    @classmethod
    def _is_component(cls, source: str, has_children: bool) -> bool:
        """
        Returns whether the part with the given properties should be considered a component, rather than a material.
        """
        return source == 'M' or has_children

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
