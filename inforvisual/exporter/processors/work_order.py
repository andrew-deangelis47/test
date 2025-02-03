
from baseintegration.exporter import BaseProcessor
from inforvisual.models import WorkOrder, Part
from inforvisual.exporter.utils import PartData, WorkOrderData, PurchasedComponentData, WorkOrderChildData
from paperless.objects.orders import Order, OrderComponent, OrderItem
from baseintegration.datamigration import logger
import datetime


class WorkOrderProcessor(BaseProcessor):

    def _process(self, order: Order, part_data: list, order_item_data: list):
        logger.info("Processing work orders")
        self.part_data = part_data
        self.work_orders = []
        self.purchased_components = []
        for item in order_item_data:
            order_item = item.order_item
            if item.should_process:
                self.get_work_orders(order_item)
        logger.info("Done processing work orders")
        return self.work_orders, self.purchased_components

    def get_work_orders(self, item: OrderItem):
        root: OrderComponent = item.root_component
        logger.info(f"Getting component with id {str(root.part_number)} from existing components")
        part_data: PartData = self.get_component_part_data(root.id)
        # we only need to create the master engineering work orders if the part doesn't exist
        if part_data.part_is_new:
            logger.info(f"Part {str(root.part_number)} is new, creating work orders for it")
            # nonmaster part is lot id 1, master part is lot id 0
            lot_id = 0
            # base id is part id because it is the engineering master
            base_id = part_data.part.id
            # sub id is 0 for the opening work order
            parent_work_order_data: WorkOrderData = self.create_work_order(part_data.part, lot_id, base_id, root, 0, item.ships_on_dt)
            self.work_orders.append(parent_work_order_data)
            sub_id = 1
            logger.info("Getting child work orders")
            self.get_child_work_orders(lot_id, base_id, root, sub_id, item.ships_on_dt, root.deliver_quantity, parent_work_order_data)

    def create_work_order(self, part_object: Part, lot_id: int, base_id: int, component: OrderComponent, sub_id: int, ships_on_dt: datetime) -> WorkOrderData:
        logger.info(f"Creating work order. Base id is {base_id} and sub id is {sub_id}")
        # If not using legs, set all to engineering masters
        if not self._exporter.erp_config.leg_assembly:
            sub_id = 0
            base_id = part_object.id
        new_wo = WorkOrder.objects.create(
            type="M",
            base_id=base_id,
            lot_id=lot_id,
            split_id=0,
            sub_id=sub_id,  # tbd
            part=part_object,
            global_rank=50,
            status="U",  # tbd
            desired_qty=10,
            received_qty=0,
            create_date=datetime.datetime.now(),
            status_eff_date=datetime.datetime.now(),
            desired_rls_date=ships_on_dt,
            product_code=part_object.product_code,
            commodity_code=part_object.commodity_code,
            forward_schedule="N",
            posting_candidate="N",
            warehouse_id=self._exporter.erp_config.default_site_id,
            marked_for_purge="N",
            dbr_type="O",
            wbs_project="N",
            edi_blanket_flag="N",
            allow_upd_from_mst="Y",
            allow_upd_from_leg="Y",
            site_id=self._exporter.erp_config.default_site_id,
            inactive="N",
            customer_priority=0
        )
        child_data = WorkOrderChildData()
        child_data.child_work_orders = []

        return WorkOrderData(work_order=new_wo, component=component, part_is_new=True, child_data=child_data)

    def get_component_part_data(self, component_id: int):
        for p_data in self.part_data:
            p_data: PartData = p_data
            if p_data.component.id == component_id:
                return p_data
        else:
            raise ValueError("Could not find the necessary component in the list")

    def get_child_work_orders(self, lot_id, base_id, root, sub_id, ships_on_dt, parent_quantity: int, parent_work_order_data: WorkOrderData):
        if len(root.child_ids) == 0:
            return sub_id
        for child_node in root.children:
            quantity_per_parent = child_node.quantity
            total_child_quantity = quantity_per_parent * parent_quantity
            tup: PartData = self.get_component_part_data(child_node.child_id)
            part_object: Part = tup.part
            component: OrderComponent = tup.component
            if component.purchased_component:
                logger.info(f"Component {component.part_number} is a purchased component, not creating a work order")
                purchased_component_data = PurchasedComponentData(
                    part=part_object,
                    component=component,
                    quantity_per_parent=quantity_per_parent,
                    deliver_quantity=total_child_quantity
                )
                self.purchased_components.append(purchased_component_data)
                if parent_work_order_data:
                    parent_work_order_data.child_data.child_purchased_components.append(purchased_component_data)
                continue
            if tup.part_is_new is False:
                logger.info(f"Child component {component.part_number} is not new, skipping")
                continue
            work_order_data = self.create_work_order(part_object, lot_id, base_id, component, sub_id, ships_on_dt)
            work_order_data = work_order_data._replace(
                quantity_per_parent=quantity_per_parent,
                deliver_quantity=total_child_quantity
            )
            self.work_orders.append(work_order_data)
            if parent_work_order_data:
                parent_work_order_data.child_data.child_work_orders.append(work_order_data)
            sub_id = sub_id + 1
            if component.child_ids:
                sub_id = self.get_child_work_orders(
                    lot_id, base_id, component, sub_id, ships_on_dt, total_child_quantity, work_order_data
                )
        return sub_id
