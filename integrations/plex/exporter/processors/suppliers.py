from typing import Union
from paperless.objects.orders import OrderOperation
from plex.exporter.processors.base import PlexProcessor
from plex.objects.routing import PartOperation
from plex.objects.part import Part
from plex.objects.supplier import ApprovedSupplier, Supplier
from baseintegration.datamigration import logger


class SupplierProcessor(PlexProcessor):

    def _process(self, op: OrderOperation, part_op: PartOperation, part: Part) -> Union[ApprovedSupplier, bool]:

        code = op.get_variable(self._exporter.erp_config.costing_variable_supplier_code)
        if code is None:
            logger.debug('No supplier code found skipping')
            return False

        supplier: Supplier = Supplier.find_suppliers(code=code)
        if len(supplier) == 0:
            logger.debug('supplier code could not be matched up')
            return False
        try:
            ap_supplier: ApprovedSupplier = ApprovedSupplier(
                supplierId=supplier[0].id,
                partOperationId=part_op.id,
                partId=part.id,
            ).create()
        except TypeError:
            logger.exception("A Parameter type mismatch may have occurred")
            return False
        return ap_supplier
