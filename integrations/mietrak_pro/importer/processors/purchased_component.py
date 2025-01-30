from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get
from mietrak_pro.models import Item, Itemcatalogcategory
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent, PurchasedComponentColumn, \
    PurchasedComponentCustomProperty
from typing import List
from mietrak_pro.importer.processors.material import MaterialImportProcessor

# Use a module-level variable to make sure this behavior only happens the first time the processor runs (per
# instantiation of the class). This is a way of saving redundant API calls
should_create_custom_columns = True


class MietrakProPurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]):
        self.create_purchased_component_columns()
        return self.bulk_create_update_purchased_components(purchased_component_ids=purchased_component_ids)

    def bulk_create_update_purchased_components(self, purchased_component_ids: List[str]):
        purchased_component_list = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            item_record = Item.objects.filter(itempk=purchased_component_id).first()

            if not item_record:
                logger.info(f"Object with ID {purchased_component_id} could not be found in MIE Trak Pro. Returning")
                return

            piece_price = self.get_piece_price(item_record)
            oem_part_number = self.get_oem_part_number(item_record)
            internal_part_number = self.get_internal_part_number(item_record)
            description = self.get_description(item_record)

            if not oem_part_number:
                logger.info(f'Object with ID {purchased_component_id} has blank part number. Skipping')
                continue

            purchased_component = PurchasedComponent(piece_price=piece_price,
                                                     oem_part_number=oem_part_number,
                                                     internal_part_number=internal_part_number,
                                                     description=description
                                                     )
            purchased_component_property = PurchasedComponentCustomProperty(key='vendor',
                                                                            value=self.get_vendor(item_record))
            purchased_component.properties.append(purchased_component_property)

            if self._importer.erp_config.should_import_category:
                pc_category_property = PurchasedComponentCustomProperty(key='category',
                                                                        value=self.get_category(item_record))
                purchased_component.properties.append(pc_category_property)

            if self._importer.erp_config.should_import_leadtime:
                pc_leadtime_property = PurchasedComponentCustomProperty(key='leadtime',
                                                                        value=self.get_leadtime(item_record))
                purchased_component.properties.append(pc_leadtime_property)

            if self._importer.erp_config.should_import_po_history:
                MaterialImportProcessor.upload_po_history(purchased_component_id)

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
                                                     default_string_value=None,
                                                     # TODO - remove once the API has been updated to make this an optional field
                                                     default_boolean_value=False,
                                                     # TODO - remove once the API has been updated to make this an optional field
                                                     default_numeric_value=None)  # TODO - remove once the API has been updated to make this an optional field
            logger.info('Creating PurchasedComponentColumn with name Vendor')
            vendor_column.create()
        if self._importer.erp_config.should_import_category and 'category' not in purchased_component_column_names:
            category_column = PurchasedComponentColumn(name='Category',
                                                       code_name='category',
                                                       value_type='string',
                                                       default_string_value=None,
                                                       default_boolean_value=False,
                                                       default_numeric_value=None
                                                       )
            logger.info('Creating PurchasedComponentColumn with name Category')
            category_column.create()

        if self._importer.erp_config.should_import_leadtime and 'leadtime' not in purchased_component_column_names:
            leadtime_column = PurchasedComponentColumn(name='Leadtime',
                                                       code_name='leadtime',
                                                       value_type='numeric',
                                                       default_string_value=None,
                                                       default_boolean_value=False,
                                                       default_numeric_value=None)
            logger.info('Creating PurchasedComponentColumn with name Leadtime')
            leadtime_column.create()

        should_create_custom_columns = False

    @staticmethod
    def get_piece_price(item_record):
        try:
            piece_price = item_record.price1 if item_record.price1 else 0.
            if piece_price < 0:
                piece_price = 0.0
        except (ZeroDivisionError, TypeError):
            piece_price = 0.0
        piece_price = str(round(piece_price, 4))[0:10]
        return piece_price

    @staticmethod
    def get_category(item_record):
        category = Itemcatalogcategory.objects.filter(itemfk=item_record.itempk).first()
        return safe_get(category, 'catalogcategoryfk.name')

    @staticmethod
    def get_leadtime(item_record):
        leadtime = item_record.leadtime
        return leadtime

    @staticmethod
    def get_oem_part_number(item_record):
        oem_part_number = item_record.partnumber
        return oem_part_number

    @staticmethod
    def get_internal_part_number(item_record):
        # The Open API does not currently allow blank values for this field, but it does allow None
        internal_part_number = item_record.vendorpartnumber if item_record.vendorpartnumber else None
        return internal_part_number

    @staticmethod
    def get_description(item_record):
        # The Open API does not currently allow blank values for this field, but it does allow None
        description = item_record.description if item_record.description else None
        if description is not None:
            description = description[:100]  # The API allows a max length of 100 for this field
        return description

    @staticmethod
    def get_vendor(item_record):
        vendor = item_record.partyfk
        vendor_name = safe_get(vendor, 'name')
        return vendor_name


class MietrakProPurchasedComponentImportProcessor(MietrakProPurchasedComponentBulkImportProcessor):

    def _process(self, purchased_component_id: str):
        self.create_purchased_component_columns()
        return self.bulk_create_update_purchased_components(purchased_component_ids=[purchased_component_id])


class MietrakProPurchasedComponentPlaceholder:
    pass
