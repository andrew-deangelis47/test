from e2.exporter.processors.order_line_item import OrderLineItemProcessor
from e2.models import OrderDet, Releases, OrderRouting, Routing, Workcntr, Opercode
from e2.utils.utils import OrderLineItemData
from baseintegration.datamigration import logger


class E2ShopSystemOrderLineItemProcessor(OrderLineItemProcessor):

    def _process(self, order_item, order, order_header, part, component, order_item_number, parent_job_number):
        e2_order_number = self.get_e2_order_number(order_header)
        part_number = self.get_part_number(part)
        quantity_to_make = self.get_quantity_to_make(component)

        order_line_item = self.create_order_line_item(order_item, order, order_header, part, component,
                                                      order_item_number, parent_job_number)

        # TODO - move this to _post_process
        # Populate the OrderRouting records for this order line item from the Estim's Routing records
        date_entered = self.get_date_entered()
        add_on_routing_lines = []
        if self._exporter.erp_config.should_populate_order_routing_for_add_ons:
            add_on_routing_lines = self.populate_order_routing_from_paperless_add_ons(component, order_item,
                                                                                      order_line_item, part,
                                                                                      date_entered)
        order_routing_lines = self.copy_routing_from_template_part_to_order_routing_table(
            part_number, e2_order_number, order_item_number, part_number, quantity_to_make, date_entered,
            order_line_item, add_on_routing_lines)
        logger.info(order_routing_lines)

        # Also populate a Releases record for this order line item
        del_type = self.get_del_type(component)
        release_quantity = self.get_release_quantity(component)
        release = Releases.objects.create(
            orderno=order_line_item.orderno,
            jobno=order_line_item.job_no,
            partno=order_line_item.part_no,
            partdesc=order_line_item.part_desc,
            deltype=del_type,
            qty=release_quantity,
            duedate=order_line_item.due_date,
            datecomplete=None,
            deliveryticketno='',
            comments=None,
            itemno=order_line_item.itemno,
            destjobno=None,
            mfgjobno=None,
            binlocation=None,
            lotno=None,
            edisoftitemno=None,
        )

        order_line_item_data = OrderLineItemData(
            order_line_item=order_line_item,
            order_routing_lines=order_routing_lines,
            release=release
        )
        return order_line_item_data

    def create_order_line_item(self, order_item, order, order_header, part, component, order_item_number,
                               parent_job_number):
        e2_order_number = self.get_e2_order_number(order_header)
        job_number = self.get_job_number(e2_order_number, order_item_number)
        master_job_number = self.get_master_job_number(parent_job_number)
        due_date = self.get_due_date(order, order_item)

        job_notes = self.get_job_notes(component, order, order_item, part)
        part_description = self.get_part_description(order_item, part)

        part_number = self.get_part_number(part)

        revision = self.get_revision(part)
        prod_code = self.get_prod_code(part)
        misc_descrip = self.get_part_misc_descrip(part)
        misc_chg = None
        misc_chg_billed = "N"

        if order_item.ordered_add_ons is not None and len(order_item.ordered_add_ons) > 0:
            logger.info("Adding add-ons")
            misc_chg_billed = "Y"
            misc_descrip = ""
            misc_chg = 0
            for add_on in order_item.ordered_add_ons:
                # e2 shop system only supports one add-on
                if misc_descrip != "":
                    misc_descrip = misc_descrip + ","
                misc_descrip = misc_descrip + add_on.name
                misc_chg = misc_chg + float(add_on.price.dollars)

        billing_rate = self.get_billing_rate(part)

        work_code = self.get_work_code(order_item, order, part)
        fob = self.get_fob(order_item, order, part)
        status = self.get_status()

        unit_price = self.get_unit_price(component, order_item)

        quantity_ordered = self.get_quantity_ordered(component)
        quantity_to_make = self.get_quantity_to_make(component)
        quantity_to_stock = self.get_quantity_to_stock(component)

        return OrderDet.objects.create(
            orderno=e2_order_number,
            job_no=job_number,
            part_no=part_number,
            part_desc=part_description,
            status=status,
            billing_rate=billing_rate,
            work_code=work_code,
            prod_code=prod_code,
            priority=50,
            unit_price=unit_price,
            pricing_unit='EA',
            master_job_no=master_job_number,
            misc_chg=misc_chg,
            misc_descrip=misc_descrip,
            estim_start_date=None,
            estim_end_date=None,
            actual_start_date=None,
            actual_end_date=None,
            misc_chg_billed=misc_chg_billed,
            trav_printed=None,
            disc_pct=0.0,
            cumulative_billing=None,
            fob=fob,
            revision=revision,
            comm_pct=0.,
            job_notes=job_notes,
            qty_ordered=quantity_ordered,
            qty_to_make=quantity_to_make,
            qty_to_stock=quantity_to_stock,  # TODO - what to do here?
            qty_canceled=0,
            qty_shipped_2_cust=0,
            qty_shipped_2_stock=0,
            total_est_hrs=0.0,
            total_actual_hrs=None,
            due_date=due_date,
            prev_saved='Y',  # TODO - what to do here?
            rel_set=None,
            date_finished=None,
            current_work_cntr=None,
            itemno=order_item_number,
            job_label_printed=None,
            schedule_locked='N',
            over_lap='N',
            scheduled='N',
            master_step_no=None,
            user_date1=None,
            user_date2=None,
            user_text1=None,
            user_text2=None,
            user_text3=None,
            user_text4=None,
            user_currency1=None,
            user_currency2=None,
            user_number1=None,
            user_number2=None,
            user_number3=None,
            user_number4=None,
            user_memo1=None,
            temp_priority=None,
            quote_no=None,
            quote_item_no=None,
            job_on_hold='N',
            convert_me=None
        )

    def create_order_routing_line_from_add_on(self, add_on, step_number, component, order_line_item, part,
                                              date_entered):
        work_center_short_name, is_default_work_center_name = self.get_work_center_name(add_on)

        routing_processor = self._exporter.get_processor_instance(Routing)
        default_work_center = routing_processor.get_or_create_default_work_center()

        # Get the WorkCntr record and accompanying default OperCode record
        # The E2 UI enforces uniqueness of the WorkCntr ShortName field, so we can use this in place of a primary key
        work_center = Workcntr.objects.filter(shortname=work_center_short_name).first()
        if work_center is None:
            logger.info(f'Could not find a WorkCntr record with ShortName {work_center_short_name} - assigning to '
                        f'default work center {default_work_center.shortname}')
            work_center = default_work_center
            is_default_work_center_name = True

        oper_code = Opercode.objects.filter(opercode=work_center.opercode).first()
        if oper_code is not None:
            routing_oper_code = oper_code.opercode
            team_size = oper_code.teamsize
            scrap_pct = oper_code.scrappct
            pct_eff = oper_code.pcteff
            unattend_op = oper_code.unattendop
            num_mach_for_job = oper_code.nummach
        else:
            logger.info('Could not find an OperCode record for this work center')
            routing_oper_code = None
            team_size = None
            scrap_pct = None
            pct_eff = None
            unattend_op = None
            num_mach_for_job = None

        descrip = self.get_add_on_description(is_default_work_center_name, add_on)

        order_routing_line = OrderRouting.objects.create(
            order_no=order_line_item.orderno,
            part_no=order_line_item.part_no,
            step_no=step_number,
            work_or_vend=0,
            work_cntr=work_center.shortname,
            vend_code=None,
            oper_code=routing_oper_code,
            descrip=descrip,
            setup_time=0.,
            time_unit=self._exporter.erp_config.setup_time_units,
            cycle_time=0.,
            cycle_unit=self._exporter.erp_config.runtime_units,
            mach_run=1,
            team_size=team_size,
            scrap_pct=scrap_pct,
            pct_eff=pct_eff,
            labor_acct=work_center.laboracct,
            setup_rate=0.,
            cycle_rate=0.,
            burden_rate=work_center.burdenrate,
            labor_rate=work_center.laborrate,
            unattend_op=unattend_op,
            lead_time=part.leadtime,
            markup_pct=part.markuppct,
            cert_req='N',
            gl_code=None,
            cost1=0.,
            unit1='EA',
            setup1=0.,
            cost2=0.,
            unit2='EA',
            setup2=0.,
            cost3=0.,
            unit3='EA',
            setup3=0.,
            cost4=0.,
            unit4='EA',
            setup4=0.,
            cost5=0.,
            unit5='EA',
            setup5=0.,
            cost6=0.,
            unit6='EA',
            setup6=0.,
            cost7=0.,
            unit7='EA',
            setup7=0.,
            cost8=0.,
            unit8='EA',
            setup8=0.,
            setup_price=None,
            cycle_price=None,
            total=None,
            estim_start_date=None,
            estim_end_date=None,
            actual_start_date=None,
            actual_end_date=None,
            estim_qty=None,
            actual_pcs_good=None,
            actual_pcs_scrap=None,
            ignore_vend_min=None,
            item_no=order_line_item.itemno,
            status='Future',
            empl_code='',
            tot_est_hrs=0.,
            tot_act_hrs=None,
            tot_hrs_left=0.,
            dept_num=None,
            overlap='N',
            shift_2_def_empl_code='',
            shift_3_def_empl_code='',
            num_mach_for_job=num_mach_for_job,
            job_no=order_line_item.job_no
        )
        return order_routing_line

    def copy_routing_from_template_part_to_order_routing_table(self, template_part_no, e2_order_number,  # noqa: C901
                                                               order_item_number, part_number, quantity,
                                                               date_entered, order_line_item, add_on_routing_lines):
        template_routing_records = Routing.objects.filter(partno=template_part_no).order_by('stepno')
        logger.info(
            f'Inserting {len(template_routing_records)} OrderRouting records for part number {template_part_no}')
        order_routing_lines = [*add_on_routing_lines]
        # If we created order routing lines for add-ons, start counting up from the last one's sequence number
        step_number = 10
        for routing_row in template_routing_records:
            order_routing = OrderRouting()
            for field in routing_row._meta.get_fields():
                routing_name = field.name.lower()
                order_routing_name = routing_name
                if routing_name in NAME_TRANSLATOR:
                    order_routing_name = NAME_TRANSLATOR[routing_name]
                if routing_name in ['routing_id']:
                    continue

                if order_routing_name == "part_no":
                    logger.info("inserting part no")
                    setattr(order_routing, order_routing_name, part_number)
                elif order_routing_name == "estim_qty":
                    setattr(order_routing, order_routing_name, quantity)
                elif order_routing_name == "unattend_op":
                    setattr(order_routing, order_routing_name, None)
                else:
                    setattr(order_routing, order_routing_name, getattr(routing_row, routing_name))

            for field in order_routing._meta.get_fields():
                order_routing_field = field.name
                if order_routing_field == "item_no":
                    setattr(order_routing, order_routing_field, order_item_number)
                if order_routing_field == "status":
                    setattr(order_routing, order_routing_field, 'Future')
                if order_routing_field == "empl_code":
                    setattr(order_routing, order_routing_field, '')
                if order_routing_field == "tot_est_hrs":
                    setattr(order_routing, order_routing_field, 0.0)
                if order_routing_field == "tot_hrs_left":
                    setattr(order_routing, order_routing_field, 0.0)
                if order_routing_field == "overlap":
                    setattr(order_routing, order_routing_field, 'N')
                if order_routing_field == "shift_2_def_empl_code":
                    setattr(order_routing, order_routing_field, '')
                if order_routing_field == "shift_3_def_empl_code":
                    setattr(order_routing, order_routing_field, '')
                if order_routing_field == "num_mach_for_job":
                    setattr(order_routing, order_routing_field, 1.0)
                if order_routing_field == "setup_price":
                    setattr(order_routing, order_routing_field, None)
                if order_routing_field == "cycle_price":
                    setattr(order_routing, order_routing_field, None)
                if order_routing_field == "total":
                    setattr(order_routing, order_routing_field, None)
                if order_routing_field == "ignore_vend_min":
                    setattr(order_routing, order_routing_field, None)
                if order_routing_field == "job_no":
                    setattr(order_routing, order_routing_field, order_line_item.job_no)

            order_routing.order_no = e2_order_number
            order_routing.step_no = step_number
            logger.info(f"Inserting step no {step_number}")
            order_routing.save()
            order_routing_lines.append(order_routing)
            step_number += 10
        return tuple(order_routing_lines)


