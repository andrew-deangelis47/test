import datetime

from baseintegration.datamigration import logger
from paperless.objects.orders import OrderCostingVariable, OrderComponent
import m2m.models as mm
from m2m.configuration import M2MConfiguration

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class RouterFactory:
    m2m_config = M2MConfiguration()

    def __init__(self, configuration: M2MConfiguration):
        self.m2m_config = configuration

    def check_create_standard_routers(self, item_record: mm.Inmastx, comp: OrderComponent, components: {OrderComponent},
                                      consolidate: int = None) -> []:
        ops = []
        router: mm.Inrtgc = mm.Inrtgc.objects.filter(fpartno=item_record.fpartno, fcpartrev=item_record.frev).first()
        if not isinstance(router, mm.Inrtgc):
            mm.Inrtgc.objects.create(fpartno=item_record.fpartno,
                                     fcpartrev=item_record.frev,
                                     fbatch01=0,
                                     fbatch02=0,
                                     fbatch03=0,
                                     fbatch04=0,
                                     fbatch05=0,
                                     fbatch06=0,
                                     fbatch07=0,
                                     fbatch08=0,
                                     fbatch09=0,
                                     fbatch10=0,
                                     fbatch11=0,
                                     fbatch12=0,
                                     ffixcost=0.00000,
                                     flabcost=0.00000,
                                     fmax01=0.00000,
                                     fmax02=0.00000,
                                     fmax03=0.00000,
                                     fmax04=0.00000,
                                     fmax05=0.00000,
                                     fmax06=0.00000,
                                     fmax07=0.00000,
                                     fmax08=0.00000,
                                     fmax09=0.00000,
                                     fmax10=0.00000,
                                     fmax11=0.00000,
                                     fmax12=0.00000,
                                     fothrcost=0.00000,
                                     fovrhdcos=0.00000,
                                     fqty01=0.00000,
                                     fqty02=0.00000,
                                     fqty03=0.00000,
                                     fqty04=0.00000,
                                     fqty05=0.00000,
                                     fqty06=0.00000,
                                     fqty07=0.00000,
                                     fqty08=0.00000,
                                     fqty09=0.00000,
                                     fqty10=0.00000,
                                     fqty11=0.00000,
                                     fqty12=0.00000,
                                     frev_date=item_record.frevdt,
                                     fsetuplabc=0.00000,
                                     fsetupovrc=0.00000,
                                     fsetuptime=0.00000,
                                     fspq=1.00000,
                                     fstdrtg="R",
                                     fsubcost=0.00000,
                                     ftottime=0.00000,
                                     fndbrmod=0,
                                     fac="Default",
                                     fcudrev=item_record.frev)
            op_number = 10

            if consolidate is not None:
                child = components[consolidate]
                op_number, ops = self.create_operation_record(item_record, child, op_number, ops)
            op_number, ops = self.create_operation_record(item_record, comp, op_number, ops)
            return ops
        logger.info('existing router found')
        return ops

    def create_operation_record(self, item_record: mm.Inmastx, comp: OrderComponent, op_number: int, ops: [mm.Inrtgs]):
        for op in comp.shop_operations:
            operation_memo = op.name
            if operation_memo.lower() in self.m2m_config.excluded_operations:
                continue
            operation_memo += f' :{op.notes}' if op.notes is not None else ''
            fpro_id = None
            work_center: OrderCostingVariable
            work_center = op.get_variable_obj("Work Center")
            if hasattr(work_center, 'row'):
                fpro_id = work_center.row.get('fcpro_id')
            if fpro_id is None:
                logger.info(f'Did not find work center costing variable in {op.name} ')
                fpro_id = 'NEW!'  # TODO - what to do when an operation name isn't in the mapping?
                preamble = f'Could not find PP op {op.name} - please update the mapping.'
                operation_memo = f'{preamble} \n\n{operation_memo}'

            fstddesc = op.get_variable('Std Desc Code')
            operation_code = fstddesc.split(" - ")[0].strip() if fstddesc is not None else ''

            labor_rate = 0.0
            overhead_rate = 0.0
            for var in op.costing_variables:
                if var.label == 'Labor Cost':
                    labor_rate = float(var.value) if var.value else 0.
                if var.label == 'Overhead Cost':
                    overhead_rate = float(var.value) if var.value else 0.
            setup_time = op.setup_time if op.setup_time is not None else 0.
            runtime = op.runtime if op.runtime is not None else 0.
            if runtime == 0.:
                runtime = .0000000001  # This column is a numeric(16,10) in SQL Server, 10 decimal places

            try:
                subcost = float(op.cost.dollars) / comp.deliver_quantity if op.is_outside_service else 0.
            except ZeroDivisionError:
                subcost = 0.0
            ops.append(mm.Inrtgs.objects.create(fpartno=item_record.fpartno,
                                                fcpartrev=item_record.frev,
                                                foperno=op_number if op.operation_definition_name != 'NESTING' else 1,
                                                fchngrates="Y",
                                                fcstddesc=operation_code if len(operation_code) < 5 else '',
                                                felpstime=0.00000,
                                                ffixcost=0.00000,
                                                flschedule=True,
                                                fmovetime=0.00,
                                                foperqty=comp.innate_quantity,
                                                fothrcost=0.00000,
                                                fpro_id=fpro_id,
                                                fsetuptime=setup_time,
                                                fsubcost=0.00000,
                                                fulabcost=labor_rate,
                                                fuovrhdcos=overhead_rate,
                                                fuprodtime=runtime,
                                                fusubcost=subcost,
                                                fllotreqd=False,
                                                fccharcode="",
                                                fopermemo=operation_memo,
                                                fndbrmod=0,
                                                fac="Default",
                                                fcudrev=item_record.frev,
                                                fnsimulops=1,
                                                fyield=100.00000,
                                                fsetyield=0.00,
                                                flbflabor=False,
                                                cycleunits=0.000,
                                                unitsize=0.000,
                                                ))
            op_number += 10 if op.operation_definition_name != 'NESTING' else 0
        return op_number, ops
