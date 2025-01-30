from e2.exporter.processors.routing import RoutingProcessor
from baseintegration.datamigration import logger
from e2.models import Workcntr, Opercode, Routing, Vendcode


class E2ShopSystemRoutingProcessor(RoutingProcessor):

    def create_routing_line_from_inside_operation(self, part, operation, step_number, component):
        work_center_short_name, is_default_work_center_name = self.get_work_center_name(operation)

        default_work_center = self.get_or_create_default_work_center()

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

        descrip = self.get_inside_operation_description(is_default_work_center_name, operation)

        # Get the Estim record
        estim = part
        part_number = part.partno

        # Create the Routing record
        setup_time = operation.setup_time if operation.setup_time is not None else 0.
        setup_time = self._exporter.get_value_relative_to_current_node(setup_time)
        setup_rate = work_center.setup1 if work_center.setup1 is not None else 0.
        setup_price = setup_time * setup_rate  # TODO - should we fill this out if we're just using the operation.cost for the total field?
        runtime = operation.runtime if operation.runtime is not None else 0.
        cycle_rate = work_center.cycle1 if work_center.cycle1 is not None else 0.
        cycle_price = runtime * cycle_rate  # TODO - should we fill this out if we're just using the operation.cost for the total field?
        work_or_vend = 0

        display_setup_time, display_setup_time_units = self.get_display_setup_time(setup_time)
        display_runtime, display_runtime_units = self.get_display_runtime_units(runtime)

        routing_line = Routing.objects.create(
            partno=part_number,
            stepno=step_number,
            workorvend=work_or_vend,
            workcntr=work_center.shortname,
            vendcode=None,
            opercode=routing_oper_code,
            descrip=descrip,
            setuptime=display_setup_time,
            timeunit=display_setup_time_units,
            cycletime=display_runtime,
            cycleunit=display_runtime_units,
            machrun=1,  # TODO - what to do here? Is this nummach from Opercode?
            teamsize=team_size,
            scrappct=scrap_pct,
            pcteff=pct_eff,
            laboracct=work_center.laboracct,
            setuprate=setup_rate,
            cyclerate=cycle_rate,
            burdenrate=work_center.burdenrate,
            laborrate=work_center.laborrate,
            unattendop=unattend_op,
            leadtime=estim.leadtime,
            markuppct=estim.markuppct,
            certreq='N',
            glacct=None,
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
            setupprice=setup_price,
            cycleprice=cycle_price,
            total=self._exporter.get_value_relative_to_current_node(operation.cost.dollars),
            estimqty=None,
            actualpiecesgood=None,
            actualpiecesscrapped=None,
            ignorevendmin=None,
            nummachforjob=num_mach_for_job,
        )
        return routing_line

    def create_routing_line_from_outside_operation(self, part, operation, step_number, component):
        vendor_code, is_default_vendor_code = self.get_vendor_code(operation)

        default_vendor_code = self.get_or_create_default_vendor_code()

        # Get the VendCode record
        vend_code = Vendcode.objects.filter(vendcode=vendor_code).first()
        if vend_code is None:
            logger.info(f'Could not find a VendCode record with vendor code {vendor_code} - assigning to '
                        f'default vendor code {default_vendor_code.vendcode}')
            vend_code = default_vendor_code
            is_default_vendor_code = True

        descrip = self.get_outside_operation_description(is_default_vendor_code, operation)

        # Create the Routing record
        part_number = part.partno
        routing_line = Routing.objects.create(
            partno=part_number,
            stepno=step_number,
            workorvend=1,
            workcntr=None,
            vendcode=vend_code.vendcode,
            opercode=None,
            descrip=descrip,
            setuptime=None,
            timeunit='H',
            cycletime=None,
            cycleunit='H',
            machrun=1,
            teamsize=1,
            scrappct=0,
            pcteff=100,
            laboracct=None,
            setuprate=None,
            cyclerate=None,
            burdenrate=None,
            laborrate=None,
            unattendop='N',
            leadtime=vend_code.leadtime,
            markuppct=vend_code.markup if vend_code.markup is not None else 0,
            certreq='N',
            glacct=vend_code.glacct1,
            cost1=operation.cost.dollars / component.deliver_quantity,
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
            setupprice=0.,
            cycleprice=0.,
            total=self._exporter.get_value_relative_to_current_node(operation.cost.dollars),
            estimqty=None,
            actualpiecesgood=None,
            actualpiecesscrapped=None,
            ignorevendmin=None,
            nummachforjob=1,
        )
        return routing_line
