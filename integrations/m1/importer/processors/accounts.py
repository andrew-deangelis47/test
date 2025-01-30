import re

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from baseintegration.utils.address import AddressUtils
from paperless.objects.customers import Account, Contact, Facility, BillingAddress
from paperless.objects.address import Address
from paperless.objects.common import Money
from paperless.exceptions import PaperlessException

from m1.constants import DEFAULT_PAYMENT_TERM_MAP
from m1.models import Organizations, Organizationlocations, Organizationcontacts, Paymentterms
from typing import Tuple


class AccountImportProcessor(BaseImportProcessor):
    _fallback_country_alpha_3 = 'USA'

    def _process(self, organizations_id: str):
        m1_account: Organizations = Organizations.objects.filter(cmoorganizationid=organizations_id)[0]

        pp_accounts = Account.filter(erp_code=organizations_id)
        pp_account: Account = None
        if len(pp_accounts) < 1:
            name = m1_account.cmoname
            pp_accounts_by_name = Account.search(search_term=name)
            for item in pp_accounts_by_name:
                if item.erp_code is None and item.name == name:
                    logger.info(f"Account {organizations_id} found by Name match - {name}")
                    pp_account = Account.get(id=item.id)
                    pp_account.erp_code = organizations_id
                    pp_account.update()
                    break
            if pp_account is None:
                number = len(pp_accounts_by_name)
                if number > 0:
                    name += f'-{number}'
                pp_account = Account(name=name, erp_code=organizations_id)
                pp_account.create()
        else:
            pp_account = Account.get(id=pp_accounts[0].id)
        pp_account.erp_code = organizations_id
        web_url: str = m1_account.cmowebaddress
        pp_account.url = web_url.lower() if web_url else ''
        pp_account.phone = self.scrub_phone_number(m1_account.cmophonenumber)
        money: Money = Money(raw_amount=float(m1_account.cmocustomercreditlimit))
        pp_account.credit_line = money if money.raw_amount is not None and money.raw_amount > 0.00 else None

        try:
            pp_account.update()
        except PaperlessException:
            logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for account creation which '
                             f'prevented creation for account: {organizations_id} ')
            return False

        country_alpha_3, state_province_name = \
            AddressUtils.get_country_and_state(country_name=m1_account.cmocountry.strip(),
                                               state_province_name=m1_account.cmostate.strip(),
                                               zipcode=m1_account.cmopostcode.strip(),
                                               fallback_country_alpha_3=self._fallback_country_alpha_3)

        a_account: Address = Address(address1=m1_account.cmoaddressline1.strip(),
                                     address2=m1_account.cmoaddressline2.strip(), city=m1_account.cmocity.strip(),
                                     state=state_province_name, postal_code=m1_account.cmopostcode.strip(),
                                     country=country_alpha_3)
        pp_account.sold_to_address = a_account
        try:
            pp_account.update()
        except PaperlessException:
            msg = f' {organizations_id}, Invalid Sold To Address, street:{a_account.address1} city:{a_account.city} ' \
                  f'state:{a_account.state} zip:{a_account.postal_code} country:{a_account.country}'
            logger.debug(msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                           f'sold to address for account: {organizations_id} ')
            pp_account = Account.get(id=pp_account.id)

        if m1_account.cmocustomerpaymenttermsid:
            term, period = self.get_payment_terms(m1_account.cmocustomerpaymenttermsid)
            pp_account.payment_terms = term
            pp_account.payment_terms_period = period

        try:
            pp_account.update()
        except PaperlessException as e:
            msg = f' {organizations_id}, Invalid Payment Terms, term:{term} period:{period} with error: {e.message}'
            logger.debug(msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting payment terms update for '
                           f'account: {organizations_id} ')

        self.create_contacts(organizations_id, pp_account.id)
        self.create_address(organizations_id, pp_account.id)

        return True

    def create_contacts(self, m1_organizations_id: str, pp_account_id: str):
        m1_contacts = Organizationcontacts.objects.filter(cmcorganizationid=m1_organizations_id)
        m1_contact: Organizationcontacts
        pp_contacts = Contact.filter(account_id=pp_account_id)
        for m1_contact in m1_contacts:
            create = False
            if m1_contact.cmcemailaddress is None or m1_contact.cmcemailaddress.strip() == '':
                e_msg = f'{m1_organizations_id}, Missing Email, {m1_contact.cmcname}'
                logger.debug(e_msg)
                logger.warning(f"Email Address is missing cannot create "
                               f"contact '{m1_contact.cmcname}' '{m1_contact.cmccontactid}' for {m1_organizations_id}")
                continue

            pp_contact = None
            email = m1_contact.cmcemailaddress.strip()
            name_split = m1_contact.cmcname.strip().split(' ', 1)
            first_name = name_split[0]
            last_name = '_'
            if name_split[-1] != name_split[0]:
                last_name = name_split[-1]
            for contact in pp_contacts:
                if contact.email.strip() == email:
                    pp_contact = Contact.get(id=contact.id)
                    break
            if pp_contact is None:
                create = True
                pp_contact = Contact(account_id=int(pp_account_id), first_name=first_name, last_name=last_name,
                                     email=email)
            pp_contact.first_name = first_name
            pp_contact.last_name = last_name
            pp_contact.notes = m1_contact.cmcnotetext
            pp_contact.phone = self.scrub_phone_number(m1_contact.cmcphonenumber)
            try:
                if create:
                    pp_contact.create()
                else:
                    pp_contact.update()
            except PaperlessException as e:
                if 'email' in e.message:
                    logger.warning(f'Email issue prevented contact {pp_contact.first_name} {pp_contact.last_name} '
                                   f'with email {pp_contact.email} from processing '
                                   f'for account: {m1_organizations_id} with reason: {e.message}')
                else:
                    logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for contact creation '
                                     f'and we unable to create the contact for account: {m1_organizations_id}')
                continue

    def create_address(self, m1_organizations_id: str, pp_account_id: str):
        m1_locations: [Organizationlocations] = Organizationlocations.objects.filter(
            cmlorganizationid=m1_organizations_id)
        pp_facilities = Facility.list(account_id=pp_account_id)
        pp_billings = BillingAddress.list(account_id=pp_account_id)
        for m1_location in m1_locations:
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(m1_location.cmlcountry.strip(),
                                                                                      m1_location.cmlstate.strip(),
                                                                                      m1_location.cmlpostcode.strip(),
                                                                                      self._fallback_country_alpha_3)
            if m1_location.cmlquotelocation:
                self.add_billing(m1_organizations_id, pp_account_id, m1_location, pp_billings, state_province_name,
                                 country_alpha_3)
            else:
                self.add_facility(m1_organizations_id, pp_account_id, m1_location, pp_facilities, state_province_name,
                                  country_alpha_3)

    @staticmethod
    def add_facility(m1_organizations_id: str, pp_account_id: str, m1_location: Organizationlocations,
                     pp_facilities: [Facility], state_province_name: str, country_alpha_3: str):
        create = False
        pp_address = None
        name = m1_location.cmlname
        for pp_facility in pp_facilities:
            if pp_facility.name == name:
                pp_address = Facility.get(id=pp_facility.id)
                break
        if pp_address is None:
            create = True
            pp_address = Facility(account_id=pp_account_id, name=name)
        pp_address.address = Address(address1=m1_location.cmladdressline1.strip(),
                                     address2=m1_location.cmladdressline2.strip(),
                                     city=m1_location.cmlcity.strip(),
                                     state=state_province_name, postal_code=m1_location.cmlpostcode.strip(),
                                     country=country_alpha_3)
        try:
            if create:
                pp_address.create(account_id=pp_account_id)
            else:
                pp_address.update()
        except PaperlessException:
            f_msg = f' {m1_organizations_id}, Invalid Facility Address, street:{pp_address.address.address1}  ' \
                    f'city:{pp_address.address.city} state:{pp_address.address.state} ' \
                    f'zip:{pp_address.address.postal_code}  country:{pp_address.address.country}'
            logger.debug(f_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Facility address: {m1_organizations_id}-{m1_location.cmlname}')

    @staticmethod
    def add_billing(m1_organizations_id: str, pp_account_id: str, m1_location: Organizationlocations,
                    pp_billings: [BillingAddress], state_province_name: str, country_alpha_3: str):
        for pp_billing in pp_billings:
            if pp_billing.address1 == m1_location.cmladdressline1.strip() and \
                    pp_billing.city == m1_location.cmlcity.strip() and \
                    pp_billing.country == country_alpha_3 and pp_billing.state == state_province_name and \
                    pp_billing.postal_code == m1_location.cmlpostcode.strip() and \
                    pp_billing.address2 == m1_location.cmladdressline2.strip():
                return
        pp_address = BillingAddress(address1=m1_location.cmladdressline1.strip(),
                                    address2=m1_location.cmladdressline2.strip(),
                                    city=m1_location.cmlcity.strip(),
                                    state=state_province_name, postal_code=m1_location.cmlpostcode.strip(),
                                    country=country_alpha_3)
        try:
            pp_address.create(account_id=pp_account_id)
        except PaperlessException:
            b_msg = f' {m1_organizations_id}, Invalid Billing Address, street:{pp_address.address1} ' \
                    f'city:{pp_address.city} state:{pp_address.state} zip:{pp_address.postal_code} ' \
                    f'country:{pp_address.country}'
            logger.debug(b_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Billing address: {m1_organizations_id}-Billing-{m1_location.cmlname}')

    @staticmethod
    def scrub_phone_number(phone_num: str) -> str:
        """
        This method takes a string value of an M1 phone number and strips all non-numeric character leaving
        only 1 tru 9. Then it takes the first 10 character of the striped substring.  This is done to adhere to
        Paperless Parts Open API constraints.

        @param phone_num: a string value of an M1 phone number
        @type phone_num: str
        @return: A strip down string limited to 10 characters
        @rtype: str
        """
        return re.sub('[^0-9]', '', phone_num)[0:10]

    @staticmethod
    def get_payment_terms(term_code: str = 'NET30') -> Tuple[str, int]:
        """
        This method takes a string value of an M1 payment term ID and find it M1 SQL DB record.  The method does do a
        mapping check between default M1 term IDs with default Paperless Parts payment term names.  If a match is found
        the Paperless Parts Payment Term equivalent will be used.

        @param term_code: a string value of an M1 payment term ID
        @type term_code: str
        @return: A string value of an M1 payment term ID and its corresponding payment integer period in days.  Default
        values if parameter 'term_code' is passed in as empty are term description 'Net 30' and term period 30.
        @rtype: str, int
        """

        term = 'Net 30'
        period = 30
        if term_code and term_code != '':
            m1_terms: Paymentterms = Paymentterms.objects.filter(xatpaymenttermid=term_code)[0]

            default_term_map = DEFAULT_PAYMENT_TERM_MAP

            term = m1_terms.xatpaymenttermid

            if m1_terms.xatpaymenttermid in default_term_map:
                term = default_term_map[m1_terms.xatpaymenttermid]
            period = m1_terms.xatdaysdue
        return term, int(period)
