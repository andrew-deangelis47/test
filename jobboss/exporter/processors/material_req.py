import datetime
import numbers
import uuid
import jobboss.models as jb
from jobboss.query.job import get_material
from baseintegration.datamigration import logger
from . import JobBossProcessor
from jobboss.query.job import get_template_job, get_most_recent_job
from paperless.objects.orders import OrderComponent, OrderItem, OrderOperation
from baseintegration.utils import safe_get, trim_django_model
from django.utils.timezone import make_aware
from typing import Union


class MaterialReqProcessor(JobBossProcessor):

    @staticmethod
    def get_comp_type(comp: OrderComponent):
        """
        'H' - Hardware, 'R' - Raw Material, 'F' - Finished Good (for customers using POs,
        create Finished Good and link in SoDetail)
        """
        if comp.is_hardware:
            return 'H'
        else:
            return 'R'

    def get_material_name(self, comp, mat_type):
        if mat_type == 'R' and comp.material is not None:
            mat_name = comp.material.name.upper()[0:30]
        elif mat_type == 'H' and comp.part_number:
            mat_name = comp.part_number[0:30]
        else:
            mat_name = str(self._exporter.erp_config.default_hardware_material)
        return mat_name

    @staticmethod
    def get_node_quantity_per(mat_type, assm_comp=None):
        return assm_comp.quantity_per_parent if mat_type == "H" else 1

    @staticmethod
    def get_quantity_per(order_item, comp, mat_type, parts_per_bar_variable=None, mat_op=None):
        if mat_op is None and mat_type == "H":
            for parent_id in comp.parent_ids:
                parent = order_item.get_component(parent_id)
                for child in parent.children:
                    if child.child_id == comp.id:
                        return child.quantity
        elif mat_op and mat_type == "R":
            parts_per_bar = mat_op.get_variable(parts_per_bar_variable)
            if type(parts_per_bar) == str and parts_per_bar.isnumeric():
                parts_per_bar = float(parts_per_bar)
            if parts_per_bar and isinstance(parts_per_bar, numbers.Number):
                return round(parts_per_bar, 4)
        return 1

    def get_mat_name_from_op_variable(self, mat_op: OrderOperation, pp_mat_variable: str, default_mat_name: str):
        """
        Attempts to get a valid JB Material id based off of the value in the pp_mat_variable.
        If a valid material instance exists for the specified ID, the material ID will be returned
        If no material exists for the specified ID, the default will be returned (if use_default_materials=True)
        Else, return a new material ID to be added as a type "M" material in later actions.
        """
        material_id = mat_op.get_variable(pp_mat_variable)
        if material_id and get_material(material_id):
            material_id = get_material(material_id).material
        elif self._exporter.erp_config.use_default_materials:
            material_id = default_mat_name
        if material_id is None:
            material_id = "No Name Specified"
        if mat_op.operation_definition_name is None and material_id is None:
            material_id = "Manual Material"
        return material_id

    @staticmethod
    def get_op_variable_value_or_zero(mat_op: OrderOperation, variable_name: str):
        """
        Returns the specified operation variable value if it exists, else returns 0.
        """
        variable_value = mat_op.get_variable(variable_name)
        if variable_value:
            return variable_value
        return 0

    @staticmethod
    def get_parent_job(assm_comp, processed_parents):
        parent_id = safe_get(assm_comp, 'parent.id')
        parent_data = processed_parents.get(parent_id, None)
        if parent_data:
            job_instance = parent_data.parent_job
            return job_instance
        return None

    def add_finished_good_to_parent(self, comp: OrderComponent, parent_job, order_item: OrderItem, now, today):
        material_id = comp.part_number.strip()[:30]
        mat_type = "F"
        fg_mat_req = self.generate_material_op(material_id, parent_job, order_item, now, today, mat_type)
        logger.info(f"Added Finished Good material {material_id} to parent job {parent_job.job}.")
        return fg_mat_req

    def get_material_master_enforced_fields(self, material_id):
        material_master_attributes_dict: dict = {}
        material_instance = jb.Material.objects.filter(material=material_id).first()
        if material_instance is not None:
            material_master_attributes_dict["uofm"] = safe_get(material_instance, "stocked_uofm", "ea")
            material_master_attributes_dict["cost_uofm"] = safe_get(material_instance, "cost_uofm", "ea")
            material_master_attributes_dict["quantity_per_basis"] = safe_get(
                material_instance, "quantity_per_basis", "I"
            )
            material_master_attributes_dict["type"] = safe_get(material_instance, "type", "H")
        return material_master_attributes_dict

    def generate_material_op(self, material_id, job: jb.Job, order_item, now, today, mat_type="M", qty_per=1,
                             mat_op=None,
                             notes=None, part_length=0, part_width=0, cutoff=0, bar_end=0):
        material_master_attributes_dict = self.get_material_master_enforced_fields(material_id)
        mat = jb.MaterialReq(
            job=job,
            material=material_id,
            description=material_id,
            pick_buy_indicator=self._exporter.erp_config.material_req_default_pick_or_buy,
            type=material_master_attributes_dict.get("type", "H"),
            status='O',
            quantity_per_basis=material_master_attributes_dict.get("quantity_per_basis", "I"),
            quantity_per=qty_per,
            uofm=material_master_attributes_dict.get("uofm", "ea"),
            deferred_qty=self.get_material_op_calculator_quantity(),
            est_qty=self.get_material_op_calculator_quantity(),
            est_unit_cost=self.jb_configured_unit_cost if self.jb_configured_unit_cost > 0 else
            round(mat_op.cost.raw_amount / order_item.quantity, 2) if mat_op else 0,
            est_addl_cost=0,
            est_total_cost=self.get_material_op_total_cost(mat_op),
            act_qty=0,
            act_unit_cost=0,
            act_addl_cost=0,
            act_total_cost=0,
            part_length=part_length,
            part_width=part_width,
            bar_end=bar_end,
            cutoff=cutoff,
            facing=self.facing,
            bar_length=0,
            lead_days=0,
            currency_conv_rate=1,
            trade_currency=1,
            fixed_rate=True,
            trade_date=today,
            certs_required=False,
            manual_link=False,
            last_updated=now,
            note_text=notes,
            cost_uofm=material_master_attributes_dict.get("cost_uofm", "ea"),
            cost_unit_conv=1,
            quantity_multiplier=1,
            partial_res=False,
            objectid=str(uuid.uuid4()),
            job_oid=job.objectid if isinstance(job, jb.Job) else None,
            affects_schedule=False,
            rounded=self.rounded,
            material_oid=None
        )
        try:
            mat = trim_django_model(mat)
            mat.save()
            mat.refresh_from_db()
            logger.info(f"Saved MaterialReq {mat.material} to Job {mat.job.job}")
        except Exception as e:
            logger.error(f'Failed to save MaterialReq: {mat.material} to Job: {mat.job.job}. [ERROR] - {e}')
            logger.error(mat.__dict__)
        return mat

    def generate_material_op_from_template(self, template_job, job, now, today):
        mats = []
        mat_list = jb.MaterialReq.objects.filter(job=template_job.job)
        for mat in mat_list:
            mat_req = jb.MaterialReq(
                job=job,
                material=mat.material,
                note_text=mat.note_text,
                description=mat.description,
                pick_buy_indicator=mat.pick_buy_indicator,
                type=mat.type,
                status='O',
                quantity_per_basis=mat.quantity_per_basis,
                quantity_per=mat.quantity_per,
                uofm=mat.uofm,
                deferred_qty=mat.deferred_qty,
                est_qty=mat.est_qty,
                est_unit_cost=mat.est_unit_cost,
                est_addl_cost=mat.est_addl_cost,
                est_total_cost=mat.est_total_cost,
                act_qty=mat.act_qty,
                act_unit_cost=mat.act_unit_cost,
                act_addl_cost=mat.act_addl_cost,
                act_total_cost=mat.act_total_cost,
                part_length=mat.part_length,
                part_width=mat.part_width,
                bar_end=mat.bar_end,
                cutoff=mat.cutoff,
                facing=mat.facing,
                bar_length=mat.bar_length,
                lead_days=mat.lead_days,
                currency_conv_rate=mat.currency_conv_rate,
                trade_currency=mat.trade_currency,
                fixed_rate=mat.fixed_rate,
                trade_date=today,
                certs_required=mat.certs_required,
                manual_link=mat.manual_link,
                last_updated=now,
                cost_uofm=mat.cost_uofm,
                cost_unit_conv=mat.cost_unit_conv,
                quantity_multiplier=mat.quantity_multiplier,
                partial_res=mat.partial_res,
                objectid=uuid.uuid4(),
                job_oid=job.objectid,
                affects_schedule=mat.affects_schedule,
                rounded=mat.rounded
            )
            try:
                mat_req = trim_django_model(mat_req)
                mat_req.save()
                mat.refresh_from_db()
                logger.info(f"Saved template MaterialReq {mat_req.material} to Job {mat_req.job.job}")
            except Exception as e:
                logger.error(
                    f'Failed to save template MaterialReq: {mat_req.material} to Job: {mat_req.job.job}. [ERROR] - {e}')
                logger.error(mat_req.__dict__)
            mats.append(mat_req)
        return mats

    def get_generic_raw_material_attributes(self):
        op_ignore = self._exporter.erp_config.op_ignore.split(",")
        pp_mat_variable = self._exporter.erp_config.pp_mat_id_variable
        default_mat = self._exporter.erp_config.default_raw_material
        parts_per_bar_variable = self._exporter.erp_config.parts_per_bar_variable
        return op_ignore, pp_mat_variable, default_mat, parts_per_bar_variable

    def get_pp_material_operation_variables(self, mat_op):
        notes = mat_op.notes
        part_length = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.part_length_variable)
        part_width = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.part_width_variable)
        cutoff = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.cutoff_variable)
        bar_end = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.standard_bar_end_variable)
        self.facing = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.facing_variable)
        self.jb_calculator_qty = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.jb_calculator_qty)
        self.rounded = self.is_rounded(mat_op)
        self.jb_configured_unit_cost = self.get_op_variable_value_or_zero(mat_op,
                                                                          self._exporter.erp_config.buy_item_unit_cost)
        return notes, part_length, part_width, cutoff, bar_end

    def is_rounded(self, mat_op):
        is_rounded_string = mat_op.get_variable(self._exporter.erp_config.is_rounded_variable)
        if is_rounded_string == "No":
            return False
        return True

    def get_buy_item_attributes(self, mat_op):
        buy_item_desc = self.create_buy_item_notes(mat_op)
        notes = f"{buy_item_desc}\n{mat_op.notes}"
        part_length = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.part_length_variable)
        part_width = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.part_width_variable)
        cutoff = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.cutoff_variable)
        bar_end = self.get_op_variable_value_or_zero(mat_op, self._exporter.erp_config.standard_bar_end_variable)
        jb_configured_unit_cost = self.get_op_variable_value_or_zero(mat_op,
                                                                     self._exporter.erp_config.buy_item_unit_cost)
        return notes, part_length, part_width, cutoff, bar_end, jb_configured_unit_cost

    def create_buy_item_notes(self, mat_op):
        """Returns P3L assembled description from the operation variable for buy items."""
        description = ''
        for buy_item_desc_var in self._exporter.erp_config.buy_item_description_variables.split(","):
            if mat_op.get_variable(buy_item_desc_var) is not None:
                description += f"{buy_item_desc_var}: {mat_op.get_variable(buy_item_desc_var)}\n"
        return description

    def add_material_as_buy_item(self, material_id, job: jb.Job, order_item, comp: OrderComponent, now, today, qty_per,
                                 mat_op, jb_configured_unit_cost, notes=None):
        """
        This function generates a type="M" material, also known as a buy-item in JobBOSS vernacular. Type="M" materials
        are used when an existing instance of the specified material ID does not exist in the system admin material
        tables (also known as material master, or part master).
        """
        logger.info(f"Adding item {material_id} as buy item.")
        mat = jb.MaterialReq(
            job=job,
            material=material_id,
            description="See notes for details.",
            pick_buy_indicator="B",
            type="M",
            status='O',
            quantity_per_basis='I',  # P - mfg parts/item || I - items per mfg part (hardware)
            quantity_per=qty_per,  # If type="H" item, qty_per=child qty. If type="R", qty_per=parts_per_bar config
            uofm='ea',
            deferred_qty=round(self._exporter.get_make_quantity(comp) / qty_per, 2),  # Needs to match est_qty
            est_qty=round(self._exporter.get_make_quantity(comp) / qty_per, 2),  # This is JB logic. Paperless rounds to ceil(req qty).
            est_unit_cost=jb_configured_unit_cost,
            est_addl_cost=0,
            est_total_cost=self.get_material_op_total_cost(mat_op),
            act_qty=0,
            act_unit_cost=0,
            act_addl_cost=0,
            act_total_cost=0,
            lead_days=0,
            currency_conv_rate=1,
            trade_currency=1,
            fixed_rate=True,
            trade_date=today,
            certs_required=False,
            manual_link=False,
            last_updated=now,
            note_text=notes,
            cost_uofm='ea',
            cost_unit_conv=1,
            quantity_multiplier=1,
            partial_res=False,
            objectid=str(uuid.uuid4()),
            job_oid=job.objectid if isinstance(job, jb.Job) else None,
            affects_schedule=False,
            rounded=True,
            material_oid=None
        )
        try:
            mat = trim_django_model(mat)
            mat.save()
            mat.refresh_from_db()
            logger.info(f"Saved MaterialReq {mat.material} to Job {mat.job.job}")
        except Exception as e:
            logger.error(f'Failed to save MaterialReq: {mat.material} to Job: {mat.job.job}. [ERROR] - {e}')
            logger.error(mat.__dict__)
        return mat

    @staticmethod
    def should_generate_buy_item(material_id):
        """Check if material id exists in system admin to determine how to add the material to the job."""
        material_master = jb.Material.objects.filter(material=material_id).first()
        if material_master is None:
            return True
        return False

    def add_raw_materials_from_paperless_operations(self, order_item: OrderItem, comp: OrderComponent, job: jb.Job,
                                                    mat_type, now, today):
        # Check if operations are present for additional processing:
        if not len(comp.material_operations) > 0:
            logger.info(f"No material operations present. No Material added to Job {job.job} ")
            return None

        op_ignore, pp_mat_variable, default_mat, parts_per_bar_variable = self.get_generic_raw_material_attributes()
        for mat_op in comp.material_operations:
            if mat_op.operation_definition_name in op_ignore:
                continue
            self.add_material(order_item, comp, job, now, today, mat_type, parts_per_bar_variable, mat_op,
                              pp_mat_variable, default_mat)

    def add_material(self, order_item, comp, job, now, today, mat_type, parts_per_bar_variable, mat_op,
                     pp_mat_variable, default_mat):
        # Get all attributes from material operation needed to generate MaterialReq
        material_id = self.get_mat_name_from_op_variable(mat_op, pp_mat_variable, default_mat)
        qty_per = self.get_quantity_per(order_item, comp, mat_type, parts_per_bar_variable, mat_op)

        # Determine if material should be buy item or standard required material item
        if self.should_generate_buy_item(material_id):
            notes, part_length, part_width, cutoff, bar_end, jb_configured_unit_cost = \
                self.get_buy_item_attributes(mat_op)
            self.add_material_as_buy_item(material_id, job, order_item, comp, now, today, qty_per, mat_op,
                                          jb_configured_unit_cost, notes)
        else:
            notes, part_length, part_width, cutoff, bar_end = self.get_pp_material_operation_variables(mat_op)
            self.generate_material_op(material_id, job, order_item, now, today, mat_type, qty_per, mat_op,
                                      notes, part_length, part_width, cutoff, bar_end)

    def add_hardware_materials(self, order_item: OrderItem, comp: OrderComponent, job: jb.Job, top_level_job,
                               parent_job, mat_type, now, today, qty_per):
        # If hardware should only exist at the top level, pass the top level job into the MaterialReq
        if self._exporter.erp_config.hardware_is_top_level_only and top_level_job is not None:
            job = top_level_job
        # Hardware should be assigned to its parent if a parent exists, else the current component/job.
        elif parent_job is not None:
            job = parent_job
        material_id = self.get_material_name(comp, mat_type)
        if material_id is not None:
            hardware_material = self.generate_material_op(material_id, job, order_item, now, today, mat_type, qty_per)
            self.assign_hardware_quantities_and_cost(comp, hardware_material)

    def assign_hardware_quantities_and_cost(self, comp: OrderComponent, hardware_material: jb.MaterialReq):
        """
        Takes the purchased component OrderComponent and the hardware material MaterialReq and updates costing/pricing
        attributes on the record under the assumption that hardware is priced as "hardware items required per part".
        NOTE: The pricing assigned here is from the Purchased Component Piece Price in paperless.
        """
        hardware_material.quantity_per_basis = "I"  # I = Hardware items per part
        hardware_material.quantity_per = self.get_relative_quantity(comp)
        hardware_material.deferred_qty = self.get_purchased_component_quantity_from_material_op(comp)
        hardware_material.est_qty = self.get_purchased_component_quantity_from_material_op(comp)
        hardware_material.est_unit_cost = round(float(comp.purchased_component.piece_price.raw_amount), 2)
        hardware_material.est_total_cost = round(
            float(comp.purchased_component.piece_price.raw_amount) * self._exporter.get_deliver_quantity(comp), 2
        )
        hardware_material.save()
        hardware_material.refresh_from_db()

    def get_purchased_component_quantity_from_material_op(self, comp: OrderComponent) -> Union[int, float]:
        """
        - Assumes that the first operation on a PC is the standard "PC Piece Price" operation
        - If this operation does not exist, then the make quantity will be assigned by default
        """
        pc_operation = None
        if comp.material_operations and comp.material_operations[0]:
            pc_operation = comp.material_operations[0]
        if comp.shop_operations and comp.shop_operations[0]:
            pc_operation = comp.shop_operations[0]
        if pc_operation:
            pc_op_quantity = pc_operation.get_variable("integration_quantity")
            if pc_op_quantity:
                return pc_op_quantity
        return self._exporter.get_make_quantity(comp)

    def get_material_op_calculator_quantity(self):
        return self._exporter.get_value_relative_to_current_node(self.jb_calculator_qty)

    def get_material_op_total_cost(self, mat_op):
        total_cost = mat_op.cost.raw_amount if mat_op else 0
        return self._exporter.get_value_relative_to_current_node(total_cost)

    def get_relative_quantity(self, comp: OrderComponent) -> int:
        """
        - JB does quantity_per_parent, the child qtys are not relative to the root component like paperless.
        - We need to get the relative quantity from the parent component's innate_qty.
        - Relative = innate_qty / parent_innate_qty
        """
        if self._exporter.erp_config.should_export_assemblies_with_duplicate_components:
            return self._exporter.get_current_quantity_per_parent()
        else:
            if self.parent_component is not None:
                parent_innate_qty = self.parent_component.innate_quantity
                return int(comp.innate_quantity / parent_innate_qty)
            return comp.innate_quantity

    def _process(self, order_item: OrderItem, assm_comp, comp: OrderComponent, job, top_level_job, processed_parents):
        now = make_aware(datetime.datetime.utcnow())
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        mat_type = self.get_comp_type(comp)
        parts_per_bar_variable = self._exporter.erp_config.parts_per_bar_variable
        if self._exporter.erp_config.should_export_assemblies_with_duplicate_components:
            qty_per = self.get_node_quantity_per(mat_type, assm_comp)
        else:
            qty_per = self.get_quantity_per(order_item, comp, mat_type, parts_per_bar_variable)
        template_job = get_template_job(comp, self._exporter.erp_config)
        matching_part_number_job = get_most_recent_job(comp, self._exporter.erp_config)
        self.parent_component: OrderComponent = assm_comp.parent

        # Determine if component has a parent - adds the FG material to the parent, if config option enabled
        parent_job = self.get_parent_job(assm_comp, processed_parents)
        if self._exporter.erp_config.generate_finished_good_material and \
                self._exporter.erp_config.should_assign_fg_to_parent and comp.type == "manufactured":
            if parent_job is not None:
                self.add_finished_good_to_parent(comp, parent_job, order_item, now, today)
            else:
                parent_job = job
                self.add_finished_good_to_parent(comp, parent_job, order_item, now, today)

        # If template job matching is enabled, all materials will be copied from the template job
        if template_job and self._exporter.erp_config.template_job_matching_enabled:
            logger.info(f"Copying MaterialReqs from Job: {template_job.job} to Job: {job.job}")
            return self.generate_material_op_from_template(template_job, job, now, today)

        # If part number job matching is enabled, all materials will be copied from the matched job
        elif self._exporter.erp_config.part_number_job_matching_enabled and matching_part_number_job:
            logger.info(f"Copying MaterialReqs from Job: {matching_part_number_job.job} to Job: {job.job}")
            return self.generate_material_op_from_template(matching_part_number_job, job, now, today)

        # Else, create material operations from Paperless Parts data
        else:
            # Iterate the material operations in PP if enabled by config and if mat ops exist, else do nothing
            if self._exporter.erp_config.generate_material_ops and mat_type == "R":
                self.add_raw_materials_from_paperless_operations(order_item, comp, job, mat_type, now, today)

            # Create hardware MaterialReqs and associate them to the parent job or current job
            if mat_type == "H":
                self.add_hardware_materials(order_item, comp, job, top_level_job, parent_job, mat_type, now, today,
                                            qty_per)
