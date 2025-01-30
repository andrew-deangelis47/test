import jobboss.models as jb
import datetime
from baseintegration.datamigration import logger
from . import JobBossProcessor
from paperless.objects.orders import OrderItem, OrderComponent
from jobboss.models import Job, SoDetail
from baseintegration.utils import trim_django_model
from django.utils.timezone import make_aware


class AddOnProcessor(JobBossProcessor):
    do_rollback = False

    def _process(self, order_item: OrderItem, comp: OrderComponent, job: Job, so_detail: SoDetail = None):
        now = make_aware(datetime.datetime.utcnow())
        additional_charges = []
        add_ons_list = []
        if comp.is_root_component or (comp.type == "manufactured") and self._exporter.erp_config.solo_mfg_comp_assembly:
            add_ons_list = order_item.ordered_add_ons

        for add_on in add_ons_list:
            if self._exporter.erp_config.should_link_addl_charge_to_sales_order_detail:
                add_on_item = self.link_addl_charge_to_sales_order_detail(add_on, so_detail, now)
                logger.info("Linked Additional Charge to SoDetail")
            else:
                add_on_item = self.link_addl_charge_to_job(add_on, job, now)
                logger.info("Linked Additional Charge to Job")
            try:
                add_on_item = trim_django_model(add_on_item)
                add_on_item.save()
            except Exception as e:
                logger.error(f'Failed to save AdditionalCharge! [ERROR]]: {e}')
            logger.info(f"Saved additional charge {add_on_item.description}")
            additional_charges.append(add_on_item)
        return additional_charges

    @staticmethod
    def link_addl_charge_to_sales_order_detail(add_on, so_detail: SoDetail, now):
        add_on_name = add_on.name
        add_on_item = jb.AdditionalCharge(
            so_detail=so_detail.so_detail,  # Must be an SoDetail number not an instance
            description=add_on_name,
            est_price=add_on.price.raw_amount,
            job_revenue=True,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=add_on.notes,
            last_updated=now,
            charge_type=0,
            approved=None,
            recurring=False,
            commissionincluded=False
        )
        return add_on_item

    @staticmethod
    def link_addl_charge_to_job(add_on, job: Job, now):
        add_on_name = add_on.name
        add_on_item = jb.AdditionalCharge(
            job=job,  # Must be a job instance, not integer
            description=add_on_name,
            est_price=add_on.price.raw_amount,
            job_revenue=False,
            commissionable=False,
            processed=False,
            taxable=False,
            note_text=add_on.notes,
            last_updated=now,
            approved=False,
            recurring=False,
            commissionincluded=False
        )
        return add_on_item
