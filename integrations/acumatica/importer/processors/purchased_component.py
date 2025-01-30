from typing import List, Optional
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent, \
    PurchasedComponentColumn
from paperless.exceptions import PaperlessException
from acumatica.api_models.acumatica_models import StockItem

'''
We are filtering inventory items back by ItemClass=HARDWARE, but this only returns 4 parts
Should check with customer to determine the correct classes they use for purchased components, and update filter
'''


class AcumaticaPurchasedComponentImportProcessor(BaseImportProcessor):

    def create_custom_purchased_component_column(self, column_name, column_type):
        """
        This function will create new purchased component columns based on the supplied config.yaml options:
        - custom_column_header_names: List[str] - header names
        - corresponding_column_header_type: List[str] - corresponding value types for the custom_column_header_names
        NOTE: Position matters! The first header name corresponds with the first column type based on position.
        """
        custom_column = PurchasedComponentColumn(name=str(column_name),
                                                 code_name=str(column_name),
                                                 value_type=str(column_type),
                                                 default_string_value='',
                                                 default_boolean_value=False,
                                                 default_numeric_value=0)  # SDK expects int...
        try:
            custom_column.create()
            logger.info(f'Created custom Purchased Component Column {column_name}')
        except Exception as e:
            logger.info("Could not create custom Purchased Component Column")
            logger.warning(e)

    @staticmethod
    def _get_paperless_component(component_id: str) -> Optional[PaperlessPurchasedComponent]:
        """
        Note: Paperless SDK doesn't find an exact match, it'll do a fuzzy match and return a list of possible matches.
        We do an additional filter for the exact match.
        """
        possible_components: List[PaperlessPurchasedComponent] = PaperlessPurchasedComponent.search(component_id)
        actual_component = [component for component in possible_components if component.oem_part_number == component_id]
        return actual_component[0] if actual_component else None

    def _create_new_paperless_component(self, acumatica_part: StockItem) -> None:
        # Set the standard attributes
        paperless_purchased_component: PaperlessPurchasedComponent = \
            self.set_paperless_purchased_component_attributes(acumatica_part)

        # Set any custom attributes
        paperless_purchased_component: PaperlessPurchasedComponent = \
            self.set_custom_paperless_purchased_component_properties(paperless_purchased_component, acumatica_part)

        # Create the purchased component
        try:
            paperless_purchased_component.create()
            logger.info(f"New purchased component created: {paperless_purchased_component.oem_part_number}")
        except PaperlessException as e:
            logger.warning(e)
            logger.warning(f"Failed to create purchased component: {paperless_purchased_component.oem_part_number}")

    @staticmethod
    def set_paperless_purchased_component_attributes(acumatica_part: StockItem) -> PaperlessPurchasedComponent:
        # TODO: Defaulting to .01 seems risky - should we just skip components without a price?
        paperless_purchased_component = PaperlessPurchasedComponent(
            oem_part_number=acumatica_part.InventoryID,
            internal_part_number=acumatica_part.InventoryID,
            piece_price=str(acumatica_part.DefaultPrice),
            description=acumatica_part.Description[:100] if acumatica_part.Description else ''
        )
        return paperless_purchased_component

    @staticmethod
    def set_custom_paperless_purchased_component_properties(purchased_component: PaperlessPurchasedComponent,
                                                            acumatica_part: StockItem):
        """
        This is the only function you should have to override to customize your field values. ClassID will be included
        by default to serve as an example in the config and here.
        NOTE: Pay attention to the default types you set for each custom header.
        """
        purchased_component.set_property("last_cost", acumatica_part.LastCost)
        purchased_component.set_property("average_cost", acumatica_part.AverageCost)
        purchased_component.set_property("last_modified", acumatica_part.LastModified)
        return purchased_component

    def _update_paperless_component(self, acumatica_part: StockItem,
                                    paperless_part: PaperlessPurchasedComponent) -> None:
        paperless_part.oem_part_number = acumatica_part.InventoryID
        paperless_part.internal_part_number = acumatica_part.InventoryID
        paperless_part.piece_price = acumatica_part.DefaultPrice
        paperless_part.description = acumatica_part.Description[:100]
        paperless_part = self.set_custom_paperless_purchased_component_properties(paperless_part, acumatica_part)
        try:
            paperless_part.update()
            logger.info(f"Updated purchased component: {paperless_part.oem_part_number}")
        except PaperlessException as e:
            logger.warning(e)
            logger.warning(f"Failed to update purchased component: {paperless_part.oem_part_number}")

    def _process(self, component_id: str) -> None:
        logger.info(f"Processing purchased component {component_id}")
        filters = {"InventoryID": component_id}
        purchased_component: StockItem = StockItem.get_first(filters=filters)
        paperless_purchased_component: PaperlessPurchasedComponent = self._get_paperless_component(component_id=component_id)

        #  TODO Need to add auto creation of PC customer properties from config options.
        if paperless_purchased_component:
            self._update_paperless_component(acumatica_part=purchased_component, paperless_part=paperless_purchased_component)
        else:
            self._create_new_paperless_component(acumatica_part=purchased_component)
