import decimal
from decimal import Decimal
from typing import List
from paperless.exceptions import PaperlessException
from paperless.objects.common import Salesperson as PPSalesperson, Money

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import clean_up_phone_number, \
    create_or_update_account
from globalshop.customer import Customer, CustomerRecord, Contact, \
    ContactRecord, CustomerShipTo, CustomerShipToRecord
from globalshop.salesperson import Salesperson as GSSalesperson
from paperless.objects.customers import Account, Contact as \
    PaperlessContact, ContactList, Facility, BillingAddress
from paperless.objects.address import Address
from baseintegration.utils.data import safe_trim
from baseintegration.integration import logger
import re


class AccountImportProcessor(BaseImportProcessor):

    def get_payment_terms_and_period(self, customer: CustomerRecord):
        # Defaults
        terms = 'Net 30'
        period = 30
        if customer.terms is not None:
            terms = customer.terms.strip()
            terms_lower = terms.lower()
            if 'net 30' in terms_lower:
                period = 30
            elif 'net 15' in terms_lower:
                period = 15
            elif 'net 10' in terms_lower:
                period = 10
            elif 'net 21' in terms_lower:
                period = 21
            elif 'net 45' in terms_lower:
                period = 45
            elif 'net 60' in terms_lower:
                period = 60
            elif 'net 90' in terms_lower:
                period = 90
            elif 'net 40' in terms_lower:
                period = 40
            elif 'net 75' in terms_lower:
                period = 75
        return terms, period

    def _process(self, account_id: str) -> Account:
        logger.info(f'processing account id: {account_id}')
        customer_rec, account = self._process_account(account_id)
        self._process_facility(gss_customer_id=account_id, pp_account_id=account.id)
        self._process_contacts(customer_rec, pp_account_id=account.id)
        self._process_salesperson(pp_account=account, gs_customer=customer_rec)
        self._process_billing_address(pp_account=account, gs_customer=customer_rec)
        return account

    def _process_facility(self, gss_customer_id: str, pp_account_id: str):
        logger.info('processing facilities')
        pp_facilities = Facility.list(account_id=pp_account_id)

        customer_ship_tos = CustomerShipTo.select(gss_customer_id)
        logger.info(f'ship tos: {len(customer_ship_tos)}')
        for ship_to in customer_ship_tos:
            logger.info(f'ship to {ship_to}')
            country = 'USA'
            if ship_to.city and ship_to.state and ship_to.zip and ship_to.address1:
                # country, state = AddressUtils.get_country_and_state(country_name=country,
                #                                                     state_province_name=ship_to.state,
                #                                                     zipcode=ship_to.zip,
                #                                                     fallback_country_alpha_3='USA')

                ship_to_address = Address(city=safe_trim(ship_to.city),
                                          state=safe_trim(ship_to.state),
                                          postal_code=safe_trim(ship_to.zip),
                                          country=safe_trim(country),
                                          address1=safe_trim(ship_to.address1),
                                          address2=safe_trim(ship_to.address2))
                logger.info(f'ship to {ship_to_address}')
                try:
                    facility = self.get_matching_pp_facility(ship_to, pp_facilities)
                    if not facility:
                        facility = Facility(
                            address=ship_to_address,
                            name=ship_to.ship_seq,
                            attention=ship_to.name_customer_ship,
                        )
                        logger.info(f'Creating new facility {facility.name} for account {gss_customer_id}')
                        facility.create(pp_account_id)
                    else:
                        facility.address = ship_to_address
                        facility.name = ship_to.ship_seq
                        facility.attention = ship_to.name_customer_ship
                        logger.info(f'Updating facility {facility.name} for account {gss_customer_id}')
                        facility.update()
                except Exception as e:
                    logger.info(f"Encountered error importing shipping address for account {gss_customer_id}.  Error: {e}")

    def get_matching_pp_facility(self, gss_ship_to: CustomerShipToRecord, pp_facilities: List[Facility]) -> Facility:
        # TODO - Once we have ERP codes for facilities, use the ShipTo_ID instead of the location name to check for
        #  matching records
        ship_to_id = gss_ship_to.ship_seq
        facility = None
        for f in pp_facilities:
            if f.name == ship_to_id:
                facility = f
                logger.info(f'facility: {facility} Ship to: {ship_to_id}')
        return facility

    def _process_account(self, account_id: str) -> (CustomerRecord, Account):
        rec = Customer.get(account_id)
        logger.info(f'Got GS Customer: {rec}')
        erp_code = safe_trim(rec.gss_customer_number)

        account, account_is_new = create_or_update_account(
            integration=self._importer._integration,
            erp_code=erp_code,
            account_name=rec.customer_name)

        account.phone = clean_up_phone_number(safe_trim(rec.phone))

        # account.notes = rec.
        account.payment_terms, account.payment_terms_period = self.get_payment_terms_and_period(rec)

        # FIXME: Credit doesn't appear to always be a number, need to handle
        credit_line: str = rec.credit_limit if rec.credit_limit else None

        if credit_line:
            try:
                credit_line_decimal = Decimal(re.sub(r'[^\d.]', '', credit_line))
                account.credit_line = Money(credit_line_decimal)
            except decimal.InvalidOperation:
                logger.info(f'Could not parse credit line from string: {credit_line}')
                pass

        # account.url =
        # account.billing_addresses

        city = safe_trim(rec.city)
        state = safe_trim(rec.state)
        zip = safe_trim(rec.zip)
        # TODO: ensure conversion of non-ISO compliant 3 character countries
        country = safe_trim(rec.country)
        address1 = safe_trim(rec.address_1)
        address2 = safe_trim(rec.address_2)

        sold_to_address = None
        # country, state = AddressUtils.get_country_and_state(country_name=country,
        #                                                     state_province_name=state,
        #                                                     zipcode=zip,
        #                                                     fallback_country_alpha_3='USA')

        if city and state and zip and address1:
            country = 'USA'
            sold_to_address = Address(city=city,
                                      state=state,
                                      postal_code=zip,
                                      country=country,
                                      address1=address1,
                                      address2=address2)

        if sold_to_address:
            account.sold_to_address = sold_to_address
            logger.info(sold_to_address)

        if account_is_new is False:
            # We have an existing ID, update it!
            account.id = account.id
            account.update()
        else:
            # We don't have an existing account, create one:
            account.create()
        return rec, account

    def _process_billing_address(self, pp_account: Account, gs_customer: CustomerRecord):
        # Pull down the related billing addresses
        city = safe_trim(gs_customer.city)
        state = safe_trim(gs_customer.state)
        zip = safe_trim(gs_customer.zip)
        # TODO: ensure conversion of non-ISO compliant 3 character countries
        # country = safe_trim(gs_customer.country)
        country = 'USA'
        address1 = safe_trim(gs_customer.address_1)
        address2 = safe_trim(gs_customer.address_2)
        if address2 is not None and address2 == '':
            address2 = None
        pp_billing_addresses = pp_account.billing_addresses
        pp_billing_address = self.get_matching_pp_billing_address(gs_customer.gss_customer_number, pp_billing_addresses)

        is_billing_address_new = False
        if pp_billing_address is None:
            is_billing_address_new = True

        if city and state and zip and address1:

            if is_billing_address_new:
                pp_billing_address = BillingAddress(
                    address1=address1,
                    address2=address2,
                    city=city,
                    country=country,
                    postal_code=zip,
                    state=state,
                    erp_code=safe_trim(gs_customer.gss_customer_number))
            else:
                pp_billing_address.address1 = address1
                pp_billing_address.address2 = address2
                pp_billing_address.city = city
                pp_billing_address.country = country
                pp_billing_address.postal_code = zip
                pp_billing_address.state = state

            try:
                if is_billing_address_new:
                    logger.info(
                        f'Creating new billing address for account {gs_customer.gss_customer_number}')
                    pp_billing_address.create(pp_account.id)
                else:
                    logger.info(f'Updating billing address for account {gs_customer.gss_customer_number}')
                    pp_billing_address.update()
            except Exception as e:
                logger.info(f'Failed to create/update billing address for account | {str(e)}')

    def _process_contacts(self, customer_rec: CustomerRecord,
                          pp_account_id: int
                          ) -> [ContactRecord]:
        logger.info(f'processing contacts for GS/PP account id:'
                    f' {customer_rec.gss_customer_number}/{pp_account_id}')
        # Select all GS contacts associated with account:
        contacts = Contact.select(customer_rec.gss_customer_number)
        logger.info(f'{len(contacts)} selected')

        # Check if each exist already in PP:
        paperless_contacts: [ContactList] = PaperlessContact.filter(
            account_id=pp_account_id)

        # Store them by email for lookup without lots of filtering searches
        # on the API
        pp_contact_dict = {}
        for cnt in paperless_contacts:
            pp_contact_dict[cnt.email.lower()] = cnt

        for contact in contacts:
            try:
                self._process_contact(contact=contact,
                                      pp_account_id=pp_account_id,
                                      pp_contact_dict=pp_contact_dict)
            except Exception as e:
                logger.warning(
                    f"Error processing Global Shop contact: {contact}")
                logger.exception(e)

    def _process_contact(self, contact: ContactRecord, pp_account_id: int,
                         pp_contact_dict: dict):

        pp_contact_id = None
        email = safe_trim(contact.email1)
        if email:
            email = re.split(' |,|;', email.lower())[0]
            pp_contact: PaperlessContact = pp_contact_dict.get(email)
            pp_contact_id = pp_contact.id if pp_contact else None

        # We need certain fields to be filled in to integrate:
        first_name = safe_trim(contact.first_name)
        last_name = safe_trim(contact.last_name)
        logger.debug(f'Processing GS contact: {contact}')
        if first_name and last_name and email:
            pp_contact = PaperlessContact(account_id=pp_account_id,
                                          email=email,
                                          first_name=first_name,
                                          last_name=last_name)
            # TODO:
            # address=,
            # notes=,

            phone = clean_up_phone_number(safe_trim(contact.phone1))
            phone_ext = safe_trim(contact.ext1)
            if phone:
                # logger.debug(f"phone: '{phone}' ext: '{phone_ext}'")
                phone = clean_up_phone_number(phone)
                pp_contact.phone = phone
                if phone_ext:
                    pp_contact.phone_ext = phone_ext

            if pp_contact_id:
                pp_contact.id = pp_contact_id
                pp_contact.update()
            else:
                pp_contact.create()

    def _process_salesperson(self, pp_account: Account,
                             gs_customer: CustomerRecord):
        """
        For the salesperson code set on the customer in GS, look it up
        and add the email as a salesperson in PP
        """
        pp_sales = None
        try:
            sp_code = safe_trim(gs_customer.salesperson_code)
            if sp_code:
                gs_sales = GSSalesperson.get(sp_code)
                if gs_sales is None:
                    logger.warning(f"Could not find salesperson in GS for sp_code: {sp_code}")
                    return

                names = gs_sales.name.split(' ', 1)
                first = names[0] if len(names) > 0 else ""
                last = names[1] if len(names) > 1 else ""
                if gs_sales.email is None:
                    return

                pp_sales = PPSalesperson(email=safe_trim(gs_sales.email),
                                         first_name=safe_trim(first),
                                         last_name=safe_trim(last))

                pp_account.salesperson = pp_sales
                pp_account.update()
        except PaperlessException as e:
            if 'Invalid Salesperson' in e.message:
                logger.warning(f"Invalid Salesperson email: {pp_sales.email}"
                               f"for customer record {pp_account.erp_code} "
                               f"unable to be added to account {pp_account.id}"
                               )
            else:
                logger.exception(e)

    def get_matching_pp_billing_address(self, gs_account,
                                        pp_billing_addresses: List[BillingAddress]):
        billing_address_id = str(gs_account)
        matching_billing_address = None
        for b in pp_billing_addresses:
            if b.erp_code == billing_address_id:
                matching_billing_address = b
        return matching_billing_address
