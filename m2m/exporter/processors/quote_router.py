import datetime
from typing import Optional

from baseintegration.datamigration import logger
from paperless.objects.orders import OrderCostingVariable, OrderComponent
import m2m.models as mm
from m2m.configuration import M2MConfiguration

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class QuoteRouterFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration
        self.price_summary: Optional[mm.Qtpest] = None

    def check_create_quote_routers(self, bom_line: mm.Qtdbom, comp: OrderComponent, components: {OrderComponent},
                                   m2m_quote_item: mm.Qtitem, price_summary: mm.Qtpest, consolidate: int = None) -> []:
        self.price_summary = price_summary
        ops = []
        op_number = 10
        if consolidate is not None:
            child = components[consolidate]
            op_number, ops = self.create_operation_record(bom_line, child, op_number, ops, m2m_quote_item,
                                                          is_consolidated=True)
        op_number, ops = self.create_operation_record(bom_line, comp, op_number, ops, m2m_quote_item)
        return ops

    def create_operation_record(self, bom_line: mm.Qtdbom, comp: OrderComponent, op_number: int, ops: [mm.Inrtgs],
                                quote_item: mm.Qtitem, is_consolidated=False):
        for op in comp.shop_operations:
            operation_memo = op.name
            if operation_memo.lower() in self.m2m_config.excluded_operations:
                continue
            operation_memo += f' :{op.notes}' if op.notes is not None else ''
            op_description = op.get_variable('Notes')
            operation_memo += f' - {op_description}' if op_description else ''
            fpro_id = None
            work_center: OrderCostingVariable
            work_center = op.get_variable_obj("Work Center")
            if hasattr(work_center, 'row'):
                fpro_id = work_center.row.get('fcpro_id')
            if fpro_id is None:
                logger.info(f'Did not find work center costing variable in {op.name} ')
                fpro_id = 'Default'  # TODO - what to do when an operation name isn't in the mapping?
                preamble = f'Could not find PP op {op.name} - please update the mapping.'
                operation_memo = f'{preamble} \n\n{operation_memo}'

            fstddesc = op.get_variable('Std Desc Code') or ''

            subcontract_cost = float(op.get_variable('Piece Price ($/part)') or 0.0)
            fixed_cost = float(op.get_variable('Lot Charge ($)') or 0.0)
            days = float(op.get_variable('Lead Time (days)') or 0.0)
            labor_rate = float(op.get_variable('Labor Cost') or 0.0)
            overhead_rate = float(op.get_variable('Overhead Cost') or 0.0)
            other_cost = float(op.get_variable('Other Cost') or 0.0)
            setup_time = op.setup_time or 0.0
            runtime = op.runtime or 0.0
            if runtime == 0.:
                runtime = .0000000001  # This column is a numeric(16,10) in SQL Server, 10 decimal places

            routing_line = mm.Qtdrtg.objects.create(
                fbominum=bom_line.fbominum,
                fchngrates='Y',
                felpstime=days,
                ffixcost=fixed_cost,
                finumber=quote_item.finumber,
                flschedule=True,
                fmovetime=0.0,
                foperno=op_number,
                foperqty=comp.innate_quantity if is_consolidated else 1.0,
                fothrcost=other_cost,
                fpro_id=fpro_id,
                fquoteno=quote_item.fquoteno,
                fsetuptime=setup_time,
                fstddesc=fstddesc if len(fstddesc) < 5 else '',
                fulabcost=labor_rate,
                fuovrhdcos=overhead_rate,
                fuprodtime=runtime,
                fusubcost=subcontract_cost,
                fllotreqd=False,
                fdescript='',
                fopermemo=operation_memo,
                fndbrmod=0,
                fnsimulops=1,
                cycleunits=0.0,
                unitsize=0.0,
                fccharcode='',
            )

            # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
            routing_line.refresh_from_db()

            ops.append(routing_line)
            op_number += 10 if op.operation_definition_name != 'NESTING' else 0
            self.update_price_summary_with_routing_line(routing_line, bom_line)
        return op_number, ops

    def update_price_summary_with_routing_line(self, routing_line: mm.Qtdrtg, bom_line: mm.Qtdbom):
        # data is modified/reformatted upon saving; use refresh_from_db to ensure we have accurate data
        self.price_summary.refresh_from_db()

        quantity = routing_line.foperqty * bom_line.fextqty
        prod_labor_cost = routing_line.fulabcost * routing_line.fuprodtime * quantity
        prod_overhead_cost = routing_line.fuovrhdcos * routing_line.fuprodtime * quantity
        setup_labor_cost = routing_line.fulabcost * routing_line.fsetuptime
        setup_overhead_cost = routing_line.fuovrhdcos * routing_line.fsetuptime
        sub_cost = routing_line.fusubcost * quantity + routing_line.ffixcost

        self.price_summary.flabcost += prod_labor_cost
        self.price_summary.fovhdcost += prod_overhead_cost
        self.price_summary.fsetupcost += setup_labor_cost + setup_overhead_cost
        self.price_summary.fsubcost += sub_cost
        self.price_summary.fothrcost += routing_line.fothrcost

        self.price_summary.save()
