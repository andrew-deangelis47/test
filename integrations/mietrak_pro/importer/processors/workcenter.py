from typing import List
from mietrak_pro.importer.utils import MieTrakProCustomTableImportProcessor
from mietrak_pro.models import Operation


class WorkCenterImportProcessor(MieTrakProCustomTableImportProcessor):
    def _get_row_data(self, entity_id: int) -> dict:
        op: Operation = Operation.objects.filter(operationpk=entity_id).first()
        if not op:
            raise Exception(f"Was not able to import material {entity_id} as it could not be found in the Item table")

        ''' Sum up setup (Operation profit rate, employee rate, operation overhead rate)  = operation sell rate
            Sum up runtime(...
        '''
        row = {
            "OperationPK": op.operationpk,
            "WorkCenterFK": op.workcenterfk.workcenterpk if op.workcenterfk else None,
            "WorkCenterDesc": op.workcenterfk.description if op.workcenterfk else None,
            "Name": op.name,
            "Description": op.description,
            "SetupOperationProfitRate": float(op.setupoperationprofitrate) if op.setupoperationprofitrate else 0.,
            "SetupOperationOverHeadRate": float(op.setupoperationoverheadrate) if op.setupoperationoverheadrate else 0.,
            "SetupEmployeeRate": float(op.setupemployeerate) if op.setupemployeerate else 0.,
            "RunOperationProfitRate": float(op.runoperationprofitrate) if op.runoperationprofitrate else 0.,
            "RunOperationOverHeadRate": float(op.runoperationoverheadrate) if op.runoperationoverheadrate else 0.,
            "RunEmployeeRate": float(op.runemployeerate) if op.runemployeerate else 0.
        }
        setupopsellrate = row["SetupOperationProfitRate"] + row["SetupOperationOverHeadRate"] + row["SetupEmployeeRate"]
        row['SetupOperationSellRate'] = setupopsellrate
        runopsellrate = row["RunOperationProfitRate"] + row["RunOperationOverHeadRate"] + row["RunEmployeeRate"]
        row['RunOperationSellRate'] = runopsellrate

        if self._importer.erp_config.should_import_division and op.divisionfk:
            row["DivisionFK"] = op.divisionfk.divisionpk
        return row


class MieTrakProWorkCenterBulkImportProcessor(MieTrakProCustomTableImportProcessor):
    def _process(self, entity_ids: List[int]):
        self.update_custom_table(entity_ids=entity_ids)


class BulkWorkCenterImportPlaceholder:
    pass
