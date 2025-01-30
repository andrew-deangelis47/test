from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderComponent, OrderOperation
import time
import os
from baseintegration.datamigration import logger
import csv


class BOMProcessor(BaseProcessor):

    def _process(self, order: Order) -> list:
        logger.info(f"Processing BOM import for order {order.number}")
        self.order = order
        # assembly csv requires headers, single level does not. You have to use a diff CSV format based on whether an assembly is present
        self.assembly_csv = [["BOM Level",
                              "Part Number",
                              "Description",
                              "Revision Level",
                              "Quantity",
                              "Unit Of Measure",
                              "Material Unit Cost",
                              "Material Unit Price",
                              "Alternate Part Number",
                              "Part Weight",
                              "File",
                              "Drawing Designation",
                              "Notes",
                              "Vendor Code",
                              ]]
        self.single_level_csv = []
        self.base_level = 1
        assembly = self.get_assembly(order)
        for item in order.order_items:
            if assembly:
                self.assembly_level = 1
                self.bom_level = str(self.base_level)
                row = self.create_assembly_row(bom_level=self.base_level,
                                               part_number=item.root_component.part_number,
                                               description=item.root_component.description,
                                               revision=item.root_component.revision,
                                               quantity=item.root_component.make_quantity,
                                               unit_of_measure="EA",
                                               material_unit_cost=float(item.unit_price.dollars),
                                               material_unit_price=float(item.unit_price.dollars),
                                               alternate_part_number=item.root_component.part_name,
                                               part_weight=None,
                                               file=None,
                                               drawing_designation=None,
                                               notes=item.private_notes,
                                               vendor_code=None)
                self.assembly_csv.append(row)
                self.get_materials(item.root_component)
                self.populate_assembly(item.root_component)

            else:
                row = self.create_single_level_row(
                    part_number=item.root_component.part_number,
                    item_number=self.base_level,
                    alternate_part_number=item.root_component.part_name,
                    product_code=None,
                    vendor_code=None,
                    quantity=item.root_component.make_quantity,
                    part_weight=0,
                    part_notes=item.private_notes,
                    placeholder=1,
                    description=item.root_component.description,
                    unit_cost=float(item.unit_price.dollars)
                )
                self.single_level_csv.append(row)
            self.base_level += 1
        csv_to_write = self.assembly_csv if assembly else self.single_level_csv
        file_name = os.path.join(os.path.dirname(__file__), f"paperless_order_{str(order.number)}_{str(int(time.time()))}.csv")
        if not self._exporter._integration.test_mode:
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(csv_to_write)
            self._exporter.send_email(subject=f"New CSV available for Paperless order {str(order.number)}",
                                      body=f"New order {str(order.number)} with {str(len(order.order_items))} order items is now in Paperless."
                                           f" Please see the attached CSV for BOM import into E2 Cloud.", filepath=file_name)
            os.remove(file_name)
        return csv_to_write

    def populate_assembly(self, component: OrderComponent):
        if len(component.child_ids) == 0:
            return
        self.assembly_level += 1
        for child in component.child_ids:
            self.increment_bom_level()
            child_component = self.get_component(child)
            row = self.create_assembly_row(bom_level=self.bom_level,
                                           part_number=child_component.part_number,
                                           description=child_component.description,
                                           revision=child_component.revision,
                                           quantity=child_component.make_quantity,
                                           unit_of_measure="EA",
                                           material_unit_cost=0,
                                           material_unit_price=0,
                                           alternate_part_number=child_component.part_name,
                                           part_weight=None,
                                           file=None,
                                           drawing_designation=None,
                                           notes=None,
                                           vendor_code=None)
            self.assembly_csv.append(row)
            self.get_materials(child_component)
            self.populate_assembly(child_component)

    def get_component(self, component_id):
        for item in self.order.order_items:
            for component in item.components:
                if component.id == component_id:
                    return component
        else:
            raise ValueError("Component not found")

    def get_materials(self, root_component: OrderComponent):
        for mat_op in root_component.material_operations:
            mat_op: OrderOperation = mat_op
            mat_op_var = mat_op.get_variable(self._exporter.erp_config.pp_mat_id_variable)
            if mat_op_var is not None:
                self.increment_bom_level()
                row = self.create_assembly_row(self.bom_level,
                                               mat_op_var,
                                               mat_op.name,
                                               "N/A",
                                               mat_op.get_variable(self._exporter.erp_config.pp_mat_quantity_variable),
                                               mat_op.get_variable(self._exporter.erp_config.pp_um_variable),
                                               mat_op.get_variable(self._exporter.erp_config.pp_unit_cost_variable),
                                               mat_op.get_variable(self._exporter.erp_config.pp_unit_cost_variable),
                                               None,
                                               None,
                                               None,
                                               None,
                                               mat_op.notes,
                                               mat_op.get_variable(self._exporter.erp_config.pp_vendor_variable))
                self.assembly_csv.append(row)

    def increment_bom_level(self):
        dot_count = self.bom_level.count(".")
        if dot_count == (self.assembly_level - 2):
            self.bom_level = self.bom_level + ".1"
        elif dot_count == (self.assembly_level - 1):
            bom_level_rsplit = self.bom_level.rsplit(".", 1)
            self.bom_level = bom_level_rsplit[0] + "." + str(int(bom_level_rsplit[1]) + 1)
        elif dot_count < (self.assembly_level - 1):
            raise ValueError("Something got messed up! :(")

    def get_assembly(self, order: Order) -> bool:
        for order_item in order.order_items:
            if len(order_item.root_component.child_ids) > 0:
                return True
        return False

    def create_assembly_row(self, bom_level, part_number, description, revision, quantity, unit_of_measure,
                            material_unit_cost, material_unit_price, alternate_part_number, part_weight, file,
                            drawing_designation, notes, vendor_code) -> list:
        return [bom_level, part_number, description, revision, quantity, unit_of_measure,
                material_unit_cost, material_unit_price, alternate_part_number, part_weight, file,
                drawing_designation, notes, vendor_code]

    def create_single_level_row(self, part_number, item_number, alternate_part_number, product_code, vendor_code,
                                quantity, part_weight, part_notes, placeholder, description, unit_cost) -> list:
        return [part_number, item_number, alternate_part_number, product_code, vendor_code,
                quantity, part_weight, part_notes, placeholder, description, unit_cost]
