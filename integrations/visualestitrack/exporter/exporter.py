from paperless.objects.orders import Order, OrderItem, OrderComponent
from baseintegration.exporter.order_exporter import OrderExporter
from visualestitrack.models import Requestforquote, Quoteheader
from visualestitrack.exporter.processors.rfq import CreateRFQ
from visualestitrack.exporter.processors.quote import CreateQuoteHeader, CreateQuotePeripherals


class VisualEstiTrackOrderExporter(OrderExporter):

    def _setup_erp_config(self):
        pass

    def _register_default_processors(self):
        self.register_processor(Requestforquote, CreateRFQ)
        self.register_processor(Quoteheader, CreateQuoteHeader)
        self.register_processor(Order, CreateQuotePeripherals)

    def _process_order(self, order: Order):
        with self.process_resource(Requestforquote, order) as rfq:
            order_item: OrderItem
            order_item_index = 1
            for order_item in order.order_items:
                components = {}
                primary_component: OrderComponent
                for item in order_item.components:
                    components[item.id] = item
                primary_component = components[order_item.root_component_id]
                self.recursive_quote_creation(rfq=rfq, order_item=order_item, component=primary_component,
                                              components=components, root_id=rfq.id, idx=order_item_index)
                order_item_index += 1
            return True

    def recursive_quote_creation(self, rfq: Requestforquote, order_item: OrderItem, component: OrderComponent,
                                 components: {OrderComponent}, root_id: str, idx: int):
        qid = f'{root_id}-{idx}'

        sdx = 0
        sub_count = 0
        purchased = []
        for child in component.child_ids:
            if components[child].type == "purchased":
                purchased.append(components[child])
                continue
            sdx += 1
            sub_count += self.recursive_quote_creation(rfq=rfq, order_item=order_item, component=components[child],
                                                       components=components, root_id=qid, idx=sdx)
        sub_count += sdx
        self.create_quote(rfq=rfq, order_item=order_item, component=component, root_id=root_id, qid=qid,
                          sub_count=sub_count, purchased=purchased)

        return sub_count

    def create_quote(self, rfq: Requestforquote, order_item: OrderItem, component: OrderComponent, root_id: str,
                     qid: str, sub_count: int, purchased: list):
        excluded_operations = []
        fg_add = True
        if not self._integration.test_mode:
            parser = self._integration.config_yaml["Exporters"]["orders"]
            excluded_operations = parser.get('excluded_operations', [])
            vet_parser = self._integration.config_yaml.get('VISUALESTITRACK', [])
            fg_add = vet_parser.get('included_fg_inventory', False)
        with self.process_resource(Quoteheader, rfq, order_item, component, root_id, qid, sub_count, fg_add) \
                as quote_header:
            with self.process_resource(Order, quote_header, order_item, component, purchased, excluded_operations):
                pass