NAME_TRANSLATOR = {
    'partno': 'part_no',
    'stepno': 'step_no',
    'workorvend': 'work_or_vend',
    'workcntr': 'work_cntr',
    'vendcode': 'vend_code',
    'opercode': 'oper_code',
    'setuptime': 'setup_time',
    'timeunit': 'time_unit',
    'cycletime': 'cycle_time',
    'cycleunit': 'cycle_unit',
    'machrun': 'mach_run',
    'teamsize': 'team_size',
    'scrappct': 'scrap_pct',
    'pcteff': 'pct_eff',
    'laboracct': 'labor_acct',
    'setuprate': 'setup_rate',
    'cyclerate': 'cycle_rate',
    'burdenrate': 'burden_rate',
    'laborrate': 'labor_rate',
    'unattendop': 'unattend_op',
    'leadtime': 'lead_time',
    'markuppct': 'markup_pct',
    'certreq': 'cert_req',
    'glacct': 'gl_code',
    'setupprice': 'setup_price',
    'cycleprice': 'cycle_price',
    'estimqty': 'estim_qty',
    'actualpiecesgood': 'actual_pcs_good',
    'actualpiecesscrapped': 'actual_pcs_scrap',
    'ignorevendmin': 'ignore_vend_min',
    'nummachforjob': 'num_mach_for_job'
}
