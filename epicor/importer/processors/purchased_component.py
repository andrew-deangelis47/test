from typing import List, Optional
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent, PurchasedComponentColumn
from epicor.part import PurchasedComponentPart as EpicorPurchasedComponentHelper
from epicor.utils import get_epicor_part_cost_model


class EpicorPurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, component_ids: List[str]) -> bool:
        self.get_or_create_custom_purchased_component_headers()
        purchased_component_list = []
        for component_id in component_ids:
            logger.info(f"Processing purchased component {component_id}")
            try:
                epicor_component: dict = EpicorPurchasedComponentHelper.get_part_by_part_num(component_id)
            except Exception as e:
                logger.info(e)
                logger.info(f"Purchased component {component_id} being processed from Epicor, skipping")
                continue
            else:
                if str(epicor_component.get("InActive")).lower() == "true" or str(epicor_component.get("Inactive")).lower() == "true":
                    logger.info(f"Got inactive part for {epicor_component.get('PartNum', None)}")
                    continue
                purchased_component = self._instantiate_new_paperless_component(epicor_component)
                purchased_component_list.append(purchased_component)

        result = PaperlessPurchasedComponent.upsert_many(purchased_component_list)
        if result.failures:
            logger.error(f'Error uploading purchased components - {result.failures}')
        return len(result.failures) == 0

    def _instantiate_new_paperless_component(self, epicor_part: dict) -> PaperlessPurchasedComponent:
        # Set the standard attributes
        paperless_purchased_component: PaperlessPurchasedComponent = \
            self.set_paperless_purchased_component_attributes(epicor_part)

        # Set any custom attributes
        paperless_purchased_component: PaperlessPurchasedComponent = \
            self.set_custom_paperless_purchased_component_properties(paperless_purchased_component, epicor_part)

        return paperless_purchased_component

    def set_paperless_purchased_component_attributes(self, epicor_part: dict) -> PaperlessPurchasedComponent:
        part_num = epicor_part.get("PartNum", None)

        if self._importer.erp_config.get_pc_price_from_part_cost:
            epicor_part_cost_model: dict = get_epicor_part_cost_model(part_num)
            piece_price = self.get_epicor_part_last_material_cost(epicor_part_cost_model)
        else:
            # TODO: Defaulting to .01 seems risky - should we just skip components without a price?
            piece_price = self.format_decimal_places_for_api(float(epicor_part.get("UnitPrice", 0.01)))

        paperless_purchased_component = PaperlessPurchasedComponent(
            oem_part_number=part_num,
            internal_part_number=part_num,
            piece_price=piece_price,
            description=epicor_part.get("PartDescription", "No Description")[:100]
        )
        return paperless_purchased_component

    def get_epicor_part_last_material_cost(self, epicor_part_cost_component: dict):
        padding_format = '{:.4f}'  # paperless api expects 4 max padding for decimal
        last_cost_value: float = epicor_part_cost_component["LastMaterialCost"]
        last_cost_value: str = padding_format.format(last_cost_value)
        return last_cost_value

    def get_or_create_custom_purchased_component_headers(self):
        """
        Attempts to create any missing column headers when the import processor is instantiated.
        """
        if self._importer.erp_config.custom_purchased_component_columns is None:
            self._importer.erp_config.custom_purchased_component_columns = PurchasedComponentColumn.list()

            existing_table_headers = [name.code_name for name in
                                      self._importer.erp_config.custom_purchased_component_columns]

            config_columns = self._importer.erp_config.custom_column_header_names
            config_types = self._importer.erp_config.corresponding_column_header_type
            for i, name in enumerate(config_columns):
                if name in existing_table_headers:
                    continue
                else:
                    self.create_custom_purchased_component_column(config_columns[i], config_types[i])

    def create_custom_purchased_component_column(self, column_name, column_type):
        """
        This function will create new purchased component columns based on the supplied config.yaml options:
        - custom_column_header_names: List[str] - header names
        - corresponding_column_header_type: List[str] - corresponding value types for the custom_column_header_names
        NOTE: Position matters! The first header name corresponds with the first column type based on position.
        """
        config = self._importer.erp_config
        custom_column = PurchasedComponentColumn(name=str(column_name),
                                                 code_name=str(column_name),
                                                 value_type=str(column_type),
                                                 default_string_value=str(config.default_string_value),
                                                 default_boolean_value=bool(config.default_boolean_value),
                                                 default_numeric_value=int(config.default_numeric_value))  # SDK expects int...
        try:
            custom_column.create()
            logger.info(f'Created custom Purchased Component Column {column_name}')
        except Exception as e:
            logger.info("Could not create custom Purchased Component Column")
            logger.warning(e)

    def set_custom_paperless_purchased_component_properties(self, purchased_component: PaperlessPurchasedComponent,
                                                            epicor_part: dict):
        """
        This is the only function you should have to override to customize your field values. ClassID will be included
        by default to serve as an example in the config and here.
        NOTE: Pay attention to the default types you set for each custom header.
        """
        purchased_component.set_property("class_id", str(epicor_part.get("ClassID", "None")))
        if "i_u_m" in self._importer.erp_config.custom_column_header_names:
            purchased_component.set_property("i_u_m", str(epicor_part.get("IUM", "EA")))
        if "std_material_cost" in self._importer.erp_config.custom_column_header_names:
            epicor_part_cost_model: dict = get_epicor_part_cost_model(epicor_part["PartNum"])
            purchased_component.set_property("std_material_cost", round(float(epicor_part_cost_model.get("StdMaterialCost", 0)), 4))
        return purchased_component

    def _get_paperless_component(self, component_id: str) -> Optional[PaperlessPurchasedComponent]:
        """
        Note: Paperless SDK doesn't find an exact match, it'll do a fuzzy match and return a list of possible matches.
        We do an additional filter for the exact match.
        """
        possible_components: List[PaperlessPurchasedComponent] = PaperlessPurchasedComponent.search(component_id)
        actual_component = [component for component in possible_components if component.oem_part_number == component_id]
        return actual_component[0] if actual_component else None

    def format_decimal_places_for_api(self, value: float):
        """
        The Paperless Parts SDK validates a 4-decimal, string-type, unit price on PC's, therefore returning string.
        """
        padding_format = '{:.4f}'
        formatted_value: str = padding_format.format(value)
        return formatted_value


class EpicorPurchasedComponentImportProcessor(EpicorPurchasedComponentBulkImportProcessor):
    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])


class EpicorPurchasedComponentBulkPlaceholder:
    pass
