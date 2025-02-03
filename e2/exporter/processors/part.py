import os
from datetime import datetime
from typing import Optional
from baseintegration.utils import safe_get

import e2.models as e2
from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger
from e2.utils.utils import PartData, JobRequirementData, normalize_string_characters


class PartProcessor(E2Processor):
    do_rollback = False

    def get_type(self, component):
        """ Return one of {'assembled', 'manufactured', 'purchased', None} """
        if component.type == 'assembled':
            return 'assembled'
        elif component.type == 'manufactured':
            return 'manufactured'
        elif component.type == 'purchased':
            return 'purchased'
        else:
            return None

    @staticmethod
    def get_part_number(component):
        # The Estim PartNo field has a max length of 50
        part_number = component.part_number.upper()[:50] if component.part_number is not None else None
        if part_number is None:
            part_name = component.part_name[:50]
            part_number, ext = os.path.splitext(part_name)
        return part_number

    def get_revision(self, component):
        # The Estim Revision field has a max length of 30
        return component.revision.upper()[:30] if component.revision is not None else None

    def get_raw_material_part_number(self, component):
        raw_material_part_number = None
        if component.material_operations:
            material_op = component.material_operations[0]
            raw_material_part_number_variable_name = self._exporter.erp_config.raw_material_part_number_variable_name
            raw_material_part_number = material_op.get_variable(raw_material_part_number_variable_name)
        if raw_material_part_number is None or not raw_material_part_number:
            raw_material_part_number = 'NO_MATERIAL_ASSIGNED'
        else:
            # The Estim PartNo field has a max length of 50
            raw_material_part_number = raw_material_part_number[:50]
        return raw_material_part_number

    def get_raw_material_revision(self, component):
        return None

    def get_raw_material_quantity(self, component):
        return 1.

    def get_description(self, component, order_item):
        return component.description

    def get_prod_code(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 ProdCode. """
        return None

    def get_raw_material_prod_code(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 ProdCode. """
        return None

    def get_gl_code(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 GL Code. """
        return None

    def get_raw_material_gl_code(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 GL Code. """
        return None

    def get_routed_by_employee(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 routeempl. """
        return self._exporter.erp_config.default_routed_by_employee

    def get_raw_material_routed_by_employee(self, component, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
                    in Paperless we'll need to map to E2 routeempl. """
        return None

    def get_comments(self, component, order_item):
        return None

    def get_calc_method(self, component_type):
        calc_method = '2' if component_type == 'purchased' else '1'
        return calc_method

    def update_part_revision(self, part, revision):
        logger.info(f'Updating revision for part {part.partno} to rev {revision}')
        part.revision = revision
        part.save()
        return part

    def update_part_description(self, part: e2.Estim, description: Optional[str], comments: Optional[str]):
        logger.info(f'Updating description for part {part.partno}')
        part.descrip = description
        part.comments = comments
        part.save()
        return part

    def update_part_quantity_and_price(self, part, component, order_item):
        quantity = self.get_quantity(component, order_item)
        price = self.get_price(component, order_item)

        part.qty1 = quantity
        part.price1 = price
        part.lockprice = 'Y'
        part.save()
        return part

    def update_part_routed_date(self, part: e2.Estim):
        now = datetime.now()
        routed_date = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        part.routedate = routed_date
        part.save()
        return part

    def update_purchased_component_data(self, part, component, is_part_new):
        purchased_component = component.purchased_component
        should_update_purchased_component_data = \
            (self._exporter.erp_config.should_update_e2_purchased_components_data or is_part_new) \
            and purchased_component is not None
        if should_update_purchased_component_data:
            part.descrip = purchased_component.description
            part.save()

            part = self.update_purchased_component_from_user_defined_fields(part, purchased_component)
        return part

    def update_purchased_component_from_user_defined_fields(self, part, purchased_component):
        vendor_code = purchased_component.get_property('vendor')
        part.vendcode1 = vendor_code[:12] if vendor_code is not None else \
            self._exporter.erp_config.default_vendor_code_name
        part.vendcode2 = ''
        part.vendcode3 = ''  # Note - in the database it looks like any time one is set the others are set to '', not Null
        part.save()
        return part

    def _process(self, component, order_item, order, order_header: e2.Order, customer: e2.CustomerCode,
                 assembly_processor):
        component_type = self.get_type(component)

        part_number = self.get_part_number(component)
        revision = self.get_revision(component)
        description = self.get_description(component, order_item)
        prod_code_name = self.get_prod_code(component, order_item, order)
        gl_code = self.get_gl_code(component, order_item, order)
        comments = self.get_comments(component, order_item)
        calc_method = self.get_calc_method(component_type)
        routed_by_employee = self.get_routed_by_employee(component, order_item, order)
        vend_code = None  # Note - for purchased components, vend code should be set via update_purchased_component_data
        uom = 'EA'
        billing_rate = self.get_billing_rate(component, order_item, order)

        # Get or create part
        part, is_part_new = self.get_or_create_part(calc_method, comments, customer, description, gl_code, order_header,
                                                    part_number, prod_code_name, revision, routed_by_employee,
                                                    vend_code, uom, billing_rate)

        # Optionally, update the revision on the part to reflect what was entered in Paperless Parts
        if self._exporter.erp_config.should_update_e2_part_revision:
            part = self.update_part_revision(part, revision)

        # Optionally, update the part description to reflect what was entered in Paperless Parts
        if self._exporter.erp_config.should_update_e2_part_description:
            part = self.update_part_description(part, description, comments)

        # Optionally, update the price and quantity on the part
        if is_part_new or self._exporter.erp_config.should_update_e2_part_quantity_and_price:
            part = self.update_part_quantity_and_price(part, component, order_item)

        # Optionally, update the routed date on the part
        if self._exporter.erp_config.should_replace_e2_routing_for_existing_parts:
            part = self.update_part_routed_date(part)

        # If this is a purchased component, bring the additional purchased component information over from Paperless
        if component_type == 'purchased':
            part = self.update_purchased_component_data(part, component, is_part_new)

        # Optionally, clear any existing Materials records where this part is the parent. If this config option is set,
        # we need to completely rebuild the BOM based on what is on the Paperless Parts order
        if self.should_remove_existing_e2_assembly_links():
            assembly_processor.clear_existing_materials_records(part_number)

        # TODO - move this to _post_process
        # TODO - also note that this may all go away once we start including raw materials as explicit components in the tree in Paperless Parts
        # If this is a manufactured component, we also need to create an Estim record for the raw material
        job_requirement = None
        job_requirement_list = []
        if (component_type == 'manufactured' and self._exporter.erp_config.should_create_e2_raw_material_record) or\
                self._exporter.erp_config.should_use_new_multiple_material_logic:
            customer = None
            # Because of legacy custom processors, we cannot just change the old code, we need a config option
            if self._exporter.erp_config.should_use_new_multiple_material_logic:
                for material_op in component.material_operations:
                    raw_material, is_raw_material_new = self.new_get_or_create_raw_material(component, material_op, customer, order_item,
                                                                                            order, order_header)
                    if raw_material is not None:
                        raw_material_quantity = self.new_get_raw_material_quantity(component, material_op)
                        is_purchased = True
                        assembly_processor.run(part, raw_material, raw_material_quantity, is_part_new, is_purchased)
                        job_requirement_list.append(JobRequirementData(
                            outside_service_routing_line=None,
                            purchased_component=None,
                            purchased_component_part_record=None,
                            raw_material_part_record=raw_material,
                            raw_material_quantity=raw_material_quantity,
                        ))

            else:
                raw_material, is_raw_material_new = self.get_or_create_raw_material(component, customer, order_item, order, order_header)
                # If no valid raw material part number is supplied in Paperless Parts, suppress the creation of an assembly
                # link and a job requirement for the placeholder raw material. Note that the only way for raw_material to be
                # None is if the get_raw_material_part_number method is overridden to allow it, otherwise a default part
                # number is used
                if raw_material is not None:
                    raw_material_quantity = self.get_raw_material_quantity(component)
                    is_purchased = True
                    # TODO - note that running the AssemblyProcessor this way means we're bypassing the rollback functionality, among other things potentially
                    # TODO - once raw materials are treated as explicit components in the tree, we'll be able to create linkages to raw materials just like we do for any other components
                    assembly_processor.run(part, raw_material, raw_material_quantity, is_part_new, is_purchased)
                    job_requirement = JobRequirementData(
                        outside_service_routing_line=None,
                        purchased_component=None,
                        purchased_component_part_record=None,
                        raw_material_part_record=raw_material,
                        raw_material_quantity=raw_material_quantity,
                    )

        part_data = PartData(part=part, is_part_new=is_part_new, job_requirement=job_requirement,
                             job_requirement_list=job_requirement_list)
        return part_data

    def get_price(self, component, order_item):
        price = 0.
        if component.is_root_component:
            price = order_item.unit_price.dollars  # The price fields on the estimate are UNIT prices, not extended
        return price

    def get_quantity(self, component, order_item):
        quantity = 1
        if component.is_root_component:
            if self._exporter.erp_config.should_use_extended_part_quantity_and_price:
                quantity = order_item.quantity
        return quantity

    def get_billing_rate(self, component, order_item, order):
        billing_rate = 1
        return billing_rate

    def should_remove_existing_e2_assembly_links(self):
        should_remove_existing_assembly_links = False
        if self._exporter.erp_config.should_replace_e2_bom_for_existing_parts:
            should_remove_existing_assembly_links = True
        return should_remove_existing_assembly_links

    def get_or_create_part(self, calc_method, comments, customer, description, gl_code, order_header, part_number,
                           prod_code_name, revision, routed_by_employee, vend_code, uom, billing_rate):
        is_part_new = False
        part = e2.Estim.objects.filter(partno=normalize_string_characters(str(part_number))).first()
        if part is not None:
            logger.info(f'Found existing Estim record for part number {part_number}, with revision {part.revision}')
        else:
            logger.info(f'Did not find existing Estim record for part number {part_number}. Creating new record.')
            part = self.create_part(calc_method, comments, customer, description, gl_code, order_header, part_number,
                                    prod_code_name, revision, routed_by_employee, vend_code, uom, billing_rate)
            is_part_new = True

        estim_rpt = e2.Estimrpt.objects.filter(partno=normalize_string_characters(str(part_number))).first()
        if estim_rpt is None:
            self.create_estim_rpt_record(part_number)

        return part, is_part_new

    def get_or_create_raw_material(self, component, customer, order_item, order, order_header):
        calc_method = self.get_calc_method('purchased')
        comments = None
        description = None
        gl_code = self.get_raw_material_gl_code(component, order_item, order)
        part_number = self.get_raw_material_part_number(component)
        prod_code_name = self.get_raw_material_prod_code(component, order_item, order)
        revision = self.get_raw_material_revision(component)
        routed_by_employee = self.get_raw_material_routed_by_employee(component, order_item, order)
        vend_code = self.get_raw_material_vend_code(component, order_item, order)
        uom = self.get_raw_material_uom(component)
        billing_rate = self.get_raw_material_billing_rate(component, order_item, order)

        if part_number is None:  # The only way for this to be None is if get_raw_material_part_number is overridden
            return None, False

        raw_material, is_raw_material_new = self.get_or_create_part(calc_method, comments, customer, description,
                                                                    gl_code, order_header, part_number, prod_code_name,
                                                                    revision, routed_by_employee, vend_code, uom,
                                                                    billing_rate)
        return raw_material, is_raw_material_new

    def get_raw_material_billing_rate(self, component, order_item, order):
        billing_rate = 1
        return billing_rate

    def get_raw_material_uom(self, component):
        return 'EA'

    def get_raw_material_vend_code(self, component, order_item, order):
        raw_material_vend_code = None
        if component.material_operations:
            material_op = component.material_operations[0]
            raw_material_row_lookup_variable_name = self._exporter.erp_config.raw_material_row_lookup_variable_name
            material_lookup_var = material_op.get_variable_obj(raw_material_row_lookup_variable_name)
            if material_lookup_var is not None:
                material_row = material_lookup_var.row
                raw_material_vend_code = material_row.get('VendCode1')
        if raw_material_vend_code is None or not raw_material_vend_code:
            raw_material_vend_code = self._exporter.erp_config.default_vendor_code_name
        return raw_material_vend_code

    def create_part(self, calc_method, comments, customer, description, gl_code, order_header, part_number,
                    prod_code_name, revision, routed_by_employee, vend_code, uom, billing_rate):
        cust_code = safe_get(customer, 'customer_code')
        part = e2.Estim.objects.create(
            partno=part_number,
            descrip=description,  # This is the description field
            altpartno=None,
            prodcode=prod_code_name,
            glcode=gl_code,
            entby=order_header.ent_by,
            entdate=order_header.date_ent,
            pricingunit=uom,
            qty1=1,
            price1=0.,
            qty2=None,
            price2=0.0,
            qty3=None,
            price3=0.0,
            qty4=None,
            price4=0.0,
            qty5=None,
            price5=0.0,
            qty6=None,
            price6=0.0,
            qty7=None,
            price7=0.0,
            qty8=None,
            price8=0.0,
            lastpricechg=None,
            custcode=cust_code,
            billingrate=billing_rate,
            revision=revision,
            revdate=None,
            drawnum=None,
            partwt=None,
            commpct=0.,
            miscchg=None,
            miscdescrip='',
            routeempl=routed_by_employee,
            routedate=order_header.date_ent,
            drawingfilename=None,
            globalmarkuppct=None,
            ljno=None,
            ljqty=None,
            ljdatefin=None,
            ljprice=None,
            ljquoteno=None,
            ljdate=None,
            qtyip=None,
            lastdelticketno=None,
            lastdelticketdate=None,
            lastdelticketqty=None,
            comments=comments,
            stockunit=uom,
            qtyonhand=None,
            reordlevel=None,
            reordqty=None,
            qtyonres=None,
            lrno=None,
            lrdate=None,
            lrqty=None,
            binloc1=None,
            binqty1=None,
            binloc2=None,
            binqty2=None,
            binloc3=None,
            binqty3=None,
            binloc4=None,
            binqty4=None,
            binloc5=None,
            binqty5=None,
            vendcode1=vend_code,
            vendcode2=None,
            vendcode3=None,
            leadtime=None,
            purchunit=uom,
            purchfactor=1.0,
            markuppct=None,
            pqty1=None,
            pcost1=0.0,
            pqty2=None,
            pcost2=0.0,
            pqty3=None,
            pcost3=0.0,
            pqty4=None,
            pcost4=0.0,
            pqty5=None,
            pcost5=0.0,
            pqty6=None,
            pcost6=0.0,
            pqty7=None,
            pcost7=0.0,
            pqty8=None,
            pcost8=0.0,
            stockingcost=None,
            lpono=None,
            lpodate=None,
            lpoqty=None,
            lpocost=None,
            qtyonorder=None,
            qtyoutside=None,
            markup1=0.0,
            markup2=0.0,
            markup3=0.0,
            markup4=0.0,
            markup5=0.0,
            markup6=0.0,
            markup7=0.0,
            markup8=0.0,
            lockprice='Y',  # this needs to be 'Y'
            calcmethod=calc_method,
            printed='N',
            purchglcode=None,
            bin1lot=None,
            bin2lot=None,
            bin3lot=None,
            bin4lot=None,
            bin5lot=None,
            active='Y',
            defaultbinloc=None,
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
            matchqtybreaks='Y',
            allow_decimal_inventory=None,
            allow_decimal_purchasing=None,
            automatically_fill_requirements=None,
            automatically_use_partial_records=None,
            automatically_combine_partial_records=None,
            inspect_orders=None,
            inspect_customer_returns=None,
            inspect_receivers=None,
            inspect_internal_rejections=None,
            using_time_tickets=None,
            stocking_unit_new=None,
            stocking_purchasing_factor_new=None,
            purchasing_unit_new=None,
            purchasing_purchasing_factor_new=None,
            part_weight_new=None,
            saved_by_utility=None,
            new_purchasing_factor=None,
            convert_me=None,
        )
        return part

    def create_estim_rpt_record(self, part_number):
        e2.Estimrpt.objects.create(
            partno=part_number,
            startqty1=1,
            quoteqty1=1,
            psetup1=0.0,
            pcycle1=0.0,
            pmaterial1=0.0,
            poutside1=0.0,
            pcomm1=0.0,
            price1=0.0,
            clabor1=0.0,
            cburden1=0.0,
            cmaterial1=0.0,
            coutside1=0.0,
            ccomm1=0.0,
            cost1=0.0,
            totjobtime1=0.0,
            avghourly1=0.0,
            startqty2=0,
            quoteqty2=0,
            psetup2=0.0,
            pcycle2=0.0,
            pmaterial2=0.0,
            poutside2=0.0,
            pcomm2=0.0,
            price2=0.0,
            clabor2=0.0,
            cburden2=0.0,
            cmaterial2=0.0,
            coutside2=0.0,
            ccomm2=0.0,
            cost2=0.0,
            totjobtime2=0.0,
            avghourly2=0.0,
            startqty3=0,
            quoteqty3=0,
            psetup3=0.0,
            pcycle3=0.0,
            pmaterial3=0.0,
            poutside3=0.0,
            pcomm3=0.0,
            price3=0.0,
            clabor3=0.0,
            cburden3=0.0,
            cmaterial3=0.0,
            coutside3=0.0,
            ccomm3=0.0,
            cost3=0.0,
            totjobtime3=0.0,
            avghourly3=0.0,
            startqty4=0,
            quoteqty4=0,
            psetup4=0.0,
            pcycle4=0.0,
            pmaterial4=0.0,
            poutside4=0.0,
            pcomm4=0.0,
            price4=0.0,
            clabor4=0.0,
            cburden4=0.0,
            cmaterial4=0.0,
            coutside4=0.0,
            ccomm4=0.0,
            cost4=0.0,
            totjobtime4=0.0,
            avghourly4=0.0,
            startqty5=0,
            quoteqty5=0,
            psetup5=0.0,
            pcycle5=0.0,
            pmaterial5=0.0,
            poutside5=0.0,
            pcomm5=0.0,
            price5=0.0,
            clabor5=0.0,
            cburden5=0.0,
            cmaterial5=0.0,
            coutside5=0.0,
            ccomm5=0.0,
            cost5=0.0,
            totjobtime5=0.0,
            avghourly5=0.0,
            startqty6=0,
            quoteqty6=0,
            psetup6=0.0,
            pcycle6=0.0,
            pmaterial6=0.0,
            poutside6=0.0,
            pcomm6=0.0,
            price6=0.0,
            clabor6=0.0,
            cburden6=0.0,
            cmaterial6=0.0,
            coutside6=0.0,
            ccomm6=0.0,
            cost6=0.0,
            totjobtime6=0.0,
            avghourly6=0.0,
            startqty7=0,
            quoteqty7=0,
            psetup7=0.0,
            pcycle7=0.0,
            pmaterial7=0.0,
            poutside7=0.0,
            pcomm7=0.0,
            price7=0.0,
            clabor7=0.0,
            cburden7=0.0,
            cmaterial7=0.0,
            coutside7=0.0,
            ccomm7=0.0,
            cost7=0.0,
            totjobtime7=0.0,
            avghourly7=0.0,
            startqty8=0,
            quoteqty8=0,
            psetup8=0.0,
            pcycle8=0.0,
            pmaterial8=0.0,
            poutside8=0.0,
            pcomm8=0.0,
            price8=0.0,
            clabor8=0.0,
            cburden8=0.0,
            cmaterial8=0.0,
            coutside8=0.0,
            ccomm8=0.0,
            cost8=0.0,
            totjobtime8=0.0,
            avghourly8=0.0
        )

    # In order to ensure backwards compatibility we need to create new versions of all raw material related functions
    def new_get_or_create_raw_material(self, component, material_op, customer, order_item, order, order_header):
        calc_method = self.get_calc_method('purchased')
        comments = None
        description = None
        gl_code = self.new_get_raw_material_gl_code(component, material_op, order_item, order)
        part_number = self.new_get_raw_material_part_number(component, material_op)
        prod_code_name = self.new_get_raw_material_prod_code(component, material_op, order_item, order)
        revision = self.new_get_raw_material_revision(component, material_op)
        routed_by_employee = self.new_get_raw_material_routed_by_employee(component, material_op, order_item, order)
        vend_code = self.new_get_raw_material_vend_code(component, material_op, order_item, order)
        uom = self.new_get_raw_material_uom(component, material_op)
        billing_rate = self.new_get_raw_material_billing_rate(component, material_op, order_item, order)

        if part_number is None:  # The only way for this to be None is if new_get_raw_material_part_number is overridden
            return None, False

        raw_material, is_raw_material_new = self.get_or_create_part(calc_method, comments, customer, description,
                                                                    gl_code, order_header, part_number, prod_code_name,
                                                                    revision, routed_by_employee, vend_code, uom,
                                                                    billing_rate)
        return raw_material, is_raw_material_new

    def new_get_raw_material_quantity(self, component, material_op):
        material_op_quantity_required_var = self._exporter.erp_config.material_op_quantity_required_var
        raw_material_quantity = material_op.get_variable(material_op_quantity_required_var)
        return raw_material_quantity or 1.

    def new_get_raw_material_gl_code(self, component, material_op, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 GL Code. """
        return None

    def new_get_raw_material_part_number(self, component, material_op):
        raw_material_part_number_variable_name = self._exporter.erp_config.raw_material_part_number_variable_name
        raw_material_part_number = material_op.get_variable(raw_material_part_number_variable_name)
        if raw_material_part_number is None or not raw_material_part_number:
            raw_material_part_number = 'NO_MATERIAL_ASSIGNED'
        else:
            # The Estim PartNo field has a max length of 50
            raw_material_part_number = raw_material_part_number[:50]
        return raw_material_part_number

    def new_get_raw_material_prod_code(self, component, material_op, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to E2 ProdCode. """
        material_op_prod_code_var = self._exporter.erp_config.material_op_prod_code_var
        material_default_prod_code = self._exporter.erp_config.material_default_prod_code
        raw_material_prod_code = material_op.get_variable(material_op_prod_code_var)
        return raw_material_prod_code or material_default_prod_code

    def new_get_raw_material_revision(self, component, material_op):
        return None

    def new_get_raw_material_routed_by_employee(self, component, material_op, order_item, order):
        """ Take component, order_item, and order as arguments because it's not clear what information
                    in Paperless we'll need to map to E2 routeempl. """
        return None

    def new_get_raw_material_vend_code(self, component, material_op, order_item, order):
        raw_material_vend_code = None
        raw_material_row_lookup_variable_name = self._exporter.erp_config.raw_material_row_lookup_variable_name
        material_lookup_var = material_op.get_variable_obj(raw_material_row_lookup_variable_name)
        if material_lookup_var is not None:
            material_row = material_lookup_var.row
            raw_material_vend_code = material_row.get('VendCode1')
        if raw_material_vend_code is None or not raw_material_vend_code:
            raw_material_vend_code = self._exporter.erp_config.default_vendor_code_name
        return raw_material_vend_code

    def new_get_raw_material_uom(self, component, material_op):
        material_op_uom_var = self._exporter.erp_config.material_op_uom_var
        material_default_uom = self._exporter.erp_config.material_default_uom
        raw_material_uom = material_op.get_variable(material_op_uom_var)
        return raw_material_uom or material_default_uom

    def new_get_raw_material_billing_rate(self, component, material_op, order_item, order):
        billing_rate = 1
        return billing_rate
