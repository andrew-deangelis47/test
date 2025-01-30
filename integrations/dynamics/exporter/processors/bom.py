from paperless.objects.quotes import QuoteComponent

from baseintegration.exporter.quote_exporter import logger

from dynamics.utils import DynamicsExportProcessor
from dynamics.exceptions import DynamicsNotFoundException, DynamicsException
from dynamics.objects.item import Item, ProductionBOM, ProductionBOMItem, ItemVariant
from dynamics.objects.customer import Customer


class BOMProcessor(DynamicsExportProcessor):

    def _process(self, component: QuoteComponent, item: Item, customer: Customer) -> (ProductionBOM, bool):
        bom: ProductionBOM
        try:
            bom = ProductionBOM.get_first({
                "No": item.No
            })
        except DynamicsNotFoundException:
            bom = ProductionBOM.create({
                "No": item.No,
                "Unit_of_Measure_Code": "PCS"
            })
            self._create_bom_lines(bom, component)

        attempt_assembly = self._process_r_part(customer, item, bom, component)

        return bom, attempt_assembly

    def _create_bom_lines(self, bom: ProductionBOM, component: QuoteComponent):
        # first add any coating items in shop operations to BOM
        for coating_item_no in self.get_op_var_values(component, 'pp_coating_item_id_var'):
            try:
                ProductionBOMItem.create({
                    "No": coating_item_no,
                    "Production_BOM_No": bom.No,
                    "Type": "Item",
                    "Quantity_per": 1
                })
            except DynamicsException:
                logger.info(f'Unable to add BOM line for coating item with ID {coating_item_no}, skipping')

        # now add materials to BOM
        for operation in component.material_operations:
            material_id = self.get_quantity_operation_variable(operation, 'pp_mat_id_variable',
                                                               component)
            quantity = self.get_quantity_operation_variable(operation, 'pp_quantity_variable',
                                                            component)
            if material_id is None:
                logger.info(f'Unable to find material ID for BOM item {operation.name}, skipping')
                continue
            try:
                ProductionBOMItem.create({
                    "No": material_id,
                    "Production_BOM_No": bom.No,
                    "Type": "Item",
                    "Quantity_per": quantity
                })
            except DynamicsException:
                logger.info(f'Unable to add BOM line for material with ID {material_id}, skipping')

    def _process_r_part(self, customer: Customer, part: Item, bom: ProductionBOM, component: QuoteComponent) -> bool:
        attempt_assembly = True
        if self.get_config_value('enable_r_parts'):
            create_r_part = 'True' in self.get_op_var_values(component, 'pp_r_part_flag')
            if create_r_part:
                # If we create an R-part for this item, do not treat it as an assembly
                logger.info(f'Creating an R-part for {part.No}')
                attempt_assembly = False
                self._create_r_part(customer, part, bom, component)
            else:
                logger.info(f'Not creating an R-part for {part.No}')
        return attempt_assembly

    def _create_r_part(self, customer: Customer, item: Item, bom: ProductionBOM, component: QuoteComponent):
        r_part_no = f'R-{item.No}'

        # create R-part as Item

        Item.get_or_create({
            'No': r_part_no,
        }, {
            'Flushing_Method': 'Backward',
            'Item_Category_Code': '999',
            'Tax_Group_Code': self.get_config_value('tax_group_code'),
            'Base_Unit_of_Measure': self.get_config_value('base_unit_of_measure'),
            'Gen_Prod_Posting_Group': self.get_config_value('gen_prod_posting_group'),
            'Inventory_Posting_Group': self.get_config_value('inventory_posting_group')
        })

        # create item variants

        surface_area_vals = self.get_op_var_values(component, 'pp_surface_area_variable')
        surface_area = surface_area_vals[0] if surface_area_vals else 0

        ItemVariant.get_or_create({
            'Item_No': r_part_no,
            'Code': customer.No
        }, {
            'TS_Unit_Weight': surface_area,
            'TS_Pricing_UOM_Code': 'Quantity'
        })

        ItemVariant.get_or_create({
            'Item_No': item.No,
            'Code': customer.No
        }, {
            'TS_Unit_Weight': surface_area,
            'TS_Pricing_UOM_Code': 'Quantity',
            'TS_Raw_Part_No': r_part_no,
            'TS_Raw_Part_Variant_Code': customer.No
        })

        # add to BOM

        ProductionBOMItem.create({
            "No": r_part_no,
            "Production_BOM_No": bom.No,
            "Type": "Item",
            "Quantity_per": 1
        })
