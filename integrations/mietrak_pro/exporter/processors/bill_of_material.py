from typing import Union, Optional, List
from mietrak_pro.exporter.utils import RawMaterialPartData
from mietrak_pro.query.router import create_bom_item_link, create_subrouter_bom_link
from mietrak_pro.models import Router, Item, Routerworkcenter
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger
from paperless.objects.orders import OrderComponent, OrderOperation
from paperless.objects.quotes import QuoteComponent, QuoteOperation


class BOMProcessor(MietrakProProcessor):
    do_rollback = False
    component = None

    def __init__(self, exporter):
        super().__init__(exporter)
        self.blank_width = None
        self.blank_length = None

    def _process(self, router: Router, part_or_raw_material_parts: Union[Item, List[RawMaterialPartData], None],
                 subrouter: Router, bom_quantity: float,
                 component: Optional[Union[OrderComponent, QuoteComponent]]):
        # Check if this is a BOM Item or a subrouter
        self.component = component
        if part_or_raw_material_parts is None:
            self.create_bom_item_link_from_singular_part(part_or_raw_material_parts, router, component, bom_quantity,
                                                         subrouter)

        elif isinstance(part_or_raw_material_parts, list):
            for index_position, raw_material_part in enumerate(part_or_raw_material_parts):
                part: Item = raw_material_part.raw_material_part
                if part is not None:
                    self.create_bom_item_link_from_singular_part(part, router, component, bom_quantity, subrouter,
                                                                 index_position)
        else:
            part: Item = part_or_raw_material_parts
            if part is not None:
                self.create_bom_item_link_from_singular_part(part, router, component, bom_quantity, subrouter)

    def create_bom_item_link_from_singular_part(self, part, router, component, bom_quantity, subrouter,
                                                index_position=None):
        if part is not None:
            logger.info(f'Creating BOM Item link for parent {router.partnumber} and child {part.partnumber}')
            sequence_number = self.get_bom_item_sequence_number(part, component, router)
            blank_width, blank_length = self.get_raw_material_blank_size(component, index_position) or (None, None)
            self.blank_width = blank_width
            self.blank_length = blank_length
            bom_link = self.create_bom_item_link(router, part, bom_quantity, sequence_number)
            self.blank_width = None
            self.blank_length = None
        elif subrouter is not None:
            logger.info(f'Creating Subrouter BOM link for parent {router.partnumber} and child {subrouter.partnumber}')
            sequence_number = self.get_subrouter_bom_sequence_number(subrouter, component, router)
            bom_link = self.create_subrouter_bom_link(router, subrouter, bom_quantity, sequence_number)
        else:
            bom_link = None

        return bom_link

    def create_bom_item_link(self, router: Router, part: Item, bom_quantity: float, sequence_number: int):
        parts_per_blank = part_length = part_width = stock_length = stock_width = mat_notes = stock_thickness = density \
            = overagepercentage = leadtime = daysout = supplier_name = setup_charge = minimum = None
        useexactmaterialcalculation = 1
        quantityperinverse = 1.
        material_ops = self.component.material_operations if self.component else []
        part_number = self._exporter.erp_config.raw_material_part_number_variable_name
        os_part_number = self._exporter.erp_config.pp_outside_process_var
        shop_operations = self.component.shop_operations if self.component else []
        logger.info(f'Blank sizes -> {self.blank_length}, {self.blank_width}')
        # TODO: get all the hardcoded P3L vars below into config variables
        for mat_op in material_ops:
            if mat_op.get_variable(part_number) == part.partnumber:
                op = mat_op
                parts_per_blank = op.get_variable(self._exporter.erp_config.parts_per_blank_variable_name)
                part_length = op.get_variable(self._exporter.erp_config.part_length_variable_name)
                part_width = op.get_variable(self._exporter.erp_config.part_width_variable_name)
                stock_length = part.stocklength
                stock_width = part.stockwidth
                mat_notes = op.notes
                bom_quantity = op.get_variable(self._exporter.erp_config.raw_material_quantity_variable_name)
                bom_quantity = self._exporter.get_value_relative_to_current_node(bom_quantity) or 1.
                stock_thickness = op.get_variable(self._exporter.erp_config.stock_thickness_variable_name)
                density = op.get_variable(self._exporter.erp_config.density_variable_name)
                overagepercentage = op.get_variable(self._exporter.erp_config.overage_percentage_variable_name)
                use_exact_material = op.get_variable(self._exporter.erp_config.use_exact_material_calc_variable_name)
                useexactmaterialcalculation = 1 if use_exact_material and 'Net' in use_exact_material else 0
        for shop_op in shop_operations:
            if shop_op.get_variable(os_part_number) == part.partnumber:
                logger.info('----------------- OS -------------------------')
                supplier_name = shop_op.get_variable(self._exporter.erp_config.vendor_variable_name)
                daysout = shop_op.get_variable(self._exporter.erp_config.leadtime_variable_name)
                setup_charge = shop_op.get_variable(self._exporter.erp_config.setup_charge_variable_name)
                overagepercentage = shop_op.get_variable(self._exporter.erp_config.overage_percentage_variable_name)
                minimum = shop_op.get_variable(self._exporter.erp_config.osv_minimum_variable_name)
                mat_notes = shop_op.notes
            if 'PC Piece Price' in shop_op.name:
                leadtime = shop_op.get_variable(self._exporter.erp_config.leadtime_variable_name)
                supplier_name = shop_op.get_variable(self._exporter.erp_config.vendor_variable_name)
                overagepercentage = shop_op.get_variable(self._exporter.erp_config.overage_percentage_variable_name)
                quantityperinverse = shop_op.get_variable(self._exporter.erp_config.quantity_per_inverse_variable_name)
                mat_notes = shop_op.notes
        return create_bom_item_link(router, part, sequence_number, bom_quantity, self.blank_width, self.blank_length,
                                    parts_per_blank, part_length, part_width, stock_length, stock_width, mat_notes,
                                    stock_thickness, density, overagepercentage, leadtime, daysout, supplier_name,
                                    setup_charge, quantityperinverse, useexactmaterialcalculation, minimum)

    def get_bom_item_sequence_number(self, part: Item, component: Optional[Union[OrderComponent, QuoteComponent]],
                                     parent_router: Router):
        if part.itemtypefk.description == 'Hardware/Supplies':
            return self.get_purchased_component_bom_item_sequence_number(part, component, parent_router)
        elif part.itemtypefk.description == 'Material':
            return self.get_raw_material_bom_item_sequence_number(part, component, parent_router)
        else:
            return 1

    def get_purchased_component_bom_item_sequence_number(self, part: Item,
                                                         component: Optional[Union[OrderComponent, QuoteComponent]],
                                                         parent_router: Router):
        parent_router_ops = Routerworkcenter.objects.filter(routerfk=parent_router.routerpk)
        if not self._exporter.erp_config.should_associate_purchased_components_with_assembly_operation:
            return 1
        for operation in parent_router_ops:
            work_center_instance = operation.workcenterfk
            if work_center_instance is not None:
                if work_center_instance.description == self._exporter.erp_config.default_assembly_operation_name:
                    return operation.sequencenumber
        return 1

    def get_raw_material_bom_item_sequence_number(self, part: Item,
                                                  component: Optional[Union[OrderComponent, QuoteComponent]],
                                                  parent_router: Router):
        """ The operation that the raw material is associated with will likely depend on the process (e.g. bandsaw for
            milling or shear for sheet metal). As such, it is difficult to come up with config options that describe
            the typical use case. Override this function as necessary on a case-by-case basis. """
        return 1

    def create_subrouter_bom_link(self, router: Router, subrouter: Router, bom_quantity: float, sequence_number: int):
        create_subrouter_bom_link(router, subrouter, sequence_number, bom_quantity)

    def get_subrouter_bom_sequence_number(self, subrouter: Router,
                                          component: Optional[Union[OrderComponent, QuoteComponent]],
                                          parent_router: Router):
        parent_router_ops = Routerworkcenter.objects.filter(routerfk=parent_router.routerpk)
        if not self._exporter.erp_config.should_associate_subrouters_with_assembly_operation:
            return 1
        for operation in parent_router_ops:
            work_center_instance = operation.workcenterfk
            if work_center_instance is not None:
                if work_center_instance.description == self._exporter.erp_config.default_assembly_operation_name:
                    return operation.sequencenumber
        return 1

    def get_order_raw_material_blank_size(self, material_op: OrderOperation):
        raw_material_blank_width = material_op.get_variable(
            self._exporter.erp_config.raw_material_blank_width_variable_name
        )
        raw_material_blank_length = material_op.get_variable(
            self._exporter.erp_config.raw_material_blank_length_variable_name
        )
        return raw_material_blank_width, raw_material_blank_length

    def get_quote_raw_material_blank_size(self, component: QuoteComponent, material_op: QuoteOperation):
        # Assume that the blank size costing variables are not quantity-specific and that any quantity
        # will do
        if not component.quantities:
            return None

        raw_material_blank_width = material_op.get_variable(self._exporter.erp_config.raw_material_blank_width_variable_name)
        raw_material_blank_length = material_op.get_variable(self._exporter.erp_config.raw_material_blank_length_variable_name)

        # Handle older P3L that may be quantity specific still
        if not raw_material_blank_length and not raw_material_blank_width:
            default_quantity = component.quantities[0].quantity
            raw_material_blank_width = material_op.get_variable_for_qty(
                self._exporter.erp_config.raw_material_blank_width_variable_name, default_quantity
            )
            raw_material_blank_length = material_op.get_variable_for_qty(
                self._exporter.erp_config.raw_material_blank_length_variable_name, default_quantity
            )
        return raw_material_blank_width, raw_material_blank_length

    def get_raw_material_blank_size(self, component: Optional[Union[OrderComponent, QuoteComponent]], index_position):
        if component and component.material_operations:
            # Get the corresponding material operation using the index position:
            try:
                material_op = component.material_operations[index_position]
            except Exception as e:
                logger.info(f"Due to assembly conversions, we cannot pull the blank size from this operation. {e}")
                return 0, 0

            raw_material_blank_width_variable_name = self._exporter.erp_config.raw_material_blank_width_variable_name
            raw_material_blank_length_variable_name = self._exporter.erp_config.raw_material_blank_length_variable_name
            if raw_material_blank_width_variable_name and raw_material_blank_length_variable_name:
                if isinstance(component, OrderComponent):
                    material_op: OrderOperation
                    return self.get_order_raw_material_blank_size(material_op)
                elif isinstance(component, QuoteComponent):
                    material_op: QuoteOperation
                    return self.get_quote_raw_material_blank_size(component, material_op)
