from typing import Union

from mietrak_pro.models import Item
from mietrak_pro.exporter.processors import MietrakProProcessor
from mietrak_pro.exporter.utils import AddOnData
from paperless.objects.orders import OrderedAddOn
from paperless.objects.quotes import AddOn
from baseintegration.utils import logger


class AddOnProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, add_on: Union[AddOn, OrderedAddOn]):
        add_on_item = self.get_add_on_item(add_on)
        if add_on_item is None:
            return None
        should_include_add_on_item_in_bom = self.should_include_add_on_item_in_bom(add_on_item)
        return AddOnData(add_on=add_on, add_on_item=add_on_item,
                         should_include_add_on_item_in_bom=should_include_add_on_item_in_bom)

    def get_add_on_item(self, add_on: Union[AddOn, OrderedAddOn]):
        raise NotImplementedError()

    def should_include_add_on_item_in_bom(self, add_on_item: Item):
        """ This is the convention that Chad Helland and I decided on during a meeting on 10/7/2021. The other possible
            type for add-on items is 'Miscellaneous', and we decided that only 'Tooling' items should show up in the
            BOM. """
        if add_on_item is not None and add_on_item.itemtypefk.description == 'Tooling':
            return True
        else:
            return False


class OrderAddOnProcessor(AddOnProcessor):

    def get_add_on_item(self, add_on: OrderedAddOn):
        add_on_item_id_var = add_on.get_variable('MIE Trak Pro Item ID')
        add_on_item = None
        if add_on_item_id_var is None:
            return
        try:
            add_on_item_id = int(float(add_on_item_id_var.value))
            add_on_item = Item.objects.filter(itempk=add_on_item_id).first()
            logger.info(f'Add on -> {vars(add_on_item)}')
        except:
            pass
        return add_on_item


class QuoteAddOnProcessor(AddOnProcessor):

    def get_add_on_item(self, add_on: AddOn):
        add_on_item_id = None
        for cv in add_on.costing_variables:
            if cv.label == 'MIE Trak Pro Item ID':
                # Assume that the workcenter costing variable is not quantity-specific and that any quantity will do
                try:
                    add_on_item_id = list(cv.quantities.values())[0].value
                except:
                    pass
        if add_on_item_id is None:
            return None
        try:
            add_on_item = Item.objects.filter(itempk=add_on_item_id).first()
        except:
            add_on_item = None
        return add_on_item
