from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Part
from mietrak_pro.models import Item, Router, Quote, Quoteassembly, Workorder
from baseintegration.datamigration import logger
from mietrak_pro.utils.repeat_work_utils import is_purchased_component


class RepeatPartProcessor(BaseImportProcessor):
    def _process(self, repeat_part_number: str):
        logger.info(f"Creating repeat part from Mie Trak Pro item ID: {repeat_part_number}")

        item: Item = Item.objects.select_related('itemtypefk').get(pk=repeat_part_number)
        part_number = item.partnumber or str(item.pk)
        logger.info(f"Processing part number {part_number} for item PK {repeat_part_number}")

        repeat_part = Part(
            part_number=part_number,
            revision=item.revision,
            type=self.get_part_type(item),
            erp_name="mietrak_pro",
            is_root=self.is_root(item),
            size_x=item.partlength,
            size_y=item.partwidth,
            thickness=item.thickness,
            area=item.partarea
        )

        return repeat_part, item

    @classmethod
    def get_part_type(cls, item: Item) -> str:
        if is_purchased_component(item):
            return "purchased"
        return "manufactured"  # this is potentially changed later, in the method of manufacture processor

    @classmethod
    def is_root(cls, item: Item) -> bool:
        # if a router exists for the item, it is a root
        item_router = Router.objects.filter(itemfk=item).first()
        if item_router:
            return True

        # if any quote of the item is not an "Item Quote" in some quote line, it is a root
        quotes = Quote.objects.filter(itemfk=item)
        for quote in quotes:
            if not Quoteassembly.objects.filter(itemquotefk=quote).exists():
                return True

        # if a workorder exists for the item, it is a root
        if Workorder.objects.filter(itemfk=item).exists():
            return True

        return False
