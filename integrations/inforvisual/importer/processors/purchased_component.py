from typing import Optional, List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get
from inforvisual.models import Part, PartSite, PurchaseOrder, PurcOrderLine
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent


class PurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]) -> bool:  # noqa: C901
        if self._importer.listener.erp_config.import_from_purchase_orders:
            return self.process_from_purchase_order(purchased_component_ids)
        else:
            return self.process_from_part(purchased_component_ids)

    def process_from_part(self, purchased_component_ids: [str]):
        """
        This takes a part ID and uploads the corresponding part as a purchased component. Standard behavior.
        """
        purchased_component_list = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing purchased component from part {purchased_component_id}")
            part_row: Part = Part.objects.filter(id=purchased_component_id).first()
            part_site_row: PartSite = PartSite.objects.filter(part_id=purchased_component_id).first()
            if part_row and part_site_row:
                purchased_component = self.instantiate_purchased_component(
                    purchased_component_id=purchased_component_id,
                    piece_price=part_site_row.unit_material_cost,
                    internal_part_number=purchased_component_id,
                    description=part_row.description[:100] if part_row.description else 'N/A',
                    part_row=part_row
                )
                purchased_component_list.append(purchased_component)
            else:
                logger.info(f"Object w ID {purchased_component_id} could not be found in Infor Visual. Skipping")
                continue
        result = PurchasedComponent.upsert_many(purchased_component_list)
        if result.failures:
            logger.error(result.failures)
        return len(result.failures) == 0

    def process_from_purchase_order(self, purchase_order_ids: [str]):
        """
        This takes a purchase order ID and uploads the parts that were purchased in that order as purchased components.
        This is useful for cases when the customer does not store their purchased components in the Part table.
        """
        purchased_component_list = []
        for purchase_order_id in purchase_order_ids:
            logger.info(f"Processing purchased components from purchase order {purchase_order_id}")
            purchase_order: PurchaseOrder = PurchaseOrder.objects.filter(id=purchase_order_id).first()
            if purchase_order:
                purchase_order_lines = PurcOrderLine.objects.filter(purc_order=purchase_order)
                for purchase_order_line in purchase_order_lines:
                    purchase_order_line: PurcOrderLine
                    purchased_component_id = purchase_order_line.vendor_part_id
                    if not purchased_component_id:
                        logger.info(f"Purchase order line {purchase_order_line.line_no} does not have a vendor part ID. Skipping")
                        continue
                    logger.info(f"Processing line {purchase_order_line.line_no} with purchased component ID {purchased_component_id}")

                    part = purchase_order_line.part

                    purchased_component = self.instantiate_purchased_component(
                        purchased_component_id=purchased_component_id,
                        piece_price=purchase_order_line.unit_price,
                        internal_part_number=safe_get(part, 'id'),
                        description=safe_get(part, 'description')
                    )
                    purchased_component_list.append(purchased_component)

            else:
                logger.info(f"Purchase order w ID {purchase_order_id} could not be found in Infor Visual. Skipping")
                continue

        result = PurchasedComponent.upsert_many(purchased_component_list)
        if result.failures:
            logger.error(result.failures)
        return len(result.failures) == 0

    def instantiate_purchased_component(self, purchased_component_id, piece_price, internal_part_number,
                                        description, part_row: Optional[Part] = None):
        try:
            if piece_price < 0:
                piece_price = 0.0
        except (ZeroDivisionError, TypeError):
            piece_price = 0.0

        purchased_component = PurchasedComponent(
            piece_price=str(round(piece_price, 4))[0:10],
            oem_part_number=purchased_component_id,
            internal_part_number=internal_part_number,
            description=description)

        if part_row:
            self.set_custom_properties(part_row, purchased_component)

        return purchased_component

    def set_custom_properties(self, part_row, purchased_component):
        pass


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):
    def _process(self, purchased_component_id: str) -> bool:
        return super()._process([purchased_component_id])


class PurchasedComponentBulkPlaceholder:
    pass
