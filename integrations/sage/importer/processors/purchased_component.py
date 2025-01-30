from typing import List, Union
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponentColumn

from sage.exceptions import SageInvalidResourceRequestedException, SageInvalidResponsePayloadException
from sage.sage_api.client import SageImportClient
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent
from sage.models.sage_models.part import PartFullEntity as SagePurchasedComponent
from sage.sage_api.filter_generation.part_filter_generator import PartFilterGenerator
from sage.models.converters.sage_purch_comp_to_paperless_purch_comp_converter import SagePurchasedCompToPaperlessPurchasedCompConverter


def _get_purchased_component(client: SageImportClient, component_id: str) -> Union[PaperlessPurchasedComponent, bool]:
    """
    - calls the sage client to get the specified purchased component
    - returns the paperless purchase component object, or False if it does not find one
    """
    try:
        sage_purchased_component = client.get_resource(
            SagePurchasedComponent,
            PartFilterGenerator.get_filter_by_id(component_id),
            False
        )
    except (SageInvalidResourceRequestedException, SageInvalidResponsePayloadException) as ex:
        logger.error(ex)
        return False

    # check that we actually got back some data
    if sage_purchased_component is None:
        logger.error('No raw material found with id ' + component_id)
        return False

    # if everything worked return the purchase component
    return SagePurchasedCompToPaperlessPurchasedCompConverter.to_paperless_purchased_comp(sage_purchased_component)


class SagePurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, component_ids: List[str]) -> bool:
        client = SageImportClient.get_instance()
        purchased_component_list = []

        for component_id in component_ids:

            # 1) get the sage purchase component from the sage api
            purchased_component = _get_purchased_component(client, component_id)
            if not purchased_component:
                logger.error('Skipping purchased component ' + component_id)
                continue

            # 2) add to list
            purchased_component_list.append(purchased_component)

        # 3) Make the call to update the purchased components in the list
        result = PaperlessPurchasedComponent.upsert_many(purchased_component_list)
        return len(result.failures) == 0

    def get_or_create_custom_purchased_component_headers(self):
        """
        Attempts to create any missing column headers when the imports processor is instantiated.
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


class SagePurchasedComponentBulkPlaceholder:
    pass


class SagePurchasedComponentImportProcessor(SagePurchasedComponentBulkImportProcessor):
    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])
