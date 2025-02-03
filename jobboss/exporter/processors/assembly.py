import jobboss.models as jb
import uuid
import datetime
from . import JobBossProcessor
from paperless.objects.orders import OrderComponent
from paperless.objects.components import AssemblyComponent
from baseintegration.datamigration import logger
from baseintegration.utils import trim_django_model
from django.utils.timezone import make_aware


class AssemblyProcessor(JobBossProcessor):
    def _process(self, assm_comp: AssemblyComponent, comp: OrderComponent, comp_job: jb.Job, comp_uuid, job: jb.Job, root_job: jb.Job):
        now = make_aware(datetime.datetime.utcnow())
        # link the assembly
        if not comp.is_root_component:
            if not root_job:
                raise ValueError("Root job has not been saved yet!")
            bill_of_jobs = jb.BillOfJobs(
                parent_job=comp_job[assm_comp.parent.id],  # will be correct parent job even though parent ID could correspond to multiple jobs; this is because iterate_assembly uses DFS
                component_job=job,
                relationship_type='Component',
                relationship_qty=self._exporter.get_deliver_quantity(comp) / comp_job[assm_comp.parent.id].order_quantity,
                manual_link=False,
                last_updated=now,
                root_job=root_job.job,
                objectid=str(uuid.uuid4()),
                root_job_oid=root_job.objectid,
                parent_job_oid=comp_uuid[assm_comp.parent.id],  # will be correct parent job even though parent ID could correspond to multiple jobs; this is because iterate_assembly uses DFS
                component_job_oid=job.objectid
            )
            try:
                bill_of_jobs = trim_django_model(bill_of_jobs)
                bill_of_jobs.save()
                logger.info("Saved BillOfJobs")
            except Exception as e:
                logger.error(f'Failed to save BillOfQuotes! [ERROR]: {e}')
                logger.error(bill_of_jobs.__dict__)
