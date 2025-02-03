from dynamics.factories.base import DynamicsBaseFactory
from paperless.objects.orders import OrderComponent
from paperless.objects.quotes import QuoteComponent
from typing import Union


class ItemDataFactory(DynamicsBaseFactory):

    def to_item_data(self, component: Union[OrderComponent, QuoteComponent]) -> dict:
        return {
            'No': self._get_no(component),
            'Description': component.part_name,
            'Unit_Price': self._get_unit_price(component),
            'Tax_Group_Code': self.config.tax_group_code,
            'Base_Unit_of_Measure': self.config.base_unit_of_measure,
            'Gen_Prod_Posting_Group': self.config.gen_prod_posting_group,
            'Inventory_Posting_Group': self.config.inventory_posting_group,
            'Item_Category_Code': self._get_item_category_code(component)
        }

    def _get_no(self, component: Union[OrderComponent, QuoteComponent]) -> str:
        return component.part_number or component.part_name

    def _get_unit_price(self, component: Union[OrderComponent, QuoteComponent]) -> Union[float, int]:
        unit_price = 0
        if component.quantities and component.quantities[0].unit_price:
            unit_price = component.quantities[0].unit_price.dollars

        return unit_price

    def _get_item_category_code(self, component: Union[OrderComponent, QuoteComponent]) -> str:
        """
        we are intentionally not using the component here - this is here to help with overriding this for custom behavior
        """

        return ""
