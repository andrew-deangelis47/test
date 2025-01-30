from typing import Optional

from baseintegration.datamigration import logger
from globalshop.document_control import DocumentControl
from paperless.objects.orders import OrderItem, OrderComponent, Order
from globalshop.exporter.processors import GSProcessor


class DocumentControlProcessor(GSProcessor):

    def _process(self, item: OrderItem, order: Order):  # TODO: If part already exists, do not overwrite the filepath
        if not self._exporter.erp_config.run_document_control_exporter:
            return

        """
        We are going to write out the part level information every time,
        as the settings for when to update/insert a record is controlled
        inside Global Shop
        """
        root = item.root_component

        for assm_component in item.iterate_assembly():
            self._insert_component_document_control(root, assm_component.component, item, order)

    def _insert_component_document_control(self, root: OrderComponent, component: OrderComponent, line_item: OrderItem,
                                           order: Order = None):
        if component.part_number is not None:
            partnumber = component.part_number
        else:
            partnumber = component.part_name
        external_id = self._get_external_id(root, component, line_item, order)
        if external_id is None:
            logger.error(f'Skipping document control for component due to missing external_id: {partnumber}')
            return
        file_path = self._get_file_path(root, component, line_item, order)
        if file_path is None:
            logger.error(f'Skipping document control for component due to missing file_path: {partnumber}')
            return
        revision = component.revision
        location = None
        group_name = self._get_group(root, component, line_item, order)
        description = None

        DocumentControl.insert_with_type_inventory_master(external_id=external_id,
                                                          file_path=file_path,
                                                          partnumber=partnumber,
                                                          revision=revision,
                                                          location=location,
                                                          group_name=group_name,
                                                          description=description)
        logger.debug(f'Document control: {file_path}')

    def _get_external_id(self, root: OrderComponent, component: OrderComponent, line_item: OrderItem,
                         order: Order = None) -> Optional[str]:
        if component.part_number is not None:
            return component.part_number
        else:
            return component.part_name

    @staticmethod
    def _get_file_path(root: OrderComponent, component: OrderComponent, line_item: OrderItem,
                       order: Order = None) -> Optional[str]:
        part_viewer_url = f'https://app.paperlessparts.com/parts/viewer/{component.part_uuid}'
        return part_viewer_url

    def _get_group(self, root: OrderComponent, component: OrderComponent, line_item: OrderItem,
                   order: Order = None) -> Optional[str]:
        # Override for customer until we have some default behavior
        return "DRAWINGS"
