from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Account, Contact
from jobboss.utils.repeat_work_utils import get_jb_contact_names, RepeatPartUtilObject, RfqUtil, JobUtil, \
    get_empty_string_if_none
from baseintegration.utils import safe_get, logger
import jobboss.models as jb


class AccountContactProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("AccountProcessor - Attempting to create Account")
        self.source_database = self._importer.source_database

        repeat_part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        for rfq_util in repeat_part_util_object.rfq_utils:
            rfq_util: RfqUtil = rfq_util
            for header in rfq_util.repeat_part_headers:
                header.account = self.get_account_from_jb_rfq_util(rfq_util)
                header.contact = self.get_contact_from_jb_rfq_util(rfq_util)

        for job_util in repeat_part_util_object.job_utils:
            job_util: JobUtil = job_util
            job_util.repeat_part_header.account = self.get_account_from_jb_job_util(job_util)
            job_util.repeat_part_header.contact = self.get_contact_from_jb_job_util(job_util)

        return repeat_part_util_object

    def get_account_from_jb_rfq_util(self, rfq_util: RfqUtil):
        jb_rfq = rfq_util.jb_rfq
        logger.info(f"Attempting to assign Account for JB RFQ: {jb_rfq.rfq}")
        jb_customer = jb.Customer.objects.using(self.source_database).filter(customer=jb_rfq.customer).first()

        account = Account(
            name=safe_get(jb_customer, "name", None),
            erp_code=safe_get(jb_customer, "customer", None),
            phone=None,  # JB Customer object does not have a phone number attribute. It is stored on the contact.
            url=safe_get(jb_customer, "url", None),
        )
        return account.to_json()

    def get_contact_from_jb_rfq_util(self, rfq_util: RfqUtil):
        jb_rfq = rfq_util.jb_rfq
        logger.info(f"Attempting to assign Contact for JB RFQ: {jb_rfq.rfq}")
        jb_contact = jb.Contact.objects.using(self.source_database).filter(contact=jb_rfq.contact).first()
        contact_first_name, contact_last_name = get_jb_contact_names(jb_contact)

        contact = Contact(
            email=safe_get(jb_contact, "email_address", None),
            first_name=contact_first_name,
            last_name=contact_last_name,
            notes=get_empty_string_if_none(safe_get(jb_contact, "title", None)),
            phone=safe_get(jb_contact, "phone", None),
        )
        return contact.to_json()

    def get_account_from_jb_job_util(self, job_util: JobUtil):
        jb_job = job_util.jb_job

        logger.info(f"Attempting to assign Account for JB Job: {jb_job.job}")
        jb_customer = jb_job.customer  # Related object

        account = Account(
            name=safe_get(jb_customer, "name", None),
            erp_code=safe_get(jb_customer, "customer", None),
            phone=None,  # JB Customer object does not have a phone number attribute. It is stored on the contact.
            url=safe_get(jb_customer, "url", None),
        )
        return account.to_json()

    def get_contact_from_jb_job_util(self, job_util: JobUtil):
        jb_job = job_util.jb_job
        logger.info(f"Attempting to assign Contact for JB Job: {jb_job.job}")
        jb_contact = jb.Contact.objects.using(self.source_database).filter(contact=jb_job.contact).first()
        contact_first_name, contact_last_name = get_jb_contact_names(jb_contact)

        contact = Contact(
            email=safe_get(jb_contact, "email_address", None),
            first_name=contact_first_name,
            last_name=contact_last_name,
            notes=get_empty_string_if_none(safe_get(jb_contact, "title", None)),
            phone=safe_get(jb_contact, "phone", None),
        )
        return contact.to_json()
