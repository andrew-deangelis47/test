from paperless.objects.quotes import QuoteComponent

from dynamics.utils import DynamicsExportProcessor
from dynamics.exceptions import DynamicsNotFoundException
from dynamics.objects.item import Item
from dynamics.factories import ItemDataFactory


class PartProcessor(DynamicsExportProcessor):

    def _process(self, component: QuoteComponent) -> Item:
        factory: ItemDataFactory = self._exporter.item_data_factory

        try:
            # first check if part already exists
            if component.part_number:
                return Item.get_first({
                    'No': component.part_number
                })
            else:
                return Item.get_first({
                    'No': component.part_name
                })
        except DynamicsNotFoundException:
            # create part
            item_data: dict = factory.to_item_data(component)
            return Item.create(item_data)
