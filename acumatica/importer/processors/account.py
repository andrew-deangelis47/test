from paperless.exceptions import PaperlessException
from paperless.objects.address import Address as PaperlessAddress
from paperless.objects.customers import Account, Contact as \
    PaperlessContact, Facility, BillingAddress

from baseintegration.integration import logger
from baseintegration.utils.address import AddressUtils
from baseintegration.utils import set_blank_to_default_value, create_or_update_account
from baseintegration.importer.import_processor import BaseImportProcessor

from acumatica.api_models.acumatica_models import Customer, Contact, Address, BillingContact


class AccountImportProcessor(BaseImportProcessor):

    @staticmethod
    def get_credit_limit(customer: Customer):
        return 0.

    @staticmethod
    def get_is_po_enabled(customer: Customer):
        return True

    @staticmethod
    def get_is_tax_exempt(customer: Customer):
        return False

    @staticmethod
    def get_payment_terms(customer: Customer):
        payment_terms = customer.Terms
        period = 0
        return payment_terms, period

    def _sync_billing_address(self, customer: Customer, account: Account):

        billing_contact: BillingContact = customer.get_billing_contact()
        address: Address = billing_contact.get_address()

        paperless_billing_addresses = BillingAddress.list(account_id=account.id)

        erp_code_map = {}
        for billing_address in paperless_billing_addresses:
            # TODO 1 Billing Address in Acumatica. Should we delete all exisxting before update?
            billing_address.delete()

        # Use ID for the erp_code
        erp_code = address.id

        # FIXME: Paramterize what the default should be in case we are
        #  deploying to international locations
        formatted_country, formatted_state = AddressUtils.get_country_and_state(address.Country,
                                                                                address.State,
                                                                                address.PostalCode,
                                                                                fallback_country_alpha_3='USA')
        billing_address = BillingAddress(address1=address.AddressLine1,
                                         city=address.City,
                                         state=formatted_state,
                                         postal_code=address.PostalCode,
                                         erp_code=erp_code,
                                         country=formatted_country)
        #  if address.AddressLine2:
        #    billing_address.address2 = address.AddressLine2

        #  Check if there is a Billing Address that matches on erp_code
        existing_billing = erp_code_map.get(erp_code)
        logger.info(
            f'Searching for billing address with erp_code: {erp_code}. '
            f'Result of: {existing_billing}')

        try:  # pragma: no cover
            if not existing_billing:
                #  There is not a match, create one!
                billing_address.create(account_id=account.id)
            else:
                #  There is a match, update the existing!
                billing_address.id = existing_billing.id
                billing_address.update()
        except Exception as e:
            logger.info("Failed to create or update billing address")
            logger.warning(e)

    @classmethod
    def _sync_shipping_address(self, customer: Customer, account: Account):
        facilities: list[Facility] = Facility.list(account_id=account.id)
        erp_code_map = {}
        for facility in facilities:
            addr: Address = facility.address
            if not addr:
                continue
            erp_code_map[facility.address.erp_code] = facility

        customer_locations = customer.get_customer_locations(customer_id=customer.CustomerID)
        if not customer_locations:
            logger.info(f'Shipping contact not found for {account.name}')
            return

        for customer_location in customer_locations:
            name = customer_location.LocationName
            erp_code = customer_location.LocationID  # TODO
            try:
                shipping_address: Address = customer_location.get_address()
            except Exception as e:
                logger.error(f'Skipping address with error - {e}')
                continue

            address1 = shipping_address.AddressLine1
            city = shipping_address.City
            state = shipping_address.State
            postal_code = shipping_address.PostalCode
            country = shipping_address.Country

            if not (address1 and city and state and postal_code and country):
                logger.info(f'Skipping facility with incomplete address: {shipping_address}')
                return

            logger.info(f'Processing Facility: with ID {erp_code}')
            formatted_country, formatted_state = AddressUtils.get_country_and_state(
                country_name=country,
                state_province_name=state,
                zipcode=postal_code,
                fallback_country_alpha_3='USA')

            address = PaperlessAddress(
                address1=address1,
                city=city,
                state=formatted_state,
                postal_code=postal_code,
                country=formatted_country,
                erp_code=erp_code)

            logger.debug(f'Address: {address}')

            # Since it is possible the facility above is actually a
            # minimal set of info returned in list form, we are going to
            # create a new object every time to be sure.

            # Check if there is a bill to number that matches on erp_code
            existing_facility = erp_code_map.get(erp_code)
            logger.debug(f'Searching for facility with erp_code: {erp_code}. '
                         f'Result of: {existing_facility}')

            facility = Facility(
                name=name,
                account_id=account.id,
                address=address,
                attention=''
            )
            logger.info(facility)
            try:  # pragma: no cover
                if not existing_facility:
                    # There is not a match, create one!
                    facility.create(account_id=account.id)
                    logger.info(f'Created new facility - {facility.name} - {erp_code}')
                else:
                    # There is a match, update the existing!
                    facility.id = existing_facility.id
                    facility.update()
                    logger.info(f'Updated existing facility - {facility.name} - {erp_code}')
            except Exception as e:  # pragma: no cover
                logger.info("Failed to create or update facility")
                logger.warning(e)

    def _sync_contacts(self, customer: Customer, account: Account):
        logger.info('Contact sync')
        contacts: list = customer.get_contacts()
        if not contacts:
            logger.info(f'No Contacts found for Account {account.name}')
            return
        for contact in contacts:
            contact: Contact
            if not contact:
                logger.info("Skipping contact")
                continue
            else:
                contacts = PaperlessContact.search(f'email={contact.Email}')

                first_name = set_blank_to_default_value(contact.FirstName, 'N/A')
                last_name = set_blank_to_default_value(contact.LastName, 'N/A')
                paperless_contact = PaperlessContact(
                    first_name=first_name,
                    last_name=last_name,
                    email=contact.Email,
                    #  salesperson=salesperson,
                    account_id=account.id)

                contact_id = None
                if contacts:
                    contact: PaperlessContact = contacts[0]
                    contact_id = contact.id

                try:  # pragma: no cover
                    if contact_id:
                        logger.info('f Updating')
                        paperless_contact.id = contact_id
                        paperless_contact.update()
                    else:
                        # Create!
                        paperless_contact.create()
                except PaperlessException as e:
                    logger.debug(f'Error syncing contact: '
                                 f'{paperless_contact}. {repr(e)}')

    def _sync_customer(self, customer: Customer) -> Account:
        erp_code = customer.CustomerID
        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=erp_code,
                                                              account_name=customer.CustomerName)

        is_po_enabled = self.get_is_po_enabled(customer=customer)
        is_tax_exempt = self.get_is_tax_exempt(customer=customer)
        payment_terms, payment_period = self.get_payment_terms(customer=customer)

        pp_account.erp_code = erp_code
        pp_account.name = customer.CustomerName
        pp_account.purchase_orders_enabled = is_po_enabled
        pp_account.tax_exempt = is_tax_exempt

        if payment_period and payment_terms:
            if isinstance(payment_period, int):
                pp_account.payment_terms = payment_terms
                pp_account.payment_terms_period = payment_period

        if not account_is_new:
            pp_account.update()
        else:
            pp_account.create()
        return pp_account

    def _process(self, customer_id: str) -> [Account, None]:
        logger.info(f'Processing Acumatica Customer ID: {customer_id}')

        customer: Customer = Customer.get(cust_id=customer_id)
        account: Account = self._sync_customer(customer=customer)
        if not isinstance(account, Account):  # pragma: no cover
            logger.info(f'Account not created for customer ID - {customer_id}. '
                        f'Skipping Contact/Address Processor')
            return

        self._sync_contacts(customer=customer, account=account)
        self._sync_shipping_address(customer=customer, account=account)
        self._sync_billing_address(customer=customer, account=account)

        return account
