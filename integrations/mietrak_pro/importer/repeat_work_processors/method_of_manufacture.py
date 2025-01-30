import math
from decimal import Decimal
from typing import List, Callable

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get
from baseintegration.utils.repeat_work_objects import MethodOfManufacture, \
    Operation, RequiredMaterials, Child, CostingVariable, Part
from baseintegration.utils.repeat_work_utils import MOMWrapper
from mietrak_pro.models import Item, Quote, Quoteassembly, \
    Operation as MTPOperation, Quotequantity, Workorder, Router, Workorderrelease, \
    Workorderassembly, Workcenter, Workordercompletion, Workordertotal, Workorderissuing, Workordercollection, \
    Workordertypeofhour, Calculationtype, Workcentertype, Routerworkcenter, Iteminventory
from baseintegration.datamigration import logger
from mietrak_pro.utils.repeat_work_utils import get_estimated_operation_costing_variables, \
    get_estimated_material_costing_variables, get_engineered_operation_costing_variables, \
    get_engineered_material_costing_variables, MoMQuantityData, OperationData, MoMCostData, \
    MoMTemplateQuantityData, get_template_operation_costing_variables, get_template_material_costing_variables


class MethodOfManufactureProcessor(BaseImportProcessor):
    def _process(self, repeat_part: Part, item: Item, create_child_parts: bool):
        logger.info(f"Creating repeat part methods of manufacture from Mie Trak Pro item ID: {item.pk}")

        self.create_child_parts = create_child_parts
        self.repeat_part = repeat_part

        methods_of_manufacture = []

        methods_of_manufacture += self.get_template_methods_of_manufacture(item)
        methods_of_manufacture += self.get_estimated_methods_of_manufacture(item)
        methods_of_manufacture += self.get_engineered_methods_of_manufacture(item)
        methods_of_manufacture += self.get_executed_methods_of_manufacture(item)

        return methods_of_manufacture

    def get_template_methods_of_manufacture(self, item: Item) -> List[MOMWrapper]:
        methods_of_manufacture = []
        routers = Router.objects.filter(itemfk=item)
        for router in routers:
            router: Router
            router_work_centers = Routerworkcenter.objects.filter(routerfk=router)\
                .select_related('workcenterfk__workcentertypefk', 'itemfk__iteminventoryfk', 'unitofmeasuresetfk',
                                'itemrouterfk__itemfk')
            for quantity_data in self.get_template_roots_with_quantities(router):
                root_router = quantity_data.root
                total_price = item.sellprice1 or 0
                unit_price = total_price / (item.quantity1 or 1)
                total_quantity = quantity_data.total_quantity or 1
                mom = MethodOfManufacture(
                    requested_qty=total_quantity,
                    make_qty=total_quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    operations=self.get_template_operations(router_work_centers, total_quantity),
                    required_materials=self.get_template_required_materials(router_work_centers, total_quantity),
                    children=self.get_template_children(router_work_centers)
                )
                mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="template", root=root_router)
                methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    @classmethod
    def get_template_roots_with_quantities(cls, router: Router, running_quantity=1) -> List[MoMTemplateQuantityData]:
        roots = []

        router_work_centers = Routerworkcenter.objects.filter(itemrouterfk=router)
        for router_work_center in router_work_centers:
            router_work_center: Routerworkcenter
            parent_router: Router = router_work_center.routerfk
            quantity_required = router_work_center.quantityrequired
            roots += cls.get_template_roots_with_quantities(parent_router, running_quantity * int(quantity_required))

        roots.append(
            MoMTemplateQuantityData(
                root=router,
                total_quantity=running_quantity,
            )
        )

        return roots

    @classmethod
    def get_template_operations(cls, router_work_centers, total_quantity: int) -> List[Operation]:
        operations = []
        for router_work_center in router_work_centers:
            router_work_center: Routerworkcenter
            work_center: Workcenter = router_work_center.workcenterfk
            if work_center:
                setup_hours = router_work_center.setuptime / 60
                run_hours = (router_work_center.minutesperpart / 60) * total_quantity
                total_hours = setup_hours + run_hours
                work_center: Workcenter = router_work_center.workcenterfk
                hourly_rate = (work_center.averageemployeeoverheadrate or 0) + \
                              (work_center.hourlyoverhead or 0) + \
                              (work_center.averageemployeerate or 0)
                cost = total_hours * hourly_rate
                costing_var_dict = get_template_operation_costing_variables(router_work_center, work_center)
                operation = Operation(
                    is_finish=False,
                    is_outside_service=cls.get_is_outside_service(work_center),
                    name=work_center.description,
                    notes=router_work_center.comment,
                    position=router_work_center.sequencenumber,
                    runtime=run_hours,
                    setup_time=setup_hours,
                    total_cost=cost,
                    costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                )
                operations.append(operation)
        return operations

    @classmethod
    def get_template_material_cost(cls, router_work_center: Routerworkcenter):
        item: Item = router_work_center.itemfk
        if item:
            item_inventory: Iteminventory = item.iteminventoryfk
            if item_inventory:
                return item_inventory.standardcost or 0
        return router_work_center.price or 0

    @classmethod
    def get_template_required_materials(cls, router_work_centers, total_quantity: int) -> List[RequiredMaterials]:
        materials = []
        for router_work_center in router_work_centers:
            router_work_center: Routerworkcenter
            item: Item = router_work_center.itemfk
            if item:
                unit_cost = cls.get_template_material_cost(router_work_center)
                quantity = (router_work_center.quantityrequired or 1) * total_quantity
                total_cost = unit_cost * quantity
                costing_var_dict = get_template_material_costing_variables(router_work_center, item)
                material = RequiredMaterials(
                    name=item.partnumber,
                    notes=router_work_center.comment,
                    total_cost=total_cost,
                    costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(material)
        return materials

    def get_template_children(self, router_work_centers) -> List[Child]:
        children = []
        for router_work_center in router_work_centers:
            router_work_center: Routerworkcenter
            child_router: Router = router_work_center.itemrouterfk
            if child_router:
                item: Item = child_router.itemfk
                self.process_child_repeat_part(item.pk)
                child = Child(
                    part_number=item.partnumber,
                    revision=item.revision,
                    qty_per_parent=router_work_center.quantityrequired,
                )
                children.append(child)
        return children

    def get_estimated_methods_of_manufacture(self, item: Item) -> List[MOMWrapper]:
        methods_of_manufacture = []
        quotes = Quote.objects.filter(itemfk=item).select_related('customerfk')
        for quote in quotes:
            quote: Quote
            for quantity_data in self.get_roots_with_quantities(quote):
                root_quote = quantity_data.root
                delivery = quantity_data.quantity_data.delivery or 1
                unit_price = quantity_data.quantity_data.price or 0
                total_quantity = quantity_data.total_quantity or 1
                total_price = unit_price * total_quantity
                quote_assemblies = Quoteassembly.objects.filter(
                    quotefk=root_quote, parentquoteassemblyfk=quantity_data.linking_assembly)\
                    .select_related('operationfk__workcenterfk', 'itemfk', 'unitofmeasuresetfk',
                                    'partyfk', 'itemquotefk__itemfk')
                mom = MethodOfManufacture(
                    requested_qty=total_quantity,
                    make_qty=total_quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    operations=self.get_estimated_operations(quote_assemblies, total_quantity, delivery),
                    required_materials=self.get_estimated_required_materials(quote_assemblies, total_quantity),
                    children=self.get_estimated_children(quote_assemblies)
                )
                mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="estimated", root=root_quote)
                methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    @classmethod
    def get_estimated_operations(cls, quote_assemblies, total_quantity: int, delivery: int) -> List[Operation]:
        operations = []
        for quote_assembly in quote_assemblies:
            quote_assembly: Quoteassembly
            mtp_operation: MTPOperation = quote_assembly.operationfk
            if mtp_operation:
                run_time_hours = (quote_assembly.runtime or 0) / 60
                setup_time_hours = (quote_assembly.setuptime or 0) / 60
                total_cost = (float(quote_assembly.setupcost or 0) * float(delivery)) + \
                    (float(quote_assembly.runcost or 0) * float(total_quantity))
                workcenter = mtp_operation.workcenterfk
                if not workcenter:
                    workcenter = Workcenter.objects.filter(description=mtp_operation.name)\
                        .select_related('workcentertypefk').first()
                if workcenter:
                    costing_var_dict = get_estimated_operation_costing_variables(
                        quote_assembly, workcenter)
                    operation = Operation(
                        is_finish=False,
                        is_outside_service=cls.get_is_outside_service(workcenter),
                        name=mtp_operation.name,
                        notes=quote_assembly.comment,
                        position=quote_assembly.sequencenumber,
                        runtime=run_time_hours,
                        setup_time=setup_time_hours,
                        total_cost=total_cost,
                        costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                    )
                    operations.append(operation)
        return operations

    @classmethod
    def get_is_outside_service(cls, work_center: Workcenter):
        work_center_type: Workcentertype = work_center.workcentertypefk
        return (work_center_type and work_center_type.description == "Outside Processing") or False

    @classmethod
    def get_shop_operation_costing_variables(cls, costing_vars: dict) -> List[CostingVariable]:
        pp_costing_vars = []
        for pp_var_name, (value, value_type) in costing_vars.items():
            if value is not None:
                pp_costing_vars.append(
                    CostingVariable(
                        label=pp_var_name,
                        value=value_type(value)
                    )
                )
        return pp_costing_vars

    @classmethod
    def _get_material_price(cls, quote_assembly: Quoteassembly, price: Decimal, total_quantity: int) -> Decimal:
        """
        These formulas are directly from https://learnhub.mie-solutions.com/Content/Maintenance/maint_item_mat_setup_Key_Fields_for_mat_Setup.htm
        (this webpage was taken down - we still have this though: https://www.mie-solutions.com/blog/2011/03/29/estimating-material-in-cost-estimates-weight-calculation)
        """
        calculation_type: Calculationtype = quote_assembly.calculationtypefk
        calculation_description = calculation_type.description or ""
        vendor_unit = quote_assembly.vendorunit or 0
        stock_pieces = quote_assembly.stockpieces or 1
        stock_width = quote_assembly.stockwidth or 1
        stock_length = quote_assembly.stocklength or 1
        blank_width = quote_assembly.blankwidth or 0
        blank_length = quote_assembly.blanklength or 0
        parts_per_blank = quote_assembly.partsperblank or 1
        parts_required = quote_assembly.partsrequired or 1
        piece_weight = quote_assembly.pieceweight or 0
        stock_required = 1
        real_parts_required = max(quote_assembly.quantityrequired or 1, parts_required) or 1
        blanks_per_stock = math.ceil(stock_pieces / parts_per_blank) or 1
        blanks_required = math.ceil(total_quantity / parts_per_blank)
        stock_sheets_required = Decimal(blanks_required / blanks_per_stock)
        percentage_of_sheet_is_not_scrap_based_on_blanks = ((blank_width * blank_length) / (stock_width * stock_length))
        if "Single Part Price" in calculation_description:
            return price
        elif "Calculate Include Scrap" in calculation_description:
            return price * Decimal(vendor_unit / stock_pieces)
        elif "Calculate Without Scrap" in calculation_description:
            return price * Decimal(
                Decimal(vendor_unit / (stock_width * stock_length)) * (blank_width * blank_length) / parts_per_blank
            )
        elif "Amortize" in calculation_description:
            return Decimal((vendor_unit * stock_required * price) / total_quantity) / real_parts_required
        elif "Lot Price" in calculation_description:
            return Decimal(Decimal(price / total_quantity) / real_parts_required)
        elif "Calculate Blanks Include Scrap" in calculation_description:
            return Decimal((vendor_unit * stock_sheets_required * price) / Decimal(total_quantity / parts_required))
        elif "Calculate Blanks Without Scrap" in calculation_description:
            return Decimal(
                (vendor_unit * blanks_required * price * percentage_of_sheet_is_not_scrap_based_on_blanks
                 ) / total_quantity)
        elif "Piece Weight" in calculation_description:
            return price * piece_weight
        # below are estimates
        elif "Calculate" in calculation_description:
            return price
        return price

    @classmethod
    def _get_estimated_material_cost(cls, quote_assembly: Quoteassembly, total_quantity: int) -> float:
        # first, we need to get the correct price based on the quantity breaks
        price = quote_assembly.price1 or 0
        parts_required = max(quote_assembly.quantityrequired or 1, quote_assembly.partsrequired or 1)
        total_parts_required = total_quantity * parts_required
        for i in range(1, 13):
            quantity_field_name = f"quantity{i}"
            price_field_name = f"price{i}"
            quantity = safe_get(quote_assembly, quantity_field_name)
            if quantity is not None and quantity <= total_parts_required:
                price = safe_get(quote_assembly, price_field_name) or 0

        # now get the total cost
        material_cost = Decimal(cls._get_material_price(quote_assembly, price, total_quantity))
        total_cost = material_cost * total_parts_required
        total_cost += (quote_assembly.setupcharge or 0)
        minimum_charge = quote_assembly.minimumcharge or 0
        return float(max(total_cost, minimum_charge))

    @classmethod
    def get_estimated_required_materials(cls, quote_assemblies, total_quantity: int) -> List[RequiredMaterials]:
        materials = []
        for quote_assembly in quote_assemblies:
            quote_assembly: Quoteassembly
            item: Item = quote_assembly.itemfk
            if item:
                costing_var_dict = get_estimated_material_costing_variables(quote_assembly, item)
                total_cost = cls._get_estimated_material_cost(quote_assembly, total_quantity)
                material = RequiredMaterials(
                    name=item.partnumber,
                    notes=quote_assembly.comment,
                    total_cost=total_cost,
                    costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(material)
        return materials

    def get_estimated_children(self, quote_assemblies) -> List[Child]:
        children = []
        for quote_assembly in quote_assemblies:
            quote_assembly: Quoteassembly
            child_quote: Quote = quote_assembly.itemquotefk
            if child_quote:
                item: Item = child_quote.itemfk
                self.process_child_repeat_part(item.pk)
                child = Child(
                    part_number=item.partnumber,
                    revision=item.revision,
                    qty_per_parent=quote_assembly.quantityrequired,
                )
                children.append(child)
        return children

    @classmethod
    def get_roots_with_quantities(cls, quote: Quote, running_quantity=1, quantity_data=None, linking_assembly=None) \
            -> List[MoMQuantityData]:
        quote_assemblies = Quoteassembly.objects.filter(itemquotefk=quote).select_related('quotefk__customerfk')
        roots = []

        if quote_assemblies.exists():
            # quote is a child
            for quote_assembly in quote_assemblies:
                parent_quote: Quote = quote_assembly.quotefk
                quantity_required = quote_assembly.quantityrequired
                real_quantity_data = quantity_data
                if real_quantity_data is None:
                    real_quantity_data = Quotequantity.objects.filter(quotefk=quote, quantity=quantity_required).first()
                real_linking_assembly = linking_assembly
                if real_linking_assembly is None:
                    real_linking_assembly = quote_assembly
                roots += cls.get_roots_with_quantities(parent_quote, running_quantity * int(quantity_required),
                                                       real_quantity_data, real_linking_assembly)
        else:
            # quote is a root
            for quantity in Quotequantity.objects.filter(quotefk=quote):
                quantity: Quotequantity
                roots.append(
                    MoMQuantityData(
                        root=quote,
                        total_quantity=running_quantity * int(quantity.quantity),
                        quantity_data=quantity_data or quantity,
                        linking_assembly=linking_assembly
                    )
                )

        return roots

    def get_engineered_methods_of_manufacture(self, item: Item) -> List[MOMWrapper]:
        methods_of_manufacture = []
        work_order_releases = Workorderrelease.objects.filter(itemfk=item)\
            .select_related('workorderfk__workordertotalfk', 'parentrouterfk', 'workorderfk__customerfk')
        for work_order_release in work_order_releases:
            work_order_release: Workorderrelease
            quantity = work_order_release.quantityrequired or 1
            work_order: Workorder = work_order_release.workorderfk
            cost_data = self.get_engineered_cost_data(work_order_release)
            mom = MethodOfManufacture(
                requested_qty=quantity,
                make_qty=quantity,
                unit_price=cost_data.unit_price,
                total_price=cost_data.total_price,
                operations=self.get_engineered_operations(work_order_release),
                required_materials=self.get_engineered_required_materials(work_order_release),
                children=self._get_children_of_work_order_release(work_order_release)
            )
            mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="engineered", root=work_order)
            methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    @classmethod
    def get_engineered_cost_data(cls, work_order_release: Workorderrelease) -> MoMCostData:
        cost_data = MoMCostData()
        work_order: Workorder = work_order_release.workorderfk
        is_root = not work_order_release.parentrouterfk
        if is_root and work_order.quantityrequired:
            workorder_totals: Workordertotal = work_order.workordertotalfk
            cost_data.unit_price = workorder_totals.salesrevenuesestimated or 0
            cost_data.total_price = (workorder_totals.salesrevenuesestimated or 0) * work_order.quantityrequired
        return cost_data

    @classmethod
    def get_engineered_operations(cls, work_order_release: Workorderrelease) -> List[Operation]:
        def get_operation_data(work_order_assembly: Workorderassembly) -> OperationData:
            operation_data = OperationData()
            operation_data.setup_hours = work_order_assembly.setuptime / 60
            quantity_required = work_order_assembly.quantityrequired or 1
            operation_data.run_hours = (work_order_assembly.minutesperpart / 60) * quantity_required
            total_hours = operation_data.setup_hours + operation_data.run_hours
            work_center: Workcenter = work_order_assembly.workcenterfk
            hourly_rate = (work_center.averageemployeeoverheadrate or 0) + \
                          (work_center.hourlyoverhead or 0) + \
                          (work_center.averageemployeerate or 0)
            operation_data.cost = total_hours * hourly_rate
            return operation_data

        return cls._get_operations_from_work_order_release(work_order_release, get_operation_data)

    @classmethod
    def get_engineered_required_materials(cls, work_order_release: Workorderrelease) -> List[RequiredMaterials]:
        def get_cost(work_order_assembly: Workorderassembly):
            return (work_order_assembly.price or 0) * (work_order_assembly.totalquantityrequired or 1)
        return cls._get_required_materials_from_work_order_release(work_order_release, get_cost)

    def get_executed_methods_of_manufacture(self, item: Item) -> List[MOMWrapper]:
        methods_of_manufacture = []
        work_order_releases = Workorderrelease.objects.filter(itemfk=item)\
            .select_related('workorderfk__workordertotalfk', 'parentrouterfk', 'workorderfk__customerfk')
        for work_order_release in work_order_releases:
            work_order_release: Workorderrelease
            work_order: Workorder = work_order_release.workorderfk
            completed = Workordercompletion.objects.filter(workorderfk=work_order).exists()
            if completed:
                quantity = work_order_release.quantityrequired or 1
                cost_data = self.get_executed_cost_data(work_order_release)
                mom = MethodOfManufacture(
                    requested_qty=quantity,
                    make_qty=quantity,
                    unit_price=cost_data.unit_price,
                    total_price=cost_data.total_price,
                    operations=self.get_executed_operations(work_order_release),
                    required_materials=self.get_executed_required_materials(work_order_release),
                    children=self._get_children_of_work_order_release(work_order_release)
                )
                mom_wrapper = MOMWrapper(method_of_manufacture=mom, header_type="executed", root=work_order)
                methods_of_manufacture.append(mom_wrapper)
        return methods_of_manufacture

    @classmethod
    def get_executed_cost_data(cls, work_order_release: Workorderrelease) -> MoMCostData:
        cost_data = MoMCostData()
        work_order: Workorder = work_order_release.workorderfk
        is_root = not work_order_release.parentrouterfk
        if is_root and work_order.quantityrequired:
            workorder_totals: Workordertotal = work_order.workordertotalfk
            cost_data.unit_price = workorder_totals.salesrevenues or 0
            cost_data.total_price = (workorder_totals.salesrevenues or 0) * work_order.quantityrequired
        return cost_data

    @classmethod
    def get_executed_operations(cls, work_order_release: Workorderrelease) -> List[Operation]:
        def get_operation_data(work_order_assembly: Workorderassembly) -> OperationData:
            operation_data = OperationData()
            work_order_collections = Workordercollection.objects.filter(workorderassemblynumber=work_order_assembly.pk)\
                .select_related('workordertypeofhourfk')
            for work_order_collection in work_order_collections:
                work_order_collection: Workordercollection
                employee_rate = work_order_collection.employeeovertimerate if work_order_collection.isovertime \
                    else work_order_collection.employeewagerate
                hourly_rate = (work_order_collection.employeeoverheadrate or 0) + \
                              (work_order_collection.workcenteroverheadrate or 0) + \
                              (employee_rate or 0)
                total_hours = work_order_collection.totalhours or 0
                operation_data.cost += total_hours * hourly_rate
                hour_type: Workordertypeofhour = work_order_collection.workordertypeofhourfk
                if "setup" in (hour_type.description or "").lower():
                    operation_data.setup_hours += total_hours
                else:
                    operation_data.run_hours += total_hours
            return operation_data

        return cls._get_operations_from_work_order_release(work_order_release, get_operation_data)

    @classmethod
    def get_executed_required_materials(cls, work_order_release: Workorderrelease) -> List[RequiredMaterials]:
        def get_cost(work_order_assembly: Workorderassembly):
            cost = 0
            work_order_issuings = Workorderissuing.objects.filter(workorderassemblynumber=work_order_assembly.pk)
            for work_order_issuing in work_order_issuings:
                work_order_issuing: Workorderissuing
                cost += (work_order_issuing.extendedamount or 0)
            return cost
        return cls._get_required_materials_from_work_order_release(work_order_release, get_cost)

    @classmethod
    def _get_operations_from_work_order_release(cls, work_order_release: Workorderrelease,
                                                get_operation_data: Callable) -> List[Operation]:
        operations = []
        work_order_assemblies = Workorderassembly.objects.filter(workorderreleasefk=work_order_release)\
            .select_related('workcenterfk__workcentertypefk')
        for work_order_assembly in work_order_assemblies:
            work_order_assembly: Workorderassembly
            work_center: Workcenter = work_order_assembly.workcenterfk
            if work_center:
                operation_data: OperationData = get_operation_data(work_order_assembly)
                costing_var_dict = get_engineered_operation_costing_variables(
                    work_order_assembly, work_center)
                operation = Operation(
                    is_finish=False,
                    is_outside_service=cls.get_is_outside_service(work_center),
                    name=work_center.description,
                    notes=work_order_assembly.comment,
                    position=work_order_assembly.sequencenumber,
                    runtime=operation_data.run_hours,
                    setup_time=operation_data.setup_hours,
                    total_cost=operation_data.cost,
                    costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                )
                operations.append(operation)
        return operations

    @classmethod
    def _get_required_materials_from_work_order_release(cls, work_order_release: Workorderrelease, get_cost: Callable) \
            -> List[RequiredMaterials]:
        materials = []
        work_order_assemblies = Workorderassembly.objects.filter(workorderreleasefk=work_order_release)\
            .select_related('itemfk__partyfk', 'unitofmeasuresetfk')
        for work_order_assembly in work_order_assemblies:
            work_order_assembly: Workorderassembly
            item: Item = work_order_assembly.itemfk
            if item:
                costing_var_dict = get_engineered_material_costing_variables(work_order_assembly, item)
                cost = get_cost(work_order_assembly) or 0
                operation = RequiredMaterials(
                    name=item.partnumber,
                    notes=work_order_assembly.comment,
                    total_cost=cost,
                    costing_variables=cls.get_shop_operation_costing_variables(costing_var_dict)
                )
                materials.append(operation)
        return materials

    def _get_children_of_work_order_release(self, work_order_release: Workorderrelease) -> List[Child]:
        children = []
        root: Workorder = work_order_release.workorderfk
        parent_quantity = work_order_release.quantityrequired or 1
        work_order_assemblies = Workorderassembly.objects.filter(workorderreleasefk=work_order_release)\
            .select_related('itemrouterfk__itemfk')
        for work_order_assembly in work_order_assemblies:
            work_order_assembly: Workorderassembly
            child_router: Router = work_order_assembly.itemrouterfk
            if child_router:
                child_release: Workorderrelease = Workorderrelease.objects.filter(
                    workorderfk=root, routerfk=child_router).first()
                if child_release:
                    item: Item = child_router.itemfk
                    quantity = child_release.quantityrequired or 1
                    qty_per_parent = quantity / parent_quantity
                    self.process_child_repeat_part(item.pk)
                    child = Child(
                        part_number=item.partnumber,
                        revision=item.revision,
                        qty_per_parent=qty_per_parent
                    )
                    children.append(child)
        return children

    def process_child_repeat_part(self, item_id):
        self.repeat_part.type = "assembled"
        if self.create_child_parts:
            logger.info(f"Creating child parts for {item_id}")
            self._importer._process_repeat_part(item_id, create_child_parts=True)
