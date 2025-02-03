from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from e2.models import Estim
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent, PurchasedComponentColumn

# Use a module-level variable to make sure this behavior only happens the first time the processor runs (per
# instantiation of the class). This is a way of saving redundant API calls
should_create_custom_columns = True


class PurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]) -> bool:
        self.create_purchased_component_columns()
        purchased_component_list = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            estim_row = Estim.objects.filter(partno=purchased_component_id).first()

            if not estim_row:
                logger.info(f"Object w ID {purchased_component_id} could not be found in E2. Skipping")
                continue

            purchased_component = PurchasedComponent(piece_price=self.get_piece_price(estim_row),
                                                     oem_part_number=self.get_oem_part_number(estim_row),
                                                     internal_part_number=self.get_internal_part_number(estim_row),
                                                     description=self.get_description(estim_row))

            purchased_component_list.append(purchased_component)
        result = PurchasedComponent.upsert_many(purchased_component_list)
        return len(result.failures) == 0

    def create_purchased_component_columns(self):
        global should_create_custom_columns
        if not should_create_custom_columns:
            # Don't go past this point if this method has already run for this instantiation of the class
            return

        purchased_component_columns = PurchasedComponentColumn.list()
        purchased_component_column_names = [pcc.code_name for pcc in purchased_component_columns]
        if 'vendor' not in purchased_component_column_names:
            vendor_column = PurchasedComponentColumn(name='Vendor',
                                                     code_name='vendor',
                                                     value_type='string',
                                                     default_string_value=None,  # TODO - remove once the API has been updated to make this an optional field
                                                     default_boolean_value=False,  # TODO - remove once the API has been updated to make this an optional field
                                                     default_numeric_value=None)  # TODO - remove once the API has been updated to make this an optional field
            logger.info('Creating PurchasedComponentColumn with name Vendor')
            vendor_column.create()

        should_create_custom_columns = False

    def get_piece_price(self, estim_row):
        try:
            # piece_price = estim_row.price1 / estim_row.qty1 # TODO - commented line because price1 might already be a unit price and doesnt need to be divided by qty
            piece_price = estim_row.price1
            if piece_price < 0:
                piece_price = 0.0
        except (ZeroDivisionError, TypeError):
            piece_price = 0.0
        piece_price = str(round(piece_price, 4))[0:10]
        return piece_price

    def get_oem_part_number(self, estim_row):
        oem_part_number = estim_row.partno
        return oem_part_number

    def get_internal_part_number(self, estim_row):
        # The Open API does not currently allow blank values for this field, but it does allow None
        internal_part_number = estim_row.altpartno if estim_row.altpartno else None
        return internal_part_number

    def get_description(self, estim_row):
        # The Open API does not currently allow blank values for this field, but it does allow None
        description = estim_row.descrip if estim_row.descrip else None
        if description is not None:
            description = description[:100]  # The API allows a max length of 100 for this field
        return description

    def get_vendor(self, estim_row):
        vendor = estim_row.vendcode1
        return vendor

    def set_custom_properties(self, estim_row, purchased_component):
        vendor = self.get_vendor(estim_row)
        purchased_component.set_property('vendor', vendor)


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):
    def _process(self, purchased_component_id: str) -> bool:
        return super()._process([purchased_component_id])


class PurchasedComponentBulkPlaceholder:
    pass
