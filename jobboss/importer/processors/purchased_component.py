from typing import List

from baseintegration.utils import safe_get
import jobboss.models as jb
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.objects.purchased_components import PurchasedComponent, PurchasedComponentColumn

# Use a module-level variable to make sure this behavior only happens the first time the processor runs (per
# instantiation of the class). This is a way of saving redundant API calls
should_create_custom_columns = True


class PurchasedComponentBulkImportProcessor(BaseImportProcessor):

    def _process(self, purchased_component_ids: List[str]) -> bool:
        # Set default JobBOSS column names for initial import
        jobboss_column_names = [
            ("vendor", "string"),
            ("standard_cost", "numeric"),
            ("cost_uofm", "string"),
            ("last_cost", "numeric"),
            ("lead_days", "numeric"),
            ("location_id", "string"),
            ("last_updated", "string")
        ]
        try:
            self.create_purchased_component_columns(jobboss_column_names)
        except Exception as e:
            logger.info(f"Columns already created. {e}")

        purchased_component_list = []
        for purchased_component_id in purchased_component_ids:
            logger.info(f"Processing {purchased_component_id}")
            pc = jb.Material.objects.filter(material=purchased_component_id).first()
            if not pc:
                logger.info(f"Hardware material with id: {purchased_component_id} could not be found in JobBOSS. Skipping")
                continue

            piece_price = self.get_piece_price(pc)
            oem_part_number = self.get_oem_part_number(pc)
            internal_part_number = self.get_internal_part_number(pc)
            description = self.get_description(pc)

            purchased_component = PurchasedComponent(
                piece_price=piece_price,
                oem_part_number=oem_part_number,
                internal_part_number=internal_part_number,
                description=description)

            self.set_custom_properties(pc, purchased_component)

            purchased_component_list.append(purchased_component)

        result = PurchasedComponent.upsert_many(purchased_component_list)
        return len(result.failures) == 0

    def create_purchased_component_columns(self, jobboss_column_names):
        # Check if custom columns were created when the class was instantiated. Skip this if yes, else create them.
        if not self._importer.should_create_custom_columns:
            return
        purchased_component_columns = PurchasedComponentColumn.list()
        purchased_component_column_names = [pcc.code_name for pcc in purchased_component_columns]
        for column_tuple in jobboss_column_names:
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

    def get_piece_price(self, pc):
        piece_price = round(float(pc.standard_cost), 2) if pc.standard_cost > 0 else 0.01
        return str(piece_price)

    def get_oem_part_number(self, pc):
        oem_part_number = pc.material
        return oem_part_number

    def get_internal_part_number(self, pc):
        # The Open API does not currently allow blank values for this field, but it does allow None
        internal_part_number = "None"
        return internal_part_number

    def get_description(self, pc):
        # The Open API does not currently allow blank values for this field, but it does allow None
        description = safe_get(pc, 'description')
        if description is not None:
            description = description[:100]  # The API allows a max length of 100 for this field
        return description

    def get_vendor(self, pc):
        vendor = safe_get(pc, 'primary_vendor.vendor')
        return vendor

    def get_standard_cost(self, pc):
        standard_cost = round(float(pc.standard_cost), 2) if pc.standard_cost > 0 else 0.01
        return standard_cost

    def get_cost_uofm(self, pc):
        cost_uofm = pc.price_uofm
        return cost_uofm

    def get_last_cost(self, pc):
        last_cost = round(float(pc.last_cost), 2) if pc.last_cost > 0 else 0.01
        return last_cost

    def get_lead_days(self, pc):
        lead_days = pc.lead_days
        return lead_days

    def get_location_id(self, pc):
        location_id = pc.location_id
        return location_id

    def get_last_updated(self, pc):
        last_updated = str(pc.last_updated)
        return last_updated

    def set_custom_properties(self, pc, purchased_component):
        vendor = self.get_vendor(pc)
        standard_cost = self.get_standard_cost(pc)
        cost_uofm = self.get_cost_uofm(pc)
        last_cost = self.get_last_cost(pc)
        lead_days = self.get_lead_days(pc)
        location_id = self.get_location_id(pc)
        last_updated = self.get_last_updated(pc)
        purchased_component.set_property('vendor', vendor)
        purchased_component.set_property('standard_cost', standard_cost)
        purchased_component.set_property('cost_uofm', cost_uofm)
        purchased_component.set_property('last_cost', last_cost)
        purchased_component.set_property('lead_days', lead_days)
        purchased_component.set_property('location_id', location_id)
        purchased_component.set_property('last_updated', last_updated)


class PurchasedComponentImportProcessor(PurchasedComponentBulkImportProcessor):
    def _process(self, purchased_component_id: str) -> bool:
        return super()._process([purchased_component_id])


class PurchasedComponentBulkPlaceholder:
    pass
