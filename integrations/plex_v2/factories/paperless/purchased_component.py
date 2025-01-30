from plex_v2.objects.part import Part, PartInventorySummaryGetDataSource
from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent
from plex_v2.configuration import PlexConfig
from pytz import timezone
from pendulum.datetime import DateTime
from plex_v2.utils.material_pricing_helper import MaterialPricingHelper
from baseintegration.datamigration import logger


class PaperlessPurchasedComponentFactory:

    plex_config: PlexConfig
    material_pricing_helper: MaterialPricingHelper

    def __init__(self, plex_config: PlexConfig, material_pricing_helper: MaterialPricingHelper):
        self.plex_config = plex_config
        self.material_pricing_helper = material_pricing_helper

    def to_pp_purchased_component(self, part: Part) -> PaperlessPurchasedComponent:
        pp_pc = PaperlessPurchasedComponent(
            oem_part_number=part.number,
            internal_part_number=part.number,
            description=self._get_description(part),
            piece_price=str(self.plex_config.default_pc_piece_price)
        )

        pp_pc.set_property("part_name", part.name)
        pp_pc.set_property("part_type", part.type)
        pp_pc.set_property("part_group", part.group)
        pp_pc.set_property("part_source", part.source)
        pp_pc.set_property("revision", part.revision)
        pp_pc.set_property("status", part.status)
        pp_pc.set_property("last_import_time", self._get_current_time())

        if self.plex_config.should_import_pc_pricing:
            price, price_unit = self.material_pricing_helper.get_price_and_pricing_unit(part)
            pp_pc.piece_price = str(price)
            pp_pc.set_property("price_unit", price_unit)

        # inventory levels
        if self.plex_config.should_import_pc_inventory:
            inv_summary: PartInventorySummaryGetDataSource = PartInventorySummaryGetDataSource.get(part.number)
            if len(inv_summary) == 0:
                logger.info(f'Could not get inventory information using data source 15664 for part number "{part.number}". This occured while importing purchased components.')

            else:
                inventory_dict: dict = inv_summary[0].to_dict()
                for property in inventory_dict:
                    if property in self.plex_config.pc_inventory_properties:
                        pp_pc.set_property(property, inventory_dict[property])

        return pp_pc

    def _get_description(self, part: Part) -> str:
        if len(part.description) == 0:
            return self.plex_config.default_description_if_blank
        return part.description[0:100]

    def _get_current_time(self) -> str:
        tz = timezone('EST5EDT')
        return (str(DateTime.now(tz))[0:19]).replace('T', ' ')
