from typing import List, Union
from baseintegration.importer.import_processor import BaseImportProcessor
from sage.sage_api.client import SageImportClient
from sage.models.converters import SageCustomerToPaperlessAccountConverter, SageCustomerToPaperlessFacilityConverter, SageContactToPaperlessContactConverter
from baseintegration.utils import create_or_update_account, get_or_create_contact
from paperless.objects.customers import Facility as PaperlessFacility, BillingAddress
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity
from paperless.objects.customers import Account as PaperlessAccount
from baseintegration.integration import Integration
from baseintegration.datamigration import logger
from paperless.exceptions import PaperlessException
from sage.sage_api.filter_generation.customer_filter_generator import CustomerFilterGenerator
from sage.exceptions import SageInvalidResourceRequestedException, SageInvalidResponsePayloadException

PAPERLESS_EXCEPTION_CONTACT_INVALID_EMAIL = 'Enter a valid email address.'
PAPERLESS_EXCEPTION_CONTACT_BLANK_FIELD = 'This field may not be blank.'


def _get_customer(client: SageImportClient, cust_id: str) -> Union[SageCustomerFullEntity, bool]:
    """
    - calls the sage client to get the specified customer
    - returns the sage full customer object, or False if it does not find one
    """
    try:
        sage_full_cust_object = client.get_resource(
            SageCustomerFullEntity,
            CustomerFilterGenerator.get_filter_by_id(cust_id),
            False
        )
    except (SageInvalidResourceRequestedException, SageInvalidResponsePayloadException) as ex:
        logger.error(ex)
        return False

    # check that we actually got back some data
    if sage_full_cust_object is None:
        logger.error('No sage customer found with id ' + cust_id)
        return False

    # if everything worked return the customer
    return sage_full_cust_object


def handle_exception(err: PaperlessException, resource: str, resource_id: str):
    if PAPERLESS_EXCEPTION_CONTACT_INVALID_EMAIL in err.message:
        logger.warn(f'Invalid email address for {resource} with id {resource_id}, skipping import')
        return
    if PAPERLESS_EXCEPTION_CONTACT_BLANK_FIELD in err.message:
        logger.warn(f'Blank required field for {resource} with id {resource_id}, skipping import')
        return

    logger.warn(f'Paperless exception throw for {resource} with id {resource_id}: {err.message}')


def _create_or_update_contacts(sage_customer_full_entity: SageCustomerFullEntity, paperless_account: PaperlessAccount):
    for contact in sage_customer_full_entity.contacts:

        # 1) create paperless contact object from sage api data
        paperless_contact = SageContactToPaperlessContactConverter.to_paperless_contact(contact, paperless_account.id)

        # 2) check if contact already exists
        contact_found, contact_is_new = get_or_create_contact(contact.email, paperless_account)

        # 3) update or create contact for this account
        try:
            if contact_is_new:
                paperless_contact.create()
            else:
                contact_found.update()
        except PaperlessException as err:
            handle_exception(err, 'contact', paperless_contact.account_id)


def _create_or_update_facility(sage_customer_full_entity: SageCustomerFullEntity, paperless_account: PaperlessAccount):
    # 1) check if facility already exists - for Arcamed Sage integration there will only be one per account
    existing_facility_for_account_list = PaperlessFacility.list(account_id=paperless_account.id)

    # 2) If facility exists update it
    if len(existing_facility_for_account_list) > 0:
        existing_facility_for_account = SageCustomerToPaperlessFacilityConverter.update_existing_facility(
            existing_facility_for_account_list[0],
            sage_customer_full_entity
        )
        existing_facility_for_account.update()

    # 3) Create facility is it does not exist
    else:
        # need to confirm that the sage shipping address is a valid address before creating facility
        facility = SageCustomerToPaperlessFacilityConverter.to_paperless_facility(
            sage_customer_full_entity,
            paperless_account.id
        )
        if not facility:
            logger.warn('Not setting or updating facility for customer ' + sage_customer_full_entity.customer.code)
            return

        facility.create(account_id=paperless_account.id)


def _create_or_update_account(integration: Integration, sage_customer_full_entity: SageCustomerFullEntity,
                              cust_id: str) -> PaperlessAccount:
    # 1) create account object from sage api data
    paperless_account = SageCustomerToPaperlessAccountConverter.to_paperless_account(
        sage_customer_full_entity.customer,
        sage_customer_full_entity.addresses
    )

    # these are the most up-to-date addresses straight from Sage ERP
    current_billing_addresses = paperless_account.billing_addresses

    # 2) check if account already exists
    existing_paperless_account, is_new_account = create_or_update_account(
        integration,
        cust_id,
        paperless_account.name
    )

    # 3) Update or create account
    if is_new_account:
        paperless_account.create()
    else:
        paperless_account.id = existing_paperless_account.id
        paperless_account.update()

    # 4) Get rid of old billing addresses and update in case they have changed
    existing_billing_addrs = BillingAddress.list(account_id=paperless_account.id)
    for existing_billing_addr in existing_billing_addrs:
        existing_billing_addr.delete()
    for current_billing_address in current_billing_addresses:
        current_billing_address.create(account_id=paperless_account.id)

    # 5) return the object as we will need to pass it in to other functions
    return paperless_account


class SageBulkCustomerImportProcessor(BaseImportProcessor):

    def _process(self, customer_ids: List[str]) -> bool:
        client = SageImportClient.get_instance()
        for cust_id in customer_ids:

            # 1) Get customer info via the Sage API, should only be one thing returned but comes back as list
            sage_customer_full_entity = _get_customer(client, cust_id)
            if not sage_customer_full_entity:
                logger.error('Skipping customer ' + cust_id)
                continue

            # 3) create or update account from customer data
            paperless_account = _create_or_update_account(
                self._importer._integration,
                sage_customer_full_entity,
                cust_id
            )

            # 4) create or update associated contacts
            _create_or_update_contacts(sage_customer_full_entity, paperless_account)

            # 5) create or update associated facility (should only be one per the Arcamed SOW)
            _create_or_update_facility(sage_customer_full_entity, paperless_account)

        return True


class SageCustomerImportProcessor(SageBulkCustomerImportProcessor):
    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])


class SageCustomerBulkPlaceholder:
    pass
