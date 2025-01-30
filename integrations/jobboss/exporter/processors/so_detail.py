import jobboss.models as jb
import uuid
import datetime
from baseintegration.datamigration import logger
from . import JobBossProcessor
from paperless.objects.orders import OrderComponent
from baseintegration.utils import safe_get, trim_django_model
from django.utils.timezone import make_aware


class SoDetailProcessor(JobBossProcessor):
    def get_fg_material(self, comp: OrderComponent):
        logger.info("Getting/creating finished good material.")
        fg_material = None
        part_number = comp.part_number
        if part_number:
            fg_material = jb.Material.objects.filter(material=comp.part_number).last()
        if fg_material is None:
            fg_material = jb.Material.objects.filter(material=self._exporter.erp_config.default_raw_material).last()
        return fg_material

    def _process(self, comp, i, job, order_item, so_header):
        if not self._exporter.erp_config.sales_orders_active:
            logger.info('Sales Orders are disabled.')
            return None
        fg_material = self.get_fg_material(comp)
        so_detail = jb.SoDetail(
            sales_order=so_header,  # Must be so header instance (not numeric)
            so_line='{:03d}'.format(i + 1),
            po=None,
            line=None,
            material=safe_get(fg_material, 'material'),  # Material ID not object
            ship_to=so_header.ship_to,  # This should be the integer address ID in JB (not instance or string)
            drop_ship=0,
            quote=None,
            job=job.job,
            status='Open',
            make_buy='M',
            unit_price=order_item.unit_price.dollars,
            discount_pct=0,
            price_uofm='ea',
            total_price=order_item.total_price.dollars,
            deferred_qty=order_item.quantity,  # The deferred_qty updates the matching PN FG "allocated_qty" on the
            # Material record. NOTE: there cannot also be a MaterialReq for the FG or the allocated_qty will not update
            prepaid_amt=0,
            unit_cost=order_item.unit_price.dollars,
            order_qty=order_item.quantity,
            stock_uofm='ea',
            backorder_qty=0,
            picked_qty=0,  # Picked qty default 0 so that the SO doesn't appear as fulfilled when created.
            shipped_qty=0,  # Picked qty default 0 so that the SO doesn't appear as fulfilled when created.
            returned_qty=0,
            certs_required=0,
            taxable=0,
            commissionable=0,
            commission_pct=0,
            sales_code=str(self._exporter.erp_config.sales_code),
            note_text='\n\n' + job.note_text if job.note_text is not None else ' ',
            promised_date=order_item.ships_on_dt,
            last_updated=make_aware(datetime.datetime.utcnow()),
            price_unit_conv=1,
            rev=comp.revision,
            tax_code=None,
            ext_description=None,
            cost_uofm='ea',
            cost_unit_conv=1,
            partial_res=0,
            prepaid_trade_amt=0,
            objectid=uuid.uuid4(),
            commissionincluded=0
        )
        try:
            so_detail = trim_django_model(so_detail)
            so_detail.save()
            so_detail.refresh_from_db()
            logger.info(f'Saved SoDetail {so_detail.so_detail}')
        except Exception as e:
            logger.error(f"Failed to save SoDetail {so_detail.so_detail}. [ERROR] - {e}")
            logger.error(so_detail.__dict__)
        return so_detail
