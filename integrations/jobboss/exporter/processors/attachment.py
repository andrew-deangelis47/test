import jobboss.models as jb
import datetime
from paperless.objects.orders import Order
from . import JobBossProcessor
from django.utils.timezone import make_aware


class AttachmentProcessor(JobBossProcessor):
    def _process(self, order: Order, so_header=None, job=None):
        if so_header:
            order_link = self.process_so_order_link(order, so_header)
            quote_link = self.process_so_quote_link(order, so_header)
            pv_link = None
        elif job:
            order_link = self.process_job_order_link(order, job)
            quote_link = self.process_job_quote_link(order, job)
            pv_link = self.process_part_viewer_link(order, job)
        else:
            return None, None, None
        return order_link, quote_link, pv_link

    def process_so_order_link(self, order: Order, so_header: jb.SoHeader) -> jb.Attachment:
        # create links to quote and order
        so_order_link = jb.Attachment(
            owner_type='SOHeader',
            owner_id=so_header.sales_order,
            attach_path='https://app.paperlessparts.com/orders/edit/{}'.format(
                order.number),
            description='PP Order #{}'.format(order.number),
            print_attachment=False,
            last_updated=make_aware(datetime.datetime.utcnow()),
            attach_type='Link'
        )
        so_order_link.save_with_autonumber()
        return so_order_link

    def process_so_quote_link(self, order: Order, so_header: jb.SoHeader) -> jb.Attachment:
        quote_number = self.get_quote_number(order)
        so_quote_link = jb.Attachment(
            owner_type='SOHeader',
            owner_id=so_header.sales_order,
            attach_path='https://app.paperlessparts.com/quotes/edit/{}'.format(
                quote_number),
            description='PP Quote #{}'.format(quote_number),
            print_attachment=False,
            last_updated=make_aware(datetime.datetime.utcnow()),
            attach_type='Link'
        )
        so_quote_link.save_with_autonumber()
        return so_quote_link

    def process_job_order_link(self, order: Order, job: jb.Job) -> jb.Attachment:
        # create links to quote and order
        job_order_link = jb.Attachment(
            owner_type='Job',
            owner_id=job.job,
            attach_path='https://app.paperlessparts.com/orders/edit/{}'.format(
                order.number),
            description='PP Order #{}'.format(order.number),
            print_attachment=False,
            last_updated=make_aware(datetime.datetime.utcnow()),
            attach_type='Link'
        )
        job_order_link.save_with_autonumber()
        return job_order_link

    def process_job_quote_link(self, order: Order, job: jb.Job) -> jb.Attachment:
        quote_number = self.get_quote_number(order)
        job_quote_link = jb.Attachment(
            owner_type='Job',
            owner_id=job.job,
            attach_path='https://app.paperlessparts.com/quotes/edit/{}'.format(
                quote_number),
            description='PP Quote #{}'.format(quote_number),
            print_attachment=False,
            last_updated=make_aware(datetime.datetime.utcnow()),
            attach_type='Link'
        )
        job_quote_link.save_with_autonumber()
        return job_quote_link

    def process_part_viewer_link(self, order: Order, job: jb.Job):
        for order_item in order.order_items:
            if order_item.root_component is not None:
                job_pv_link = jb.Attachment(
                    owner_type='Job',
                    owner_id=job.job,
                    attach_path='https://app.paperlessparts.com/parts/viewer/{}'.format(
                        order_item.root_component.part_uuid),
                    description='PP Part Viewer Link',
                    print_attachment=False,
                    last_updated=make_aware(datetime.datetime.utcnow()),
                    attach_type='Link'
                )
                job_pv_link.save_with_autonumber()
                return job_pv_link

    def get_quote_number(self, order):
        if order.quote_revision_number is not None:
            quote_number = f'{order.quote_number}-{order.quote_revision_number}'
        else:
            quote_number = f'{order.quote_number}'
        return quote_number
