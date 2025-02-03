from datetime import datetime
from decimal import Decimal
from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from globalshop.part import Part, PartRecord
from paperless.objects.purchased_components import PurchasedComponent, PurchasedComponentColumn, \
    PurchasedComponentCustomProperty


class GlobalShopPurchasedComponentBulkImportProcessor(BaseImportProcessor):
    def _process(self, purchased_component_ids: List[str]):
        self.bulk_import(purchased_component_ids=purchased_component_ids)

    def bulk_import(self, purchased_component_ids: List[str]):

        # Set default GlobalShop column names for initial import
        globalshop_column_names = [
            ("product_line", "string"),
            ("description", "string"),
            ("date_last_chg", "string"),
            ("time_last_change", "string"),
            ("amt_cost", "numeric"),
        ]

        try:
            self.create_purchased_component_columns(globalshop_column_names)
        except Exception as e:
            logger.info(f"Columns already created. {e}")

        purchased_components = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            pc: PartRecord = Part.get(purchased_component_id)
            if not pc:
                logger.info(f"Part with id: {purchased_component_id} could not be found in GlobalShop, continuing to next part.")
                continue

            piece_price = self.get_piece_price(pc)
            oem_part_number = self.get_oem_part_number(pc)
            internal_part_number = self.get_internal_part_number(pc)
            description = self.get_description(pc)

            purchased_component = PurchasedComponent(piece_price=piece_price,
                                                     oem_part_number=oem_part_number,
                                                     internal_part_number=internal_part_number,
                                                     description=description)

            purchased_component.properties = self.set_custom_properties(pc)
            purchased_components.append(purchased_component)

        result = PurchasedComponent.upsert_many(purchased_components)
        return len(result.failures) == 0

    def create_purchased_component_columns(self, globalshop_column_names):
        # Check if custom columns were created when the class was instantiated. Skip this if yes, else create them.
        if not self._importer.should_create_custom_columns:
            return
        purchased_component_columns = PurchasedComponentColumn.list()
        purchased_component_column_names = [pcc.code_name for pcc in purchased_component_columns]
        for column_tuple in globalshop_column_names:
            if column_tuple not in purchased_component_column_names:
                vendor_column = PurchasedComponentColumn(name=column_tuple[0],
                                                         code_name=column_tuple[0],
                                                         value_type=column_tuple[1],
                                                         default_string_value="None",  # TODO - remove once the API has been updated to make this an optional field
                                                         default_boolean_value=False,  # TODO - remove once the API has been updated to make this an optional field
                                                         default_numeric_value=0.01)  # TODO - remove once the API has been updated to make this an optional field
                logger.info(f'Creating PurchasedComponentColumn with name {column_tuple}')
                vendor_column.create()
        self._importer.should_create_custom_columns = False

    def get_piece_price(self, pc: PartRecord) -> str:
        if not pc.amt_alt_cost:
            if not pc.amt_price:
                piece_price = 0.01
            else:
                piece_price = round(float(pc.amt_price), 2)
        else:
            piece_price = round(float(pc.amt_alt_cost), 2)
        return str(piece_price)

    def get_oem_part_number(self, pc: PartRecord) -> str:
        oem_part_number = pc.part
        return oem_part_number

    def get_internal_part_number(self, pc: PartRecord) -> str:
        # The Open API does not currently allow blank values for this field, but it does allow None
        internal_part_number = "None"
        return internal_part_number

    def get_description(self, pc: PartRecord) -> str:
        # The Open API does not currently allow blank values for this field, but it does allow None
        description = pc.description if pc.description is not None else None
        if description is not None:
            description = description[:100]  # The API allows a max length of 100 for this field
        return description

    def get_product_line(self, pc: PartRecord) -> str:
        product_line = pc.product_line if pc.product_line is not None else None
        return product_line

    def get_date_last_chg(self, pc: PartRecord) -> datetime.date:
        date_last_chg = pc.date_last_chg
        return date_last_chg

    def get_time_last_change(self, pc: PartRecord) -> datetime.time:
        time_last_change = pc.time_last_change
        return time_last_change

    def get_amt_cost(self, pc: PartRecord) -> Decimal:
        amt_cost = pc.amt_cost
        return amt_cost

    def set_custom_properties(self, pc: PartRecord) -> List[PurchasedComponentCustomProperty]:
        custom_props = []
        product_line = self.get_product_line(pc)
        date_last_chg = self.get_date_last_chg(pc)
        time_last_change = self.get_time_last_change(pc)
        amt_cost = self.get_amt_cost(pc)
        custom_props.append(PurchasedComponentCustomProperty(key='product_line', value=product_line))
        custom_props.append(PurchasedComponentCustomProperty(key='date_last_chg', value=str(date_last_chg)))
        custom_props.append(PurchasedComponentCustomProperty(key='time_last_change', value=str(time_last_change)))
        custom_props.append(PurchasedComponentCustomProperty(key='amt_cost', value=float(amt_cost)))
        return custom_props


class GlobalShopPurchasedComponentImportProcessor(GlobalShopPurchasedComponentBulkImportProcessor):

    def _process(self, purchased_component_id: str):
        self.bulk_import(purchased_component_ids=[purchased_component_id])


class GlobalShopPurchasedComponentPlaceholder:
    pass
