"""
Database field helpers
"""
import datetime
from datetime import timedelta
import uuid
from string import ascii_lowercase

from baseintegration.utils import retry_if_deadlocked
from jobboss.models import WorkCenter, Vendor, Material, Operation, Job
from paperless.objects.orders import OrderComponent
from django.utils.timezone import make_aware

MAX_JOB_RETRIES = 20
DEFAULT_WORK_CENTER_NAME = 'OTHER'
DEFAULT_VENDOR_NAME = 'OTHER'


def shipping_option_summary(shipping_option_dict: dict) -> str:
    acct_number = shipping_option_dict.get('customers_account_number')
    carrier = shipping_option_dict.get('customers_carrier')
    shipping_method = shipping_option_dict.get('shipping_method')
    if acct_number:
        summary = '{} {}'.format(carrier, acct_number)
    else:
        summary = shipping_method
    if summary:
        summary = summary[0:15]
    return summary


def get_operation(op_name: str) -> Operation:
    if op_name:
        return Operation.objects.filter(operation__iexact=op_name).first()


def get_work_center(op_name: str) -> WorkCenter:
    if op_name:
        return WorkCenter.objects.filter(work_center__iexact=op_name).first()


def get_default_work_center(name: str = None) -> WorkCenter:
    if name is None:
        name = DEFAULT_WORK_CENTER_NAME
    qs = WorkCenter.objects.filter(work_center=name)
    if qs.count() > 0:
        return qs.first()
    return WorkCenter.objects.create(
        work_center=name,
        type='Direct',
        setup_labor_rate=0,
        run_labor_rate=0,
        labor_burden=0,
        machine_burden=0,
        ga_burden=0,
        queue_hrs=0,
        link_material=False,
        link_component=False,
        last_updated=make_aware(datetime.datetime.utcnow()),
        is_parent=False,
        has_parent=False,
        objectid=uuid.uuid4(),
        machines=1,
        operators=1,
        operators_per_machine=1,
        link_finishedgoods=False,
        link_hardware=False,
        link_supplies=False,
        link_misc=False,
        link_rawstock=False,
        finite_schedule=False,
        lag_hrs=0,
        uvamount1=0,
        uvamount2=0,
        uvnumeric1=0,
        uvnumeric2=0,
        uvdecimal1=0,
        equipment=False,
    )


def get_vendor(op_name: str) -> Vendor:
    if op_name:
        return Vendor.objects.filter(vendor__iexact=op_name).first()


def get_default_vendor(vendor: str = None) -> Vendor:
    if vendor is None:
        vendor = DEFAULT_VENDOR_NAME
    qs = Vendor.objects.filter(vendor__iexact=vendor.upper()[:10])
    if qs.count() > 0:
        return qs.first()
    return Vendor.objects.create(
        vendor=vendor.upper()[:10],
        name="PAPERLESS PARTS DEFAULT",
        status='Active',
        vendor_since=make_aware(datetime.datetime.utcnow()),
        lead_days=0,
        send_1099=False,
        currency_def=1,
        last_updated=make_aware(datetime.datetime.utcnow()),
        rating=10,
        send_report_by_email=False
    )


def increment_job(job_number):
    """Increment job number to find a unique value"""
    last_char = job_number[-1].lower()
    if last_char in ascii_lowercase and last_char != 'z':
        return job_number[0:-1] + ascii_lowercase[ascii_lowercase.find(last_char) + 1]
    else:
        return job_number + 'a'


def get_material(part_number: str) -> Material:
    pn = part_number.strip()
    return Material.objects.filter(material__iexact=pn).first()


def get_template_job(comp: OrderComponent, config_options) -> Job:
    part_number = comp.part_number.strip() if comp.part_number is not None else None
    revision = comp.revision.strip() if comp.revision is not None else None
    if part_number and revision and config_options.revision_must_match:
        return Job.objects.filter(
            part_number=part_number,
            rev=revision,
            status='Template'
        ).last()
    elif part_number:
        def get_job():
            return Job.objects.filter(
                part_number=part_number.strip(),
                status='Template'
            ).last()
        return retry_if_deadlocked(get_job)
    else:
        return None


def get_most_recent_job(comp: OrderComponent, config_options) -> Job:
    part_number = comp.part_number.strip() if comp.part_number is not None else None
    revision = comp.revision.strip() if comp.revision is not None else None
    component_type = str(comp.type)
    # Prevent integration from matching the job it just created on the specified part number
    older_than_date = make_aware(datetime.datetime.utcnow()) - timedelta(minutes=5)
    comp_type_dict = {
        "assembled": "Assembly",
        "manufactured": "Regular",
    }
    if part_number and revision and config_options.revision_must_match:
        return Job.objects.filter(
            part_number=part_number,
            rev=revision,
            type=comp_type_dict.get(component_type, "Regular"),
            last_updated__lte=older_than_date
        ).order_by('last_updated').last()
    elif part_number:
        def get_job():
            return Job.objects.filter(
                part_number=part_number.strip(),
                type=comp_type_dict.get(component_type, "Regular"),
                last_updated__lte=older_than_date
            ).order_by('last_updated').last()
        return retry_if_deadlocked(get_job)
    else:
        return None
