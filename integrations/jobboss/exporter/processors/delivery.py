import uuid
from baseintegration.datamigration import logger
import jobboss.models as jb
import datetime
from . import JobBossProcessor
from paperless.objects.orders import OrderItem
from django.utils.timezone import make_aware


class DeliveryProcessor(JobBossProcessor):
    def _process(self, order_item: OrderItem, job: jb.Job, so_detail: jb.SoDetail):
        delivery = jb.Delivery(
            job=job,
            so_detail=None,
            requested_date=order_item.ships_on_dt,
            promised_date=order_item.ships_on_dt,
            promised_quantity=order_item.quantity,
            shipped_quantity=0,
            remaining_quantity=order_item.quantity,
            returned_quantity=0,
            ncp_quantity=0,
            comment=None,  # Job notes should not end up on the delivery. This repeats notes on job paperwork.
            last_updated=make_aware(datetime.datetime.utcnow()),
            objectid=str(uuid.uuid4()),
        )
        try:
            delivery.save_with_autonumber()
            logger.info(f"Saved Delivery {delivery.delivery} for Job")
        except Exception as e:
            logger.error(f"Failed to save Delivery. [ERROR]: {e}")
            logger.error(delivery.__dict__)

        if so_detail is not None:
            delivery = jb.Delivery(
                job=None,  # Must be job instance
                so_detail=so_detail.so_detail,  # Must be string, not instance
                requested_date=order_item.ships_on_dt,
                promised_date=order_item.ships_on_dt,
                promised_quantity=order_item.quantity,
                shipped_quantity=0,
                remaining_quantity=order_item.quantity,
                returned_quantity=0,
                ncp_quantity=0,
                comment=None,  # Job notes should not end up on the delivery. This repeats notes on job paperwork.
                last_updated=make_aware(datetime.datetime.utcnow()),
                objectid=str(uuid.uuid4()),
                last_updated_by='PAPERLESS'
            )
            try:
                delivery.save_with_autonumber()
                logger.info(f'Created delivery {delivery.delivery} for Sales Order')
            except Exception as e:
                logger.error(f"Failed to save Delivery. [ERROR]: {e}")
                logger.error(delivery.__dict__)
        return delivery
