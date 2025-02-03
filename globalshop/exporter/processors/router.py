import decimal

from paperless.objects.orders import OrderComponent, OrderItem, OrderOperation
from typing import Tuple, List

from baseintegration.integration import logger
from globalshop.client import GlobalShopClient
from globalshop.customer import CustomerRecord
from globalshop.exporter.processors import GSProcessor
from globalshop.router import Router
from globalshop.utils import pad_part_num
from baseintegration.utils.data import sqlize_str


class RouterProcessor(GSProcessor):

    def _process(self, item: OrderItem, customer: CustomerRecord = None):
        """
        For each operation in the assembly, create a Labor step
        For each Outside Service in the assembly, create and Outside step
        For each part which is not a purchased component in the assembly,
        create a material step
        """
        for component in item.iterate_assembly():
            # Process the current line passed in
            self.process_part(component.component, customer)

    def process_part(self, order_component: OrderComponent,
                     customer: CustomerRecord = None):
        ops = order_component.shop_operations
        mat_ops = order_component.material_operations
        self.line_num = 0
        ops = self._order_router_lines(ops, mat_ops)
        for op in ops:

            # Check if this is a workgroup or workcenter as stored in the
            # custom table:

            logger.debug(f"Checking if Operation is workcenter/workgroup: "
                         f"{op} ")
            workcenter = self._check_if_labor_line(op)

            logger.debug(f"Is{' NOT' if workcenter is None else ''} "
                         f"workcenter: {op.name}")

            if workcenter:
                self._process_labor_line(op=op,
                                         order_component=order_component,
                                         workcenter=workcenter,
                                         customer=customer
                                         )
                continue

            #     check if it is an outside_service:
            elif op.is_outside_service:
                logger.debug(f'Op is outside service! {op.name}')
                self._process_outside_line(op=op,
                                           order_component=order_component,
                                           customer=customer)
                continue

            elif self._is_comment_code(op=op):
                logger.debug(f'Op is comment! {op.name}')
                self._process_comment_line(op=op,
                                           order_component=order_component,
                                           customer=customer)
            elif op in mat_ops:
                # Add material operations as material lines on the job
                self._process_material_line(mat_op=op,
                                            order_component=order_component,
                                            customer=customer)
            else:
                logger.debug(f'Op is not processed!: {op.name}')

        # For each Router.insert() we called it cached a sql INSERT command.
        # We now want to execute each command in one batch so the whole
        # router is processed together.
        client: GlobalShopClient = GlobalShopClient.get_instance()
        client.execute_cache(commit=True)

        # TODO: config to add purchased parts to routers?

    def _order_router_lines(self, operations: List[OrderOperation],
                            material_operations: List[OrderOperation]
                            ) -> List[OrderOperation]:
        # TODO: MOve to zephyr specific processor
        #  Sort order of router items: ENG > Prog (PG-B,P, M) > PP >
        #  RM> All other ops in order

        eng_ops = []
        prog_b_ops = []
        prog_p_ops = []
        prog_m_ops = []
        others = []
        for op in operations:
            if op.name == 'ENG':
                eng_ops.append(op)
            elif op.name == 'PG-B':
                prog_b_ops.append(op)
            elif op.name == 'PG-P':
                prog_p_ops.append(op)
            elif op.name == 'PG-M':
                prog_m_ops.append(op)
            else:
                others.append(op)

        ops = []
        ops.extend(eng_ops)
        ops.extend(prog_b_ops)
        ops.extend(prog_m_ops)
        ops.extend(material_operations)
        ops.extend(others)
        # This breaks flake!
        # ops = (eng_ops + prog_b_ops + prog_p_ops + prog_m_ops
        #        + material_operations + others)

        return ops

    def _get_next_line_num(self) -> int:
        """
        Get the next router line number. This is optional, and only needed
        if we do need to explicitly set the line number to ensure a sequence.
        """
        # TODO: Account for levels/parts not just sequence
        self.line_num += 1
        return self.line_num

    def _get_sort_code(self, customer: CustomerRecord = None):
        """
        Get the sort code for a given routing line.
        """
        sort_code = None
        if self._exporter.erp_config.use_cust_id_as_sort_code:
            logger.debug(f'erp_config.cust_sort_code: '
                         f'{self._exporter.erp_config.cust_sort_code}')
            debug_cust = customer.gss_customer_number if customer else None
            logger.debug(f'customer.gss_customer_number: '
                         f'{debug_cust}')
            sort_code = customer.gss_customer_number if customer else None
        logger.debug(
            f'use_cust_id_as_sort_code: '
            f'{self._exporter.erp_config.use_cust_id_as_sort_code}')
        logger.debug(f'Sort Code: {sort_code}')
        return sort_code

    def _process_labor_line(self, op: OrderOperation,
                            order_component: OrderComponent,
                            workcenter: str,
                            customer: CustomerRecord = None
                            ):
        """
        Insert Labor Line
        """
        if order_component.part_number is not None:
            part_num = order_component.part_number
        else:
            part_num = order_component.part_name
        part_num = pad_part_num(part_num=part_num)
        part_rev = order_component.revision

        # line_description = op.notes if op.notes else None

        # parts_hour = None
        runtime = op.runtime
        setup = op.setup_time

        product_line = self._get_product_line(order_component)

        # for var in op.costing_variables:
        # if var.label == 'Parts Per Hour':
        #     parts_hour = var.value
        customer_id = customer.gss_customer_number if customer else None
        # line_number = self._get_next_line_num()

        order_component_description_lines = order_component.description.splitlines() if order_component.description is not None else [None]

        line_comments = op.notes

        Router.insert(external_id=part_num, router_number=part_num,
                      product_line=product_line, uom='ea', line_type='L',
                      revision=part_rev,
                      workcenter=workcenter, runtime=runtime,
                      setup=setup,
                      # line_description=line_description,
                      line_cmts=line_comments,
                      router_description=order_component_description_lines[0],
                      customer_id=customer_id
                      )

    def _process_outside_line(self, op: OrderOperation,
                              order_component: OrderComponent,
                              customer: CustomerRecord = None):
        """
        Insert an Outside Service Line
        """
        if order_component.part_number is not None:
            part_num = order_component.part_number
        else:
            part_num = order_component.part_name
        part_num = pad_part_num(part_num=part_num)
        part_rev = order_component.revision

        product_line = self._get_product_line(order_component=order_component)

        outside_vars = self._get_outside_service_vars(op=op)
        project_group = self._get_outside_line_project_group(operation=op)
        customer_id = customer.gss_customer_number if customer else None
        line_description = self._get_outside_line_description(
            operation=op)

        op_code, vendor_code, group_code = outside_vars

        line_comments = op.notes

        order_component_description_lines = order_component.description.splitlines() if order_component.description is not None else [None]

        Router.insert(external_id=part_num, router_number=part_num,
                      revision=part_rev,
                      product_line=product_line,
                      uom='ea', line_type='O',
                      # line_number=self._get_next_line_num(
                      # vendor_id='A1P001', workcenter='WTIG',
                      # TODO: DO we need workcenter as well?
                      vendor_id=vendor_code,
                      outside_code=op_code,
                      line_qty=1,
                      # FIXME: Add LPF powder sort code as project group
                      #  For Zephyr, this is the same value as LPF's sort code
                      # sort_code=
                      # outside_code='A1 PAINT'
                      line_cmts=line_comments,
                      line_description=line_description,
                      project_group=project_group,
                      router_description=order_component_description_lines[0],
                      customer_id=customer_id
                      )

    def _get_outside_line_description(self, operation: OrderOperation) \
            -> str:
        # TODO: MOve to Zephyr specific logic
        if operation.operation_definition_name and operation.operation_definition_name.startswith('LPF'):
            name = operation.get_variable(self._exporter.erp_config.osv_description_var)
            return f" COLOR: {name}"
        else:
            return ""

    def _get_outside_line_project_group(self,
                                        operation: OrderOperation) -> str:
        """
        Get the project group for a provided outside service line
        """

        project_group_var = operation.get_variable_obj(self._exporter.erp_config.project_group_var)
        if project_group_var is not None:
            sort_code = project_group_var.row.get("SORT_CODE") if \
                project_group_var.row else None
            return sort_code

    def _process_comment_line(self, op: OrderOperation,
                              order_component: OrderComponent,
                              customer: CustomerRecord):
        """
        Insert a comment line
        """
        if order_component.part_number is not None:
            part_num = order_component.part_number
        else:
            part_num = order_component.part_name
        part_num = pad_part_num(part_num=part_num)
        part_rev = order_component.revision
        line_comments = op.notes

        customer_id = customer.gss_customer_number if customer else None

        product_line = self._get_product_line(order_component)

        order_component_description_lines = order_component.description.splitlines() if order_component.description is not None else [None]

        Router.insert(external_id=part_num, router_number=part_num,
                      revision=part_rev,
                      product_line=product_line,
                      uom='ea',
                      line_type='C',
                      # line_number=self._get_next_line_num(),
                      op_code=op.name,
                      line_cmts=line_comments,
                      router_description=order_component_description_lines[0],
                      customer_id=customer_id)

    def _process_material_line(self, mat_op: OrderOperation,
                               order_component: OrderComponent,
                               customer: CustomerRecord = None):
        """
        Insert a Material line
        """

        customer_id = customer.gss_customer_number if customer else None
        material = mat_op.get_variable(self._exporter.erp_config.material_id_var)
        material_description = mat_op.get_variable(self._exporter.erp_config.material_desc_var)

        # IF there is no material selected, do not try to add it to the router
        if not material:
            return None

        # Rate is the cost of one base unit of material
        rate = self._get_material_cost(mat_op)

        # Todo - this is probably outdated, GSS has a conversion where we should pass them our runtime, check w/ them
        # Runtime is the percent of base material required to produce one unit:
        #  ex: 1/(Parts per sheet)
        parts_per = self._get_parts_per_base_material(mat_op)
        if parts_per is not None:
            mat_runtime: decimal.Decimal = round(1 / parts_per, ndigits=4)
        if order_component.part_number is not None:
            part_num = order_component.part_number
        else:
            part_num = order_component.part_name
        part_num = pad_part_num(part_num=part_num)
        # part_rev = order_component.revision
        order_component_description_lines = order_component.description.splitlines() if order_component.description is not None else [None]
        # line_comments = op.notes
        product_line = self._get_product_line(order_component)

        Router.insert(external_id=part_num, router_number=part_num,
                      product_line=product_line,
                      uom='ea', line_type='M',
                      # line_number=self._get_next_line_num(),
                      line_description=material_description,
                      material=material,
                      sort_code=self._get_sort_code(customer=customer),
                      router_description=order_component_description_lines[0],
                      customer_id=customer_id,
                      rate=rate,
                      line_qty=mat_runtime
                      )

    def _get_parts_per_base_material(self, mat_op: OrderOperation) -> \
            decimal.Decimal:
        """
        Get the number of parts produced per base material
        Depending on material type, get the value of parts per *
        """

        # Todo - more recent GSS integration will ask for a required quantity var, leaving this here for anything legacy

        parts_per = None

        per_rods = mat_op.get_variable('Parts Per Rod')
        per_sheet = mat_op.get_variable('Parts Per Sheet')
        per_stick = mat_op.get_variable('Parts per Stick')

        if per_rods:
            parts_per = per_rods
        elif per_sheet:
            parts_per = per_sheet
        elif per_stick:
            parts_per = per_stick
        return parts_per

    def _get_material_cost(self, mat_op: OrderOperation):
        """
        Get the cost per base unit of material
        """
        # Todo - more recent GSS integration will ask for a required quantity var, leaving this here for anything legacy

        mat_cost = None

        rod_cost = mat_op.get_variable('Rod Cost')
        sheet_cost = mat_op.get_variable('Cost Per Sheet')
        stick_cost = mat_op.get_variable('Cost per Stick')

        if rod_cost:
            mat_cost = rod_cost
        elif sheet_cost:
            mat_cost = sheet_cost
        elif stick_cost:
            mat_cost = stick_cost
        return mat_cost

    def _get_product_line(self, order_component: OrderComponent):
        """
        Get the product_line value for a given router line based on the order
        component
        """

        # TODO: These need to be parameterized in the future
        # The root component is 'FG', or "Finished Good"
        if order_component.is_root_component:
            product_line = 'FG'
        # If this is a component part, and not a part sold to the customer
        # it is 'FC' or "Finished Component"
        else:
            product_line = 'FC'
        return product_line

    def _check_if_labor_line(self, op: OrderOperation) -> str:
        """
        Check if the provided operation should be considered a Labor line.
        Return the workcenter else None
        """

        is_wg = False
        is_wc = False
        # Select Workgroup:
        wc_name = op.get_variable(self._exporter.erp_config.workcenter_var)
        # Most, but not all workcenters/workgroups have this variable set
        if not wc_name:
            wc_name = op.name
        # if wc_name:
        sql_cmd = f'SELECT MACHINE FROM V_WORKCENTERS WHERE MACHINE = ' \
                  f'{sqlize_str(wc_name)}'
        client: GlobalShopClient = GlobalShopClient.get_instance()
        logger.debug(f'Checking if op is a Workcenter: {sql_cmd}')
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        if row:
            res: str = row[0]
            if isinstance(res, str) and res.strip() == wc_name:
                is_wc = True
                logger.debug("Is Workcenter!")

        if not is_wc:
            wg_name = wc_name
            sql_cmd = f'SELECT WORK_GROUP FROM V_WORKGROUP_HEAD WHERE ' \
                      f'WORK_GROUP = {sqlize_str(wg_name)}'

            logger.debug(f'Checking if op is a Workgroup: {sql_cmd}')
            cursor.execute(sql_cmd)
            row = cursor.fetchone()
            if row:
                res: str = row[0]
                if isinstance(res, str) and res.strip() == wg_name:
                    is_wg = True
                    logger.debug("Is Workgroup!")
        cursor.close()
        return wc_name if is_wc or is_wg else None

    def _get_outside_service_vars(self, op: OrderOperation) -> \
            Tuple[str, str, str]:
        """
        Check if this is an outside service. If yes, then return a tuple with:
            - operation
            - vendor code
            - group code
        """

        op_code: str = None
        vendor_code: str = None
        group_code: str = None

        if op.is_outside_service:
            for var in op.costing_variables:
                if var.label == 'Machine':
                    op_code = var.value
                elif var.label == 'operation':
                    vendor_code = var.value
                elif var.label == 'Powder Name':
                    group_code = var.row.get('SORT_CODE')
        return op_code, vendor_code, group_code

    def _is_comment_code(self, op: OrderOperation) -> bool:
        """
        Check if the provided comment code is a defined comment operation.
        Returns True if present in the V_OP_CODES view and LMO=='C',
        else False
        """
        client = GlobalShopClient.get_instance()
        comment_code = op.name

        # # If this is in a hard coded defined value then instantly return True
        # if comment_code in self._get_hard_coded_comment_codes():
        #     return True

        sql_cmd = f"""SELECT OPERATION FROM V_OP_CODES WHERE LMO='C'
         AND OPERATION = '{comment_code}' """
        cursor = client.cursor()
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        # If we have an exact match then this is a workcenter

        logger.debug(f'Is op {op.name} comment in V_OP_CODES?: '
                     f' {row and row[0].strip() == comment_code}. Result '
                     f'row: {row} ')
        return row and row[0].strip() == comment_code
