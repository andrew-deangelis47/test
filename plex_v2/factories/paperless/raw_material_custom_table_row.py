from plex_v2.objects.part import Part, PartInventorySummaryGetDataSource
from pytz import timezone
from pendulum.datetime import DateTime
from typing import List
from typing import Union
from plex_v2.objects.raw_material_attribute import RawMaterialAttribute
from plex_v2.factories.base import BaseFactory
from plex_v2.utils.material_pricing_helper import MaterialPricingHelper
from plex_v2.configuration import PlexConfig
from plex_v2.utils.import_utils import ImportUtils
from baseintegration.datamigration import logger


class RawMaterialCustomTableRowFactory(BaseFactory):

    config: PlexConfig
    utils: ImportUtils
    material_pricing_helper: MaterialPricingHelper

    def __init__(self, config: PlexConfig, utils: ImportUtils, material_pricing_helper: MaterialPricingHelper):
        self.config = config
        self.utils = utils
        self.material_pricing_helper = material_pricing_helper

    def to_custom_table_row(self, part: Part, attributes: List[RawMaterialAttribute]):
        row = {
            "Number": part.number,
            "Revision": part.revision,
            "Number_And_Revision": self._get_number_rev(part),
            "Description": part.description,
            "Part_Name": part.name,
            "Part_Type": part.type,
            "Part_Group": part.group,
            "Part_Source": part.source,
            "Status": part.status,
            "Lead_Time_Days": part.leadTimeDays,
            "Last_Import_Time": self._get_current_time()
        }

        # add pricing if configured
        if self.config.should_import_material_pricing:
            price, price_unit = self.material_pricing_helper.get_price_and_pricing_unit(part)
            row['Price'] = price
            row['Price_Unit'] = price_unit

        # add attributes, replace space with underscore
        attribute: RawMaterialAttribute
        for attribute in attributes:
            row[attribute.field.replace(" ", "_")] = self._validate_numeric(attribute)

        # add inventory levels if configured, only add the properties configured
        if self.config.should_import_material_inventory:
            inv_summary: PartInventorySummaryGetDataSource = PartInventorySummaryGetDataSource.get(part.number)
            if len(inv_summary) == 0:
                logger.info(
                    f'Could not get inventory information using data source 15664 for part number "{part.number}". This occured while importing material.')

            inventory_dict: dict = inv_summary[0].to_dict()
            for property in inventory_dict:
                if property in self.config.material_inventory_properties:
                    row[property] = inventory_dict[property]

        return row

    def _get_current_time(self) -> str:
        tz = timezone('EST5EDT')
        return (str(DateTime.now(tz))[0:19]).replace('T', ' ')

    def _get_number_rev(self, part: Part) -> str:
        number_rev = part.number
        if len(part.revision) > 0:
            number_rev += ' Rev:' + part.revision

        return number_rev

    def _validate_numeric(self, attribute: RawMaterialAttribute) -> Union[str, int, float]:
        """
        if the value should be numeric and it's not then default it to a numeric value
        """
        # cast to numeric
        if attribute.type != 'str' and (not str(attribute.value).replace('.', '').isnumeric() or attribute.value == ''):
            return self.config.default_raw_material_numeric_value
        return attribute.value
