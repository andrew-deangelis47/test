import datetime
import decimal
from typing import Optional

import jobboss.models as jb
from baseintegration.datamigration import logger
import uuid
from . import JobBossProcessor
from jobboss.query.job import get_template_job, get_most_recent_job
from string import ascii_uppercase
from math import floor
from jobboss.utils.utils import SuffixPosition
from paperless.objects.orders import OrderItem, OrderComponent, Order
from baseintegration.utils import safe_get, trim_django_model
from django.utils.timezone import make_aware


class JobProcessor(JobBossProcessor):
    def process_notes(self, order_item: OrderItem):
        notes = []
        desc = None
        ext_desc = None
        if order_item.description:
            desc = order_item.description[0:30]
            ext_desc = order_item.description
        if order_item.public_notes:
            notes.append(order_item.public_notes)
        if order_item.private_notes:
            notes.append(order_item.private_notes)
        return notes, desc, ext_desc

    def get_extras(self, order_item: OrderItem, comp: OrderComponent):
        extras = self._exporter.get_make_quantity(comp) - order_item.quantity * self._exporter.get_innate_quantity(comp)
        scrap_pct = (extras / self._exporter.get_make_quantity(comp)) * 100
        return extras, scrap_pct

    def get_employee_info(self, so_header: jb.SoHeader):
        commission_pct = 0
        employee = None
        if self._exporter.erp_config.sales_orders_active and so_header.customer:
            qs = jb.Employee.objects.filter(employee=so_header.customer)
            employee = qs.first()
            if employee:
                commission_pct = employee.commission_pct
        return employee, commission_pct

    @staticmethod
    def get_prefix(comp):
        return ""

    def get_suffix(self, comp):
        self.suffix = ""

    @staticmethod
    def get_assembly_suffix(assm_comp, processed_parents):
        """
        - Accepts an assembly component and records of previously processed parents as args.
        - Compares the current position index to the parent_id position index.
        - If they are on different levels, the function knows the component is the first comp that belongs to a specific
         parent id. It will update the parent position to the current position.
        - If they are on the same level, the parent will contain the previous position and count up one level_index.
        - Function returns a positional code that describes the index of the character to be appended next.
        - Function returns the job name that a character will be appended/prepended to
        """
        suffix_position = SuffixPosition(assm_comp.level, assm_comp.level_index, assm_comp.level_count, None)
        parent_id = safe_get(assm_comp, 'parent.id')
        parent_data = processed_parents.get(parent_id, None)
        if parent_data:
            parent_job = parent_data.parent_job
            if parent_data.level == assm_comp.level:
                suffix_position = SuffixPosition(parent_data.level, parent_data.level_index + 1,
                                                 parent_data.level_count, parent_job)
            elif parent_data.level < assm_comp.level:
                suffix_position = SuffixPosition(assm_comp.level, 0, assm_comp.level_count, parent_job)
            processed_parents[parent_id] = suffix_position
        return suffix_position

    def generate_custom_job_number(self, separator, prefix, suffix_position):
        """
        Overridable method to allow new assembly naming conventions to be defined and appended.
        This method will generate the following structure:
        -00001
            -00001-1...
            -00001-999
                -00001-1A...
                -00001-999ZZ
                    -00001-999ZZ1 etc...
        Each iteration sets the parent job to the job name at the level above it. Child jobs then add the appropriate
        characters to the parent job based on their sequence at that specific assembly level.
        Handing in the process() method ensures a root component is never passed to this function.
        """
        if not suffix_position.parent_job:
            logger.info("No parent job exists to generate the assembly job name.")
            return suffix_position
        if suffix_position.level % 2 == 0:
            if suffix_position.level_index < 26:
                character = str(ascii_uppercase[suffix_position.level_index])
            elif suffix_position.level_index < 325:
                first_character = str(ascii_uppercase[floor(suffix_position.level_index / 25) - 1])
                second_character = str(ascii_uppercase[suffix_position.level_index % 26])
                character = f"{first_character}{second_character}"
            else:
                logger.error(
                    f"There are more than 325 components at this assembly level. Parent job number: {suffix_position.parent_job.job}")
                character = "ZZZ"
        else:
            character = str(suffix_position.level_index + 1)
        if suffix_position.level == 1:
            # Separator is only written at the first assembly level, child components will copy the parent job string
            # which includes the separator.
            return f"{prefix}{suffix_position.parent_job.job}{separator}{self.suffix}{character}"
        return f"{prefix}{suffix_position.parent_job.job}{self.suffix}{character}"

    def create_user_values(self, order_item, comp, now) -> Optional[jb.UserValues]:
        return None

    def create_job_from_template(
            self, template_job: jb.Job, employee, commission_pct, customer: jb.Customer, so_header: jb.SoHeader,
            today, now, order: Order, order_item: OrderItem, comp: OrderComponent, top_level_job: jb.Job, notes
    ):
        job = jb.Job(
            sales_rep=employee,
            commission_pct=commission_pct,
            customer=customer,
            ship_to=safe_get(so_header, 'ship_to'),
            contact=safe_get(so_header, 'contact'),
            terms=safe_get(so_header, 'terms', default_value="Net 30 days"),
            sales_code=template_job.sales_code,
            type=template_job.type,
            order_date=today,
            status=self._exporter.erp_config.import_job_as,
            status_date=today,
            part_number=template_job.part_number,
            rev=template_job.rev,
            description=template_job.description,
            ext_description=template_job.ext_description,
            drawing=template_job.drawing,
            build_to_stock=template_job.build_to_stock,
            quote=f'PPQ#{order.quote_number}-{order.quote_revision_number}',
            order_quantity=self._exporter.get_deliver_quantity(comp),
            extra_quantity=template_job.extra_quantity,
            pick_quantity=template_job.pick_quantity,
            make_quantity=self._exporter.get_make_quantity(comp),
            split_quantity=template_job.split_quantity,
            completed_quantity=0,
            shipped_quantity=0,
            fg_transfer_qty=0,
            returned_quantity=0,
            in_production_quantity=0,
            assembly_level=template_job.assembly_level,
            certs_required=template_job.certs_required,
            time_and_materials=template_job.time_and_materials,
            open_operations=template_job.open_operations,
            scrap_pct=template_job.scrap_pct,
            est_scrap_qty=template_job.est_scrap_qty,
            est_rem_hrs=template_job.est_rem_hrs,
            est_total_hrs=template_job.est_total_hrs,
            est_labor=template_job.est_labor,
            est_material=template_job.est_material,
            est_service=template_job.est_service,
            est_labor_burden=template_job.est_labor_burden,
            est_machine_burden=template_job.est_machine_burden,
            est_ga_burden=template_job.est_ga_burden,
            act_revenue=template_job.act_revenue,
            act_scrap_quantity=template_job.act_scrap_quantity,
            act_total_hrs=template_job.act_total_hrs,
            act_labor=template_job.act_labor,
            act_material=template_job.act_material,
            act_service=template_job.act_service,
            act_labor_burden=template_job.act_labor_burden,
            act_machine_burden=template_job.act_machine_burden,
            act_ga_burden=template_job.act_ga_burden,
            priority=template_job.priority,
            unit_price=order_item.unit_price.dollars if comp.is_root_component else 0,
            total_price=order_item.unit_price.dollars * order_item.quantity if comp.is_root_component else 0,
            price_uofm='ea',
            currency_conv_rate=template_job.currency_conv_rate,
            trade_currency=template_job.trade_currency,
            fixed_rate=template_job.fixed_rate,
            trade_date=today,
            customer_po=order.payment_details.purchase_order_number,
            customer_po_ln=template_job.customer_po_ln,
            quantity_per=1,
            profit_pct=template_job.profit_pct,
            labor_markup_pct=template_job.labor_markup_pct,
            mat_markup_pct=template_job.mat_markup_pct,
            serv_markup_pct=template_job.serv_markup_pct,
            labor_burden_markup_pct=template_job.labor_burden_markup_pct,
            machine_burden_markup_pct=template_job.machine_burden_markup_pct,
            ga_burden_markup_pct=template_job.ga_burden_markup_pct,
            lead_days=order_item.lead_days,
            profit_markup=template_job.profit_markup,
            split_to_job=False,
            note_text=f'{template_job.note_text}\n\n{notes}',
            last_updated=now,
            order_unit='ea',
            price_unit_conv=1,
            source='System',
            plan_modified=False,
            objectid=str(uuid.uuid4()),
            prepaid_amt=0,
            prepaid_tax_amount=0,
            prepaid_trade_amt=0,
            commissionincluded=False,
            ship_via=safe_get(so_header, 'ship_via'),
            top_lvl_job=safe_get(top_level_job, 'job')
        )
        return job

    def create_new_job(
            self, employee: jb.Employee, commission_pct, customer: jb.Customer, so_header: jb.SoHeader, today,
            comp: OrderComponent, desc: str, ext_desc, order_item: OrderItem, order: Order, extras, scrap_pct, notes,
            now, top_level_job: jb.Job, ship_to, contact, i=None
    ):
        user_values = self.create_user_values(order_item, comp, now)
        job = jb.Job(
            sales_rep=employee,
            commission_pct=commission_pct,
            customer=customer,
            ship_to=safe_get(ship_to, 'address'),
            contact=safe_get(contact, 'contact'),
            terms=safe_get(so_header, 'terms', default_value="Net 30 days"),
            sales_code=self._exporter.erp_config.sales_code,
            type='Assembly' if len(comp.child_ids) else 'Regular',
            order_date=today,
            status=self._exporter.erp_config.import_job_as,
            status_date=today,
            part_number=comp.part_number,
            rev=comp.revision,
            description=desc,
            ext_description=ext_desc,
            drawing=comp.part_number,
            build_to_stock=True,
            quote=f'PPQ#{order.quote_number}',
            order_quantity=self._exporter.get_deliver_quantity(comp),
            extra_quantity=extras,
            pick_quantity=0,
            make_quantity=self._exporter.get_make_quantity(comp),
            split_quantity=0,
            completed_quantity=0,
            shipped_quantity=0,
            fg_transfer_qty=0,
            returned_quantity=0,
            in_production_quantity=0,
            assembly_level=0,
            certs_required=False,
            time_and_materials=False,
            open_operations=0,
            scrap_pct=0,
            est_scrap_qty=extras,
            est_rem_hrs=0,
            est_total_hrs=0,
            est_labor=0,
            est_material=0,
            est_service=0,
            est_labor_burden=0,
            est_machine_burden=0,
            est_ga_burden=0,
            act_revenue=0,
            act_scrap_quantity=0,
            act_total_hrs=0,
            act_labor=0,
            act_material=0,
            act_service=0,
            act_labor_burden=0,
            act_machine_burden=0,
            act_ga_burden=0,
            priority=5,
            unit_price=order_item.unit_price.dollars if comp.is_root_component else 0,
            total_price=order_item.unit_price.dollars * order_item.quantity if comp.is_root_component else 0,
            price_uofm='ea',
            currency_conv_rate=1,
            trade_currency=1,
            fixed_rate=True,
            trade_date=today,
            customer_po=order.payment_details.purchase_order_number,
            customer_po_ln=i + 1 if i is not None else None,
            user_values=safe_get(user_values, 'user_values'),
            quantity_per=1,
            profit_pct=0,
            labor_markup_pct=0,
            mat_markup_pct=0,
            serv_markup_pct=0,
            labor_burden_markup_pct=0,
            machine_burden_markup_pct=0,
            ga_burden_markup_pct=0,
            lead_days=order_item.lead_days,
            profit_markup='M',
            prepaid_amt=0,
            split_to_job=False,
            note_text=f'\n\n{notes}',
            last_updated=now,
            order_unit='ea',
            price_unit_conv=1,
            source='System',
            plan_modified=False,
            objectid=str(uuid.uuid4()),
            prepaid_tax_amount=0,
            prepaid_trade_amt=0,
            commissionincluded=False,
            ship_via=safe_get(so_header, 'ship_via'),
            top_lvl_job=safe_get(top_level_job, 'job')
        )
        return job

    def save_job(self, job, comp):
        job.save()

    @staticmethod
    def get_parent_part_number(order_item: OrderItem, comp: OrderComponent):
        parent_part_number = comp.part_number
        for part in order_item.components:
            if part.is_root_component:
                parent_part_number = part.part_number
        return parent_part_number

    def send_job_created_email(self, job):
        logger.info(f'Sending job created email. Job number: {job.job}')
        self._exporter.send_email(subject=self._exporter.erp_config.email_subject,
                                  body=f"JOBBOSS job {job.job} has been created."
                                       f"\n{self._exporter.erp_config.email_body}")

    def _process(self, order: Order, order_item: OrderItem, assm_comp, comp: OrderComponent, so_header,
                 top_level_job: jb.Job, customer, contact, processed_parents, i: int, ship_to, solo_mfg=False,
                 parent_price=0):
        now = make_aware(datetime.datetime.utcnow())
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        suffix_position = self.get_assembly_suffix(assm_comp, processed_parents)
        prefix = self.get_prefix(comp)
        notes, desc, ext_desc = self.process_notes(order_item)
        extras, scrap_pct = self.get_extras(order_item, comp)
        employee, commission_pct = self.get_employee_info(so_header)
        template_job = get_template_job(comp, self._exporter.erp_config)
        matching_part_number_job = get_most_recent_job(comp, self._exporter.erp_config)
        separator = self._exporter.erp_config.assembly_suffix_separator
        parent_part_number = self.get_parent_part_number(order_item, comp)

        if self._exporter.erp_config.template_job_matching_enabled and template_job:
            logger.info(f"Matching template job found: {template_job.job}. Creating new Job from template.")
            job = self.create_job_from_template(
                template_job, employee, commission_pct, customer, so_header,
                today, now, order, order_item, comp, top_level_job, notes
            )
        elif self._exporter.erp_config.part_number_job_matching_enabled and matching_part_number_job:
            logger.info(f"Matched part number: {comp.part_number} with Job: {matching_part_number_job}")
            job = self.create_job_from_template(
                matching_part_number_job, employee, commission_pct, customer, so_header,
                today, now, order, order_item, comp, top_level_job, notes
            )
        else:
            logger.info("Creating standard Job from Paperless Parts order item.")
            job = self.create_new_job(
                employee, commission_pct, customer, so_header, today, comp, desc, ext_desc,
                order_item, order, extras, scrap_pct, notes, now, top_level_job, ship_to, contact, i
            )

        if comp.is_root_component or solo_mfg:
            # Assign proper child component make quantity if job is top-level-mfg comp only
            if solo_mfg:
                job.make_quantity = self._exporter.get_innate_quantity(comp) * order_item.quantity
                job.unit_price = parent_price
                innate_qty = decimal.Decimal(self._exporter.get_innate_quantity(comp))
                job.total_price = decimal.Decimal(parent_price) * innate_qty * decimal.Decimal(order_item.quantity)
                # Assigns part number from top-level-assembly comp instead of mfg. comp if set to True in config options
                if self._exporter.erp_config.assembly_conversion_should_adopt_top_level_part_number and \
                        parent_part_number is not None:
                    job.part_number = parent_part_number
            job.top_lvl_job = job.job
            job.save_with_autonumber(prefix=prefix)
        else:
            job.job = self.generate_custom_job_number(separator, prefix, suffix_position)
            job.assembly_level = assm_comp.level
        try:
            job = trim_django_model(job)
            self.save_job(job, comp)
            logger.info(f'\n\n[{job.job}] - Created job\n')
            self._exporter.success_message = f"Associated JobBOSS job number is {job.job}"
        except Exception as e:
            logger.error(f'Job {job.job} failed to save. [ERROR]: {e}')
        if self._exporter.erp_config.should_email_when_job_created:
            self.send_job_created_email(job)
        return job
