from baseintegration.integration import logger
from baseintegration.utils.address import AddressUtils
from baseintegration.utils import set_blank_to_default_value, clean_up_phone_number
from epicor.customer import Customer, Contact as EpicorContact
from epicor.customer import PaymentTerms
from typing import Union
from epicor.importer.processors.base import EpicorImportProcessor
from paperless.exceptions import PaperlessException
from paperless.objects.address import Address
from paperless.objects.customers import Account, Contact as \
    PaperlessContact, Facility, BillingAddress, PaymentTerms as PaperlessPaymentTerms
from paperless.objects.common import Salesperson as PaperlessSalesperson
from epicor.salesperson import Salesperson


class AccountImportProcessor(EpicorImportProcessor):

    def _process(self, customer_id: str) -> Account:
        logger.info(f'Processing Epicor Customer ID: {customer_id}')
        account = self._process_account(customer_id)
        return account

    def _process_account(self, customer_id: str) -> Union[Account, None]:

        customer = Customer.get_by_id(cust_id=customer_id)
        if customer.Inactive is not None and bool(customer.Inactive):
            logger.info("Customer is inactive. Skipping.")
            return None

        account = self._sync_customer(customer=customer)
        self._sync_salesperson(customer=customer, account=account)
        self._sync_payment_terms(customer=customer, account=account)
        self._sync_contacts(customer=customer, account=account)
        self._sync_ship_toes(customer=customer, account=account)
        self._sync_bill_to(customer=customer, account=account)

        return account

    def _sync_customer(self, customer: Customer) -> Account:
        erp_code = customer.CustID
        accounts = Account.filter(erp_code=erp_code)
        account_id = None
        if accounts:
            logger.debug(f'erp_code: {erp_code} returned multiple Paperless Parts Accounts: {accounts}')
            account_id = accounts[0].id
        addr = None

        if customer.Address1 and customer.State and customer.City and customer.Country and customer.Zip:
            formatted_country, formatted_state = AddressUtils.get_country_and_state(customer.Country, customer.State,
                                                                                    customer.Zip,
                                                                                    fallback_country_alpha_3='USA')
            addr = Address(address1=customer.Address1,
                           address2=customer.Address2,
                           state=formatted_state,
                           city=customer.City,
                           postal_code=customer.Zip,
                           country=formatted_country
                           )

        account = Account(
            erp_code=erp_code,
            sold_to_address=addr,
            name=customer.Name,
            url=customer.CustURL,
            notes=customer.Comment,
            phone=clean_up_phone_number(customer.PhoneNum),
            payment_terms=customer.TermsCode,
            payment_terms_period=int(customer.TermsCode[-2:]) if customer.TermsCode and customer.TermsCode[-2:].isdigit() else 0
        )
        if account_id:
            # account = Account.get(account_id)
            account.id = account_id

            # FIXME! This always throws an exception, but it really does seem
            #  that the auth is setup correctly
            # raise PaperlessException(message=message, error_code=resp.status_code)
            # paperless.exceptions.PaperlessException: Authentication credentials were not provided.
            account.update()
        else:
            account.create()

        return account

    def _sync_contacts(self, customer: Customer, account: Account):
        # Sync over contacts
        contacts = customer.get_contacts()
        if contacts:
            for contact in contacts:
                if not contact.EMailAddress:
                    logger.info(f"Skipping contact because it does not have an email {contact.Name}")
                    continue
                elif contact.Inactive:
                    logger.info("Skipping contact because it is inactive")
                    continue
                else:
                    contact: EpicorContact
                    # print(contact)
                    contacts = PaperlessContact.search(
                        f'email={contact.EMailAddress}')
                    # print(contacts)
                    first_name = contact.FirstName
                    last_name = contact.LastName
                    if not first_name and not last_name and contact.Name:
                        names = set_blank_to_default_value(contact.Name, '').split(' ')
                        first_name = names[0]
                        last_name = names[1] if len(names) > 1 else first_name
                    first_name = set_blank_to_default_value(first_name, 'N/A')
                    last_name = set_blank_to_default_value(last_name, 'N/A')
                    paperless_contact = PaperlessContact(
                        first_name=first_name,
                        last_name=last_name,
                        email=contact.EMailAddress,
                        # salesperson=salesperson,
                        account_id=account.id)
                    contact_id = None
                    if contacts:
                        contact: PaperlessContact = contacts[0]
                        contact_id = contact.id

                    try:

                        if contact_id:
                            # Update!
                            paperless_contact.id = contact_id
                            paperless_contact.update()
                        else:
                            # Create!
                            paperless_contact.create()
                    except PaperlessException as e:
                        logger.debug(f'Error syncing contact: '
                                     f'{paperless_contact}. {repr(e)}')

    def _sync_ship_toes(self, customer: Customer, account: Account):

        ship_toes = customer.ship_toes()
        facilities = Facility.list(account_id=account.id)
        erp_code_map = {}
        for facility in facilities:
            addr: Address = facility.address
            if not addr:
                continue
            erp_code_map[facility.address.erp_code] = facility

        for ship_to in ship_toes:
            if not (ship_to.Name and ship_to.Address1 and ship_to.City and ship_to.ZIP and ship_to.State):
                logger.info(f'Skipping Ship To with incomplete address: {ship_to}')
                continue
            name = ship_to.Name
            erp_code = ship_to.ShipToNum
            logger.info(f'Processing Ship To: {ship_to}')

            formatted_country, formatted_state = AddressUtils.get_country_and_state(ship_to.Country, ship_to.State,
                                                                                    ship_to.ZIP,
                                                                                    fallback_country_alpha_3='USA')
            address = Address(address1=ship_to.Address1,
                              address2=ship_to.Address2,
                              city=ship_to.City,
                              state=formatted_state,
                              postal_code=ship_to.ZIP,
                              country=formatted_country,
                              erp_code=erp_code
                              )
            # logger.debug(f'Address: {address}')

            # Since it is possible the facility above is actually a
            # minimal set of info returned in list form, we are going to
            # create a new object every time to be sure.

            # Check if there is a bill to number that matches on erp_code
            existing_facility = erp_code_map.get(erp_code)
            logger.debug(f'Searching for facility with erp_code: {erp_code}. '
                         f'Result of: {existing_facility}')

            facility = Facility(name=name,
                                account_id=account.id,
                                address=address,
                                # TODO Attn, which would need to be
                                #  extracted from address lines having a
                                #  certain "Attention" or "Attn" string...?
                                attention=''
                                # TODO Salesperson
                                )

            try:
                if not existing_facility:
                    # There is not a match, create one!
                    facility.create(account_id=account.id)
                else:
                    # There is a match, update the existing!
                    facility.id = existing_facility.id
                    facility.update()
            except Exception as e:
                logger.info("Failed to create or update facility")
                logger.warning(e)

    def _sync_bill_to(self, customer: Customer, account: Account):
        # There is only one possible billing address in Epicor, and it
        # does not have a unique identifier for the erp_code, so we are
        # using the name. To be safe, we are allowing multiple addresses
        # to exist on the Paperless side, and only matching the one
        # known BT if present.

        if not (customer.BTCity and customer.BTState and customer.BTZip and customer.BTAddress1):
            logger.info(f'Incomplete Billing Address for customer: {customer.CustID}, skipping BillingAddress.')

        billing_addresses = BillingAddress.list(account_id=account.id)

        erp_code_map = {}
        for billing_address in billing_addresses:
            erp_code_map[billing_address.erp_code] = billing_address

        # Use the name for the erp_code, else address line 1
        name = customer.BTName
        erp_code = name if name else customer.BTAddress1

        # FIXME: Paramterize what the default should be in case we are
        #  deploying to international locations
        formatted_country, formatted_state = AddressUtils.get_country_and_state(customer.BTCountry, customer.BTState,
                                                                                customer.BTZip,
                                                                                fallback_country_alpha_3='USA')
        billing_address = BillingAddress(address1=customer.BTAddress1,
                                         city=customer.BTCity,
                                         state=formatted_state,
                                         postal_code=customer.BTZip,
                                         erp_code=erp_code,
                                         country=formatted_country
                                         )

        if customer.BTAddress2:
            billing_address.address2 = customer.BTAddress2

        # Check if there is a Billing Address that matches on erp_code
        existing_billing = erp_code_map.get(erp_code)
        logger.debug(
            f'Searching for billing address with erp_code: {erp_code}. '
            f'Result of: {existing_billing}')

        try:
            if not existing_billing:
                # There is not a match, create one!
                billing_address.create(account_id=account.id)
            else:
                # There is a match, update the existing!
                billing_address.id = existing_billing.id
                billing_address.update()
        except Exception as e:
            logger.info("Failed to create or update billing address")
            logger.warning(e)

    def _sync_payment_terms(self, customer: Customer, account: Account):
        logger.info("Attempting to sync payment terms")
        # Get epicor payment terms
        epicor_payment_terms: PaymentTerms = self._get_epicor_payment_terms(customer)
        if not epicor_payment_terms:
            return None

        # Get paperless payment terms list to map epicor terms to
        paperless_payment_terms = PaperlessPaymentTerms.list()

        # Set control flow variables
        payment_terms_already_exists = False
        epicor_terms_code_has_match = False
        paperless_payment_term = None

        # Iterate paperless terms to attempt to find a match with an epicor terms object for update/reassign/create
        if paperless_payment_terms:
            for paperless_term in paperless_payment_terms:
                if epicor_payment_terms.TermsCode == paperless_term.label:
                    epicor_terms_code_has_match = True
                    paperless_payment_term = paperless_term  # Set the term to the paperless term to be updated
                if epicor_payment_terms.Description == paperless_term.label:
                    payment_terms_already_exists = True
                    paperless_payment_term = paperless_term  # Set the term to the existing term to reassign

        if payment_terms_already_exists:
            # Reassign existing terms object to the account
            self._reassign_paperless_payment_terms(epicor_payment_terms, paperless_payment_term, account)
        elif epicor_terms_code_has_match:
            # Update existing terms to include erp_code and change label to human-readable format
            self._update_paperless_payment_terms(epicor_payment_terms, paperless_payment_term)
        else:
            # Paperless terms object does not yet exist, create it and associate it to the account
            self._create_paperless_payment_terms(epicor_payment_terms, account)

    def _reassign_paperless_payment_terms(self, epicor_payment_terms: PaymentTerms, paperless_payment_term,
                                          account: Account):
        account.payment_terms = paperless_payment_term.label
        account.payment_terms_period = self._get_number_of_days(epicor_payment_terms)
        try:
            account.update()
            logger.info(f"Updated PP Account terms to {account.payment_terms}")
        except Exception as e:
            logger.info(f"Failed to update PP Account terms to {account.payment_terms}\n{e}")

    def _update_paperless_payment_terms(self, epicor_payment_terms: PaymentTerms, paperless_term: PaperlessPaymentTerms):
        paperless_term.label = epicor_payment_terms.Description
        paperless_term.period = self._get_number_of_days(epicor_payment_terms)
        paperless_term.erp_code = epicor_payment_terms.TermsCode
        try:
            paperless_term.update()
            logger.info(f"Updated PP terms to Epicor payment term: {epicor_payment_terms.Description}")
        except Exception as e:
            logger.info(f"Failed to update payment terms. PP term ID: {paperless_term.id}\n{e}")
        return None

    def _create_paperless_payment_terms(self, epicor_payment_terms, account: Account):
        paperless_term = PaperlessPaymentTerms(
            label=epicor_payment_terms.Description,
            period=self._get_number_of_days(epicor_payment_terms),
            erp_code=epicor_payment_terms.TermsCode
        )
        try:
            paperless_term.create()
            logger.info(f"Created new Paperless Payment Terms: {paperless_term.label}")
            account.payment_terms = paperless_term.label
            account.payment_terms_period = paperless_term.period
            account.update()
        except Exception as e:
            logger.info(f"Failed to create new Paperless Payment Terms for Epicor terms object: "
                        f"{epicor_payment_terms.Description}\n{e}")
            return None

    def _get_epicor_payment_terms(self, customer: Customer) -> Union[PaymentTerms, None]:
        logger.info(f"Getting payment terms for customer {customer.Name}")
        epicor_terms_object = PaymentTerms.get_by_code(customer.TermsCode)
        if epicor_terms_object:
            return epicor_terms_object
        logger.info(f'No payment terms could be located for {customer.Name}')
        return None

    def _get_number_of_days(self, epicor_payment_terms: PaymentTerms) -> int:
        epicor_days_field = epicor_payment_terms.NumberOfDays
        if epicor_days_field is None:
            # Set number of days to 1 to pass paperless validation for zeroed out Epicor term lengths
            return 1
        if int(epicor_days_field) == 0:
            return 1
        return int(epicor_days_field)

    def _sync_salesperson(self, customer: Customer, account: Account):
        # Get epicor salesperson
        epicor_salesperson: Salesperson = self._get_epicor_salesperson(customer)
        if not epicor_salesperson:
            return None

        # Add salesperson to Paperless Account if Paperless salesperson already exists, (match via email)
        epicor_email = epicor_salesperson.EMailAddress.replace("'", "")\
            if epicor_salesperson.EMailAddress is not None else None
        paperless_salesperson = PaperlessSalesperson(
            email=epicor_email,
        )
        account.salesperson = paperless_salesperson

        try:
            account.update()
            logger.info(f"Added salesperson {epicor_salesperson.EMailAddress} to account.")
        except Exception as e:
            # Remove salesperson to prevent subsequent update methods on the account from failing
            account.salesperson = None
            logger.info(f"Salesperson {epicor_salesperson.Name}, ({epicor_salesperson.EMailAddress}) "
                        f"does not map to a Paperless salesperson.\n{e}")

        return epicor_salesperson

    def _get_epicor_salesperson(self, customer: Customer) -> Union[Salesperson, None]:
        epicor_salesperson = None
        try:
            epicor_salesperson = Salesperson.get_by_id(str(customer.SalesRepCode))
        except Exception as e:
            logger.info(f'No salesperson could be located for {customer.EMailAddress}\n{e}')
        return epicor_salesperson
