import e2.models as e2
from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger
from datetime import datetime


class JobRequirementProcessor(E2Processor):
    do_rollback = False

    def _process(self, component, order_line_item, job_req_data):
        # Optionally, create a JobReq record if this is an outside service to assist with sending a PO to the vendor downstream
        order_routing_record = job_req_data.outside_service_routing_line
        if order_routing_record is not None and \
                self._exporter.erp_config.should_create_order_line_items_as_processed:
            self.create_job_req_record_for_outside_service(component, order_line_item, order_routing_record)

        # Optionally, create a JobReq record for the purchased component
        purchased_component = job_req_data.purchased_component
        purchased_component_part_record = job_req_data.purchased_component_part_record
        if purchased_component_part_record is not None and purchased_component is not None and \
                self._exporter.erp_config.should_create_order_line_items_as_processed:
            self.create_job_req_record_for_purchased_component(purchased_component, order_line_item, purchased_component_part_record)

        # Optionally, create a JobReq record for the raw material
        raw_material_part_record = job_req_data.raw_material_part_record
        raw_material_quantity = job_req_data.raw_material_quantity
        if raw_material_part_record is not None and raw_material_quantity is not None and \
                self._exporter.erp_config.should_create_order_line_items_as_processed:
            self.create_job_req_record_for_raw_material(raw_material_part_record, order_line_item, raw_material_quantity)

    def create_job_req_record_for_outside_service(self, component, order_line_item, order_routing_record):
        qty_to_buy = self.get_job_req_qty_to_buy_outside_service(component)
        date_entered = self.get_date_entered()
        job_due = self.get_outside_service_order_by_date(order_line_item)

        logger.info(f'Creating a JobReq record for job number {order_line_item.job_no} and vend code {order_routing_record.vend_code}')
        e2.JobReq.objects.create(
            orderno=order_line_item.orderno,
            jobno=order_line_item.job_no,
            partno=order_line_item.part_no,
            partdesc=order_line_item.part_desc,
            vendcode=order_routing_record.vend_code,
            qty2buy=qty_to_buy,
            jobdue=job_due,
            dateprocessed=date_entered,
            prodcode=order_line_item.prod_code,
            workcode=order_line_item.work_code,
            outsideservice='Y',
            stepno=order_routing_record.step_no,
            leadtime=order_routing_record.lead_time,
            cost=0,
            stockunit='EA',
            price=0,
            pricingunit='EA',
            purchqty=qty_to_buy,
            purchunit='EA',
            certreq='N',
            setupchg=0.,
            glcode=order_routing_record.gl_code,
            ponum=None,
            podate=None,
            tempjobdue=None,
        )

    def get_outside_service_order_by_date(self, order_line_item):
        job_due = order_line_item.due_date
        return job_due

    def get_job_req_qty_to_buy_outside_service(self, component):
        return self._exporter.get_deliver_quantity(component)

    def create_job_req_record_for_purchased_component(self, purchased_component, order_line_item, purchased_component_part_record):
        qty_to_buy = self.get_job_req_qty_to_buy_purchased_component(purchased_component)
        date_entered = self.get_date_entered()
        step_no = self.get_purchased_component_step_no(order_line_item)
        job_due = self.get_purchased_component_order_by_date(order_line_item)

        logger.info(
            f'Creating a JobReq record for job number {order_line_item.job_no} and purchased component {purchased_component_part_record.partno}')
        e2.JobReq.objects.create(
            orderno=order_line_item.orderno,
            jobno=order_line_item.job_no,
            partno=purchased_component_part_record.partno,
            partdesc=purchased_component_part_record.descrip,
            vendcode=purchased_component_part_record.vendcode1,
            qty2buy=qty_to_buy,
            jobdue=job_due,
            dateprocessed=date_entered,
            prodcode=purchased_component_part_record.prodcode,
            workcode=order_line_item.work_code,
            outsideservice='N',
            stepno=step_no,
            leadtime=purchased_component_part_record.leadtime,
            cost=0,
            stockunit='EA',
            price=0,
            pricingunit='EA',
            purchqty=qty_to_buy,
            purchunit='EA',
            certreq='N',
            setupchg=0.,
            glcode=purchased_component_part_record.glcode,
            ponum=None,
            podate=None,
            tempjobdue=None,
        )

    def get_purchased_component_order_by_date(self, order_line_item):
        job_due = order_line_item.due_date
        return job_due

    def get_job_req_qty_to_buy_purchased_component(self, component):
        return self._exporter.get_deliver_quantity(component)

    def get_purchased_component_step_no(self, order_line_item):
        return 0

    def create_job_req_record_for_raw_material(self, raw_material_part_record, order_line_item, raw_material_quantity):
        qty_to_buy = self.get_job_req_qty_to_buy_raw_material(raw_material_quantity)
        date_entered = self.get_date_entered()
        step_no = self.get_raw_material_step_no(order_line_item)
        job_due = self.get_raw_material_order_by_date(order_line_item)

        logger.info(
            f'Creating a JobReq record for job number {order_line_item.job_no} and raw material {raw_material_part_record.partno}')
        e2.JobReq.objects.create(
            orderno=order_line_item.orderno,
            jobno=order_line_item.job_no,
            partno=raw_material_part_record.partno,
            partdesc=raw_material_part_record.descrip,
            vendcode=raw_material_part_record.vendcode1,
            qty2buy=qty_to_buy,
            jobdue=job_due,
            dateprocessed=date_entered,
            prodcode=raw_material_part_record.prodcode,
            workcode=order_line_item.work_code,
            outsideservice='N',
            stepno=step_no,
            leadtime=raw_material_part_record.leadtime,
            cost=0,
            stockunit=raw_material_part_record.stockunit,
            price=0,
            pricingunit=raw_material_part_record.pricingunit,
            purchqty=qty_to_buy,
            purchunit=raw_material_part_record.pricingunit,
            certreq='N',
            setupchg=0.,
            glcode=raw_material_part_record.glcode,
            ponum=None,
            podate=None,
            tempjobdue=None,
        )

    def get_job_req_qty_to_buy_raw_material(self, raw_material_quantity):
        return raw_material_quantity

    def get_raw_material_order_by_date(self, order_line_item):
        job_due = order_line_item.due_date
        return job_due

    def get_raw_material_step_no(self, order_line_item):
        return 0

    def get_date_entered(self):
        now = datetime.now()
        date_entered = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        return date_entered
