from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order
from paperless.objects.customers import Account, Address, BillingAddress, Facility, Contact, ContactList
from m1.models import Organizations, Organizationlocations, Organizationcontacts
from django.db.utils import IntegrityError


class ScrubbedAddress:
    address_line1 = ''
    address_line2 = ''
    city = ''
    county = ''
    state = ''
    postcode = ''
    country = ''

    def __init__(self, address: Address):
        if address is not None:
            self.address_line1 = address.address1
            self.address_line2 = address.address2
            self.city = address.city
            self.postcode = address.postal_code
            self.state = address.state
            self.country = address.country


class ProcessOrganization(BaseProcessor):

    def _process(self, order: Order):
        if order.contact.account is None:
            logger.warning(f'Order {order.number}: ERP Code Missing Export Bailing')
            return False

        if order.contact.account.erp_code:
            erp_code = order.contact.account.erp_code
            org_list: list[Organizations] = Organizations.objects.filter(cmoorganizationid=erp_code)
        else:
            org_list = []

        if len(org_list) > 0:
            logger.info('Organizations already exists in M1, Using first record....')
            org = org_list[0]
        else:
            logger.info('Organizations does not already exists in M1, Create one....')
            account: Account = Account.get(id=order.contact.account.id)
            org = self.create_organization(account=account)
            account.erp_code = org.cmoorganizationid
            account.update()
            self.create_organization_location(org, account.sold_to_address, '')
            self.create_billing_address(org, account)
            self.create_facility_address(org, account)
            contact_list: ContactList = Contact.filter(account_id=account.id)
            for contact_item in contact_list:
                contact = Contact.get(id=contact_item.id)
                self.create_organization_contact(org, contact)

        return org

    def create_billing_address(self, org: Organizations, account: Account):
        pp_billings: [BillingAddress] = BillingAddress.list(account_id=account.id)
        idx = 1
        for address in pp_billings:
            self.create_organization_location(org=org, address=address, name=f'B-{idx}', quote_location=True)
            idx += 1

    def create_facility_address(self, org: Organizations, account: Account):
        pp_facilities: [Facility] = Facility.list(account_id=account.id)
        idx = 1
        for facility in pp_facilities:
            if facility.name and facility != '':
                name = facility.name
            else:
                name = f'F-{idx}'
                idx += 1
            self.create_organization_location(org=org, address=facility.address, name=name)

    def create_organization(self, account: Account):

        credit_line = account.credit_line.raw_amount if account.credit_line else 0.00

        addr = ScrubbedAddress(address=account.sold_to_address)

        if account.erp_code:
            code = self.generate_m1_org_id(account.erp_code)
        else:
            code = f'PP-{account.id}'
        try:
            org = Organizations.objects.create(
                cmoorganizationid=code,
                cmoname=account.name,
                cmoaddressline1=addr.address_line1,
                cmoaddressline2=addr.address_line2,
                cmoaddressline3='',
                cmocity=addr.city,
                cmocounty=addr.county,
                cmostate=addr.state,
                cmopostcode=addr.postcode,
                cmocountry=addr.country,
                cmophonenumber=account.phone,
                cmowebaddress=account.url if account.url else '',
                cmoprintstatement=False,
                cmoemployeecount=0,
                cmofinancecompany=False,
                cmocompetitor=False,
                cmolongdescriptionrtf=account.notes,
                cmolongdescriptiontext=account.notes,
                cmocustomerstatus=2,
                cmosupplierstatus=0,
                cmorequires1099=False,
                cmosuppliertaxable=False,
                cmocustomertaxable=(account.tax_exempt is False),
                cmocalculatefinancecharges=False,
                cmoincludefreightinprice=False,
                cmocredithold=False,
                cmocustomercreditlimit=credit_line,
                cmodirectpayment=False,
                cmoarinvoicepershipmentline=False,
                cmocreatedfromweb=False,
                cmoresellerstatus=0,
                cmoresellercommissionrate=0.00,
                cmorequiresinspection=False,
                cmoresidentialaddress=False,
                cmosupplieraccredited=False,
                cmocreatedby='ppadmin',
                cmoapincludetaxinretention=False,
                cmoarincludetaxinretention=False,
                cmoform1099box=0,
                cmoavalaraaddressvalidated=False,
                cmocontractor=False,
                cmotaxreportable=False,
                cmocreatedfrommobile=False,
                cmoignoreavalara=False,
                cmosuperfund=False,
                cmoupsvalidated=False,
                cmobarecostofduty=False,
                cmobaretransportationcost=False,
                cmoediintegrated=False,
                cmosplitpercenttotal=0.00,
                cmoexpensesplitpercenttotal=0.00,
                cmojobpriorityid=0
            )

        except IntegrityError as e:  # pragma: no cover
            if "with unique index 'CMOORGANIZATIONID'" in str(e) and account.erp_code is None:
                logger.warning(f'M1 already has an organization with id {code} somehow the erp code link was lost.')
                org_list: list[Organizations] = Organizations.objects.filter(cmoorganizationid=code)

                if len(org_list) > 0:
                    org = org_list[0]
            else:
                logger.exception(f'Failed to export account to M1 {account.name}')

        return org

    @staticmethod
    def generate_m1_org_id(erp_code: str) -> str:
        """
        When creating a new organization in M1 we need to scrub the Paperless Parts ERP Code:
        - remove whitespace
        - limit to the first 10 characters
        - Cast all characters to upper case

        @param erp_code: a string value of an M1 payment term ID
        @type erp_code: str
        @return: A string value to be used as a M1 organization ID
        @rtype: str
        """
        stripped = erp_code.strip()
        replace = stripped.replace(" ", "")
        org_id = "".join(replace.split())
        return org_id.upper()[0:10]

    @staticmethod
    def create_organization_location(org: Organizations, address: Address, name: str,
                                     quote_location: bool = False):

        addr = ScrubbedAddress(address=address)
        try:
            Organizationlocations.objects.create(
                cmlorganizationid=org.cmoorganizationid,
                cmllocationid=name,
                cmlname=org.cmoname if name == '' else name,
                cmladdressline1=addr.address_line1,
                cmladdressline2=addr.address_line2,
                cmlcity=addr.city,
                cmlcounty=addr.county,
                cmlstate=addr.state,
                cmlpostcode=addr.postcode,
                cmlcountry=addr.country,
                cmlphonenumber=org.cmophonenumber if name == '' else '',
                cmlquotelocation=quote_location,
                cmlshiplocation=False,
                cmlarinvoicelocation=False,
                cmlpurchaselocation=False,
                cmlapinvoicelocation=False,
                cmlcustomertaxable=org.cmocustomertaxable if name == '' else False,
                cmlarinvoicepershipmentline=False,
                cmlinactive=False,
                cmlresidentialaddress=False,
                cmlcreditcheckforlocation=False,
                cmlcustomercreditlimit=org.cmocustomercreditlimit if name == '' else 0.00,
                cmlcredithold=False,
                cmldirectpayment=False,
                cmlcreatedby='ppadmin',
                cmlavalaraaddressvalidated=False,
                cmlcontractor=False,
                cmltaxreportable=False,
                cmlcreatedfrommobile=False,
                cmlbarecostofduty=False,
                cmlbaretransportationcost=False,
                cmlignoreavalara=False,
                cmlupsvalidated=False,
                cmlediintegrated=False,
                cmlsplitpercenttotal=0.00
            )
        except IntegrityError as e:  # pragma: no cover
            if "with unique index 'CMLORGANIZATIONID_CMLLOCATIONID'" in str(e):
                logger.warning(f'Export failed for account address with {name}, since it already exist for this '
                               f'organization.')
            else:
                logger.exception('Export failed for account address into M1')

    @staticmethod
    def create_organization_contact(org: Organizations, contact: Contact):
        try:
            Organizationcontacts.objects.create(
                cmcorganizationid=org.cmoorganizationid,
                cmclocationid='',
                cmccontactid=f'{contact.first_name[0:3]}{contact.last_name[0:2]}',
                cmcname=f'{contact.first_name} {contact.last_name}',
                cmcphonenumber=contact.phone,
                cmcemailaddress=contact.email,
                cmcwebloginenabled=False,
                cmcnomailings=False,
                cmcnotertf=contact.notes,
                cmcnotetext=contact.notes,
                cmcinactive=False,
                cmccreatedfrommobile=False,
                cmccreatedby='ppadmin',
                cmceasyorderenabled=False,
                cmccreatedbyeasyorder=False,
                cmceoeditshippingaddress=False,
                cmceoreceiveemails=False,
                cmceohtmlmail=False,
                cmceoreminderofopenorders=False,
                cmceoorderauthorisationmessage=False,
                cmceoauthorisationrequest=False,
                cmceomaynotcreordtemp=False,
            )

        except IntegrityError as e:  # pragma: no cover
            if "unique index 'CMCORGANIZATIONID_CMCLOCATIONID_CMCCONTACTID'" in str(e):
                logger.warning(f'Export failed for contact {contact.first_name} {contact.last_name} - {contact.email}'
                               f' m1 already has another contact with this id '
                               f'{contact.first_name[0:3]}{contact.last_name[0:2]} for this organization '
                               f'{org.cmoorganizationid}')
            else:
                logger.exception(f'An exception happened while exporting contact {contact.first_name} '
                                 f'{contact.last_name} - {contact.email} to m1')
