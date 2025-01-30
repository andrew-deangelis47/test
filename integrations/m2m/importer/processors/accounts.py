from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from baseintegration.utils.address import AddressUtils
from baseintegration.utils import set_blank_to_default_value
from paperless.objects.customers import Account, Contact, Facility, BillingAddress
from paperless.objects.address import Address
from paperless.objects.common import Money
from paperless.exceptions import PaperlessException
import m2m.models as mm
from m2m.settings import IS_TEST
from m2m.configuration import M2MConfiguration
from typing import Tuple


class AccountImportProcessor(BaseImportProcessor):
    _fallback_country_alpha_3 = 'USA'

    def _process(self, account_id: str, config: M2MConfiguration):
        if isinstance(config.default_country_alpha_3, str):
            self._fallback_country_alpha_3 = config.default_country_alpha_3
        m2m_account: mm.Slcdpmx = mm.Slcdpmx.objects.filter(fcustno=account_id).first()

        pp_accounts = Account.filter(erp_code=account_id)
        pp_account: Account
        create = False
        if len(pp_accounts) < 1:
            create = True
            name = m2m_account.fcompany
            pp_accounts_by_name = Account.search(search_term=name)
            number = len(pp_accounts_by_name)
            if number > 0:
                name += f'-{number}'
            pp_account = Account(name=name)
        else:
            pp_account = Account.get(id=pp_accounts[0].id)
        pp_account.erp_code = account_id
        pp_account.url = m2m_account.furl
        pp_account.notes = m2m_account.fmnotes
        pp_account.phone = set_blank_to_default_value(m2m_account.fphone, '')[0:10]
        money: Money = Money(raw_amount=float(m2m_account.fcrlimit))
        pp_account.credit_line = money

        try:
            if create:
                pp_account.create()
            else:
                pp_account.update()
        except PaperlessException:
            logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for account creation which '
                             f'prevented creation for account: {account_id} ')
            return False

        country_alpha_3, state_province_name = \
            AddressUtils.get_country_and_state(country_name=m2m_account.fcountry.strip(),
                                               state_province_name=m2m_account.fstate.strip(),
                                               zipcode=m2m_account.fzip.strip(),
                                               fallback_country_alpha_3=self._fallback_country_alpha_3)

        a_account: Address = Address(address1=m2m_account.fmstreet.strip(), city=m2m_account.fcity.strip(),
                                     state=state_province_name, postal_code=m2m_account.fzip.strip(),
                                     country=country_alpha_3)
        pp_account.sold_to_address = a_account
        try:
            pp_account.update()
        except PaperlessException:
            msg = f' {account_id}, Invalid Sold To Address, street:{a_account.address1} city:{a_account.city} ' \
                  f'state:{a_account.state} zip:{a_account.postal_code} country:{a_account.country}'
            logger.debug(msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                           f'sold to address for account: {account_id} ')
            pp_account = Account.get(id=pp_account.id)

        term, period = AccountImportProcessor.get_payment_terms(m2m_account.fterm)
        pp_account.payment_terms = term
        pp_account.payment_terms_period = period

        try:
            pp_account.update()
        except PaperlessException as e:
            msg = f' {account_id}, Invalid Payment Terms, term:{term} period:{period} with error: {e.message}'
            logger.debug(msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting payment terms update for '
                           f'account: {account_id} ')

        self.create_contacts(account_id, pp_account.id)
        self.create_address(account_id, pp_account.id)

        from django.db import connection
        cursor = connection.cursor()
        row_rev = '0x0000000000000000'
        if not IS_TEST:
            try:
                row_rev_query = f"SELECT " \
                                f"(SELECT MAX(rev_number) " \
                                f"FROM (VALUES (ac.timestamp_column),(addr.timestamp_column),(con.timestamp_column)) " \
                                f"AS UpdateDate(rev_number)) " \
                                f"AS rev_number " \
                                f"FROM slcdpmx as ac " \
                                f"LEFT JOIN syaddr as addr ON ac.fcustno = addr.fcaliaskey " \
                                f"LEFT JOIN syphon as con ON ac.fcustno = con.fcsourceid " \
                                f"WHERE ac.identity_column = '{m2m_account.identity_column}'"
                cursor.execute(row_rev_query)
                result = cursor.fetchall()
                row_rev = f'0x{result[0][0].hex()}'
            finally:
                cursor.close()
                connection.close()
        return row_rev

    def create_contacts(self, m2m_account_id, pp_account_id):
        m2m_contacts = mm.Syphon.objects.filter(fcsourceid=m2m_account_id)
        m2m_contact: mm.Syphon
        pp_contacts = Contact.filter(account_id=pp_account_id)
        for m2m_contact in m2m_contacts:
            create = False
            email = m2m_contact.fcemail.strip()
            if email is None or email == '':
                e_msg = f'{m2m_account_id}, Missing Email, {m2m_contact.fcfname} {m2m_contact.fcontact}'
                logger.debug(e_msg)
                logger.warning(f"Email Address is missing cannot create "
                               f"contact '{m2m_contact.fcfname}' '{m2m_contact.fcontact}' for {m2m_account_id}")
                continue

            pp_contact = None
            for contact in pp_contacts:
                if contact.email == email:
                    pp_contact = Contact.get(id=contact.id)
                    break
            if pp_contact is None:
                create = True
                pp_contact = Contact(account_id=pp_account_id, first_name=m2m_contact.fcfname,
                                     last_name=m2m_contact.fcontact, email=email)
            pp_contact.notes = m2m_contact.fmnotes
            pp_contact.phone = m2m_contact.phonework
            pp_contact.phone_ext = m2m_contact.fcextensio
            try:
                if create:
                    pp_contact.create()
                else:
                    pp_contact.update()
            except PaperlessException as e:
                if 'email' in e.message:
                    logger.warning(f'Email issue prevented contact {pp_contact.first_name} {pp_contact.last_name} '
                                   f'with email {pp_contact.email} from processing '
                                   f'for account: {m2m_account_id} with reason: {e.message}')
                else:
                    logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for contact creation '
                                     f'and we unable to create the contact for account: {m2m_account_id}')
                continue
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(m2m_contact.fccountry.strip(),
                                                                                      m2m_contact.state.strip(),
                                                                                      m2m_contact.postalcode.strip(),
                                                                                      self._fallback_country_alpha_3)
            c_address: Address = Address(address1=m2m_contact.address.strip(), city=m2m_contact.city.strip(),
                                         state=state_province_name, postal_code=m2m_contact.postalcode.strip(),
                                         country=country_alpha_3)
            pp_contact.address = c_address
            try:
                pp_contact.update()
            except PaperlessException:
                a_msg = f' {m2m_account_id}, Invalid Contact Address, street:{c_address.address1} ' \
                        f'city:{c_address.city} state:{c_address.state} zip:{c_address.postal_code} ' \
                        f'country:{c_address.country}'
                logger.debug(a_msg)
                logger.warning('Exception catch in AccountImportProcessor while attempting to add contact address.')

    def create_address(self, m2m_account_id, pp_account_id):
        m2m_addresses = mm.Syaddr.objects.filter(fcaliaskey=m2m_account_id)
        m2m_address: mm.Syaddr
        pp_facilities = Facility.list(account_id=pp_account_id)
        pp_billings = BillingAddress.list(account_id=pp_account_id)
        for m2m_address in m2m_addresses:
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(m2m_address.fccountry.strip(),
                                                                                      m2m_address.fcstate.strip(),
                                                                                      m2m_address.fczip.strip(),
                                                                                      self._fallback_country_alpha_3)
            if m2m_address.fcaddrtype in ['S', 'O']:
                self.add_facility(m2m_account_id, pp_account_id, m2m_address, pp_facilities, state_province_name,
                                  country_alpha_3)
            if m2m_address.fcaddrtype in ['B']:
                self.add_billing(m2m_account_id, pp_account_id, m2m_address, pp_billings, state_province_name,
                                 country_alpha_3)

    @staticmethod
    def add_facility(m2m_account_id, pp_account_id, m2m_address, pp_facilities, state_province_name,
                     country_alpha_3):
        create = False
        pp_address = None
        a_type = 'Sold To' if m2m_address.fcaddrtype == 'O' else 'Shipping'
        name = f'{m2m_address.fccompany}-{a_type}-{m2m_address.fcaddrkey}'
        old_name = f'{m2m_address.fccompany}-{m2m_address.fcaddrkey}'
        for pp_facility in pp_facilities:
            if pp_facility.name == name:
                pp_address = Facility.get(id=pp_facility.id)
                break
            if pp_facility.name == old_name:
                pp_address = Facility.get(id=pp_facility.id)
                pp_facility.name = name
                pp_facility.update()
                break
        if pp_address is None:
            create = True
            pp_address = Facility(account_id=pp_account_id, name=name)
        pp_address.attention = f'{m2m_address.fcfname} {m2m_address.fclname}'
        pp_address.address: Address = Address(address1=m2m_address.fmstreet.strip(),
                                              city=m2m_address.fccity.strip(),
                                              state=state_province_name,
                                              postal_code=m2m_address.fczip.strip(),
                                              country=country_alpha_3)
        try:
            if create:
                pp_address.create(account_id=pp_account_id)
            else:
                pp_address.update()
        except PaperlessException:
            f_msg = f' {m2m_account_id}, Invalid Facility Address, street:{pp_address.address.address1}  ' \
                    f'city:{pp_address.address.city} state:{pp_address.address.state} ' \
                    f'zip:{pp_address.address.postal_code}  country:{pp_address.address.country}'
            logger.debug(f_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Facility address: {m2m_account_id}-{a_type}-{m2m_address.fcaddrkey}')

    @staticmethod
    def add_billing(m2m_account_id, pp_account_id, m2m_address, pp_billings, state_province_name,
                    country_alpha_3):
        pp_address = None
        for pp_billing in pp_billings:
            if pp_billing.address1 == m2m_address.fmstreet and pp_billing.city == m2m_address.fccity and \
                    pp_billing.country == country_alpha_3 and pp_billing.state == m2m_address.fcstate and \
                    pp_billing.postal_code == m2m_address.fczip:
                pp_address = BillingAddress.get(id=pp_billing.id)
                break
        if pp_address is not None:
            return
        pp_address = BillingAddress(address1=m2m_address.fmstreet.strip(), city=m2m_address.fccity.strip(),
                                    state=state_province_name, postal_code=m2m_address.fczip.strip(),
                                    country=country_alpha_3)
        try:
            pp_address.create(account_id=pp_account_id)
        except PaperlessException:
            b_msg = f' {m2m_account_id}, Invalid Billing Address, street:{pp_address.address1} ' \
                    f'city:{pp_address.city} state:{pp_address.state} zip:{pp_address.postal_code} ' \
                    f'country:{pp_address.country}'
            logger.debug(b_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Billing address: {m2m_account_id}-Billing-{m2m_address.fcaddrkey}')

    @staticmethod
    def get_payment_terms(term_code: str) -> Tuple[str, int]:

        from django.db import connection
        cursor = connection.cursor()
        terms = None
        if not IS_TEST:
            try:
                terms_query = f"SELECT fcdescr, fnduedays FROM UTTERMS WHERE fctermsid = '{term_code}'"
                cursor.execute(terms_query)
                terms = cursor.fetchone()
            finally:
                cursor.close()
                connection.close()
        term = 'NET 30'
        period = '30'
        if terms is not None:
            term = terms[0].strip()
            period = terms[1]
        return term, int(period)
