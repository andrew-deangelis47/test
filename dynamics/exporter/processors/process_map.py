from dynamics.utils import DynamicsExportProcessor
from dynamics.objects.item import Item, Routing, ProductionBOM, ProcessMap
from dynamics.objects.customer import Customer


class ProcessMapProcessor(DynamicsExportProcessor):

    def _process(self, customer: Customer, item: Item, routing: Routing, bom: ProductionBOM) -> None:
        return ProcessMap.get_or_create({
            "Item_No": item.No,
        }, {
            "Variant_Code": customer.No,
            "Routing_No": routing.No,
            "Production_BOM_No": bom.No,
            "Modifier": "1"
        })
