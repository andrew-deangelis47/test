import e2.models as e2
from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger


class AssemblyProcessor(E2Processor):
    do_rollback = False

    def _process(self, parent_part, part, child_quantity, is_parent_part_new: bool, is_purchased: bool):
        parent_part_number = parent_part.partno
        child_part = part
        child_part_number = child_part.partno
        should_create_or_update_bom = self.should_create_or_update_bom(is_parent_part_new)

        assembly_link = e2.Materials.objects.filter(partno=parent_part_number, subpartno=child_part_number).first()

        # If no Materials record exists for this parent_part_number / child_part_number pair, create one
        if should_create_or_update_bom:
            # Note - it's possible for assembly_link to be None in the case where the parent part is not new and
            # the existing part did not have a link to the child, and the config option to modify anyway is set to False
            assembly_link = self.create_assembly_link(child_part, child_part_number, child_quantity, parent_part_number, is_purchased)
        return assembly_link

    def create_assembly_link(self, child_part, child_part_number, child_quantity, parent_part_number, is_purchased):
        logger.info(f'Creating new  Materials record for parent part number {parent_part_number} with child part number {child_part_number}.')
        # Figure out what item number to assign this Materials record by looking at the the maximum existing item
        # number for this part_part_number
        max_item_number = 0
        existing_assembly_links_for_parent = e2.Materials.objects.filter(partno=parent_part_number)
        for existing_assembly_link in existing_assembly_links_for_parent:
            if existing_assembly_link.itemno > max_item_number:
                max_item_number = existing_assembly_link.itemno

        item_number = max_item_number + 1

        vendor = child_part.vendcode1
        unit = child_part.stockunit
        description = child_part.descrip

        assembly_link = e2.Materials.objects.create(
            partno=parent_part_number,
            subpartno=child_part_number,
            descrip=description,
            qty=child_quantity,
            unit=unit,
            purchased=int(is_purchased),
            vendor=vendor,
            totalqty=child_quantity,
            unitcost=0,
            unitprice=0,
            totalcost=0,
            totalprice=0,
            totalwt=0,
            stepno=0,
            partwt=None,
            itemno=item_number
        )
        return assembly_link

    def should_create_or_update_bom(self, is_part_new: bool):
        should_create_or_update_bom = False
        if is_part_new:
            should_create_or_update_bom = True
        else:
            if self._exporter.erp_config.should_replace_e2_bom_for_existing_parts:
                should_create_or_update_bom = True
        return should_create_or_update_bom

    def clear_existing_materials_records(self, parent_part_number):
        materials_queryset = e2.Materials.objects.filter(partno=parent_part_number)
        logger.info(f'Deleting {len(materials_queryset)} existing Materials records for parent part number {parent_part_number}')
        materials_queryset.delete()
