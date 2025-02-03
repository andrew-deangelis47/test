from baseintegration.utils.operations import OperationUtils
from typing import List
from plex_v2.configuration import PlexConfig
from plex_v2.objects.part import Part
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.routing import PartOperation
from plex_v2.objects.part_get_datasource import PartGetDataSource
from plex_v2.objects.routing import Operation
from plex_v2.objects.approved_supplier import ApprovedSupplierPurchasing, ApprovedSupplierGetDatasource
from plex_v2.objects.supplier import Supplier, SupplierGetDatasource
from plex_v2.objects.part_operation_key_get_datasource import PartOperationKeyGetDatasource
from baseintegration.datamigration import logger
from paperless.exceptions import PaperlessException
from paperless.objects.customers import Account, Contact, Facility, BillingAddress, Address
from plex_v2.objects.customer import Customer, CustomerContact, CustomerAddress
from baseintegration.utils.address import AddressUtils
from paperless.objects.purchased_components import PurchasedComponent
from paperless.client import PaperlessClient


class ImportUtils:

    config: PlexConfig
    operation_utils: OperationUtils
    default_country: str

    def __init__(self, config: PlexConfig, utils: OperationUtils):
        self.config = config
        self.operation_utils = utils
        self.default_country = 'USA'

    def get_custom_table_rows(self, custom_table_name: str):
        client = PaperlessClient.get_instance()

        try:
            response = client.request(f'suppliers/public/custom_tables/{custom_table_name}', data={}, method="get")
            return response.json()["rows"]
        except Exception as e:
            raise CancelledIntegrationActionException(f'Error reading from "{custom_table_name}" table: {str(e)}')

    # ------------------- Part Functions -------------------

    def audit_pp_pc_list(self, pc_list: List[PurchasedComponent]):
        """
        checks on existing PC list for the following criteria and removes if not
        - is the status in the table valid
        - is the type in the table valid
        """
        plex_part_list: List[Part] = Part.search()
        plex_part_no_list: List[str] = [part.number for part in plex_part_list]
        pc: PurchasedComponent
        for pc in pc_list:
            # check that it exists in Plex
            if pc.oem_part_number not in plex_part_no_list:
                logger.info(f'Removing component {pc.oem_part_number} from list in Paperless, part no longer exists in Plex')
                try:
                    pc.delete()
                except Exception:
                    pass

            # check status
            elif pc.get_property('status') not in self.config.part_statuses_active:
                logger.info(f'Removing component {pc.oem_part_number} from list in Paperless, invalid status of {pc.get_property("status")}')
                try:
                    pc.delete()
                except Exception:
                    pass

            # check type
            elif pc.get_property('part_type') not in self.config.purchased_component_types:
                logger.info(f'Removing component {pc.oem_part_number} from list in Paperless, invalid type of {pc.get_property("part_type")}')
                try:
                    pc.delete()
                except Exception:
                    pass

    def get_part_op_key_from_op_code_and_part_key(self, op_code: str, part_key: int) -> int:
        part_op_key_datasources: List[PartOperationKeyGetDatasource] = PartOperationKeyGetDatasource.get(op_code, part_key)

        if len(part_op_key_datasources) == 0:
            logger.info(f'Could not find part operation key for part key {part_key} and operation code {op_code}')
            return None

        return part_op_key_datasources[0].Part_Operation_Key

    def get_supplier_material_price_and_price_unit(self, part: Part, part_key: int, part_op_key: int, supplier_no: int):
        suppliers: List[ApprovedSupplierGetDatasource] = ApprovedSupplierGetDatasource.get(part_key, part_op_key, supplier_no)

        if len(suppliers) == 0:
            logger.info(f'Could not find supplier price for part {part.number}')
            return None

        if len(suppliers) > 1:
            logger.info(f'Found multiple supplier prices for part {part.number}, using the first one')

        return suppliers[0]

    def get_supplier_no_from_supplier_code(self, supplier_code: str):
        suppliers: List[SupplierGetDatasource] = SupplierGetDatasource.get(supplier_code)

        if len(suppliers) == 0:
            logger.info(f'Found 0 suppliers with code {supplier_code}')
            return None

        if len(suppliers) > 1:
            logger.info(f'Found more than one supplier with supplier code "{supplier_code}", using the first one')

        return suppliers[0].Supplier_No

    def get_supplier_id_from_part_and_op_code(self, part: Part, op_code: str) -> str:
        approved_suppliers: List[ApprovedSupplierPurchasing] = ApprovedSupplierPurchasing.find_approved_suppliers(
            partId=part.id,
            operationCode=op_code
        )

        if len(approved_suppliers) == 0:
            logger.info(f'Could not find approved supplier for part {part.number} by querying on operation {op_code}')
            return None

        if len(approved_suppliers) > 1:
            logger.info(f'Multiple approved suppliers found for part {part.number} and operation {op_code}, using the first one')

        return approved_suppliers[0].supplierId

    def get_supplier_code_from_supplier_id(self, supplier_id: str) -> str:
        suppliers: List[Supplier] = Supplier.search(id=supplier_id)

        if len(suppliers) == 0:
            logger.info(f'Could not find supplier with id {supplier_id}')
            return None

        return suppliers[0].code

    def get_plex_part_key_from_part(self, part: Part):
        part_get_datasources: List[PartGetDataSource] = PartGetDataSource.get(part.number, part.revision)
        if len(part_get_datasources) == 0:
            raise CancelledIntegrationActionException(f'Could not find part with number "{part.number}" and revision "{part.revision}"'
                                                      f' using data source Parts_Get (Part)')

        return part_get_datasources[0].Part_Key

    def get_first_op_code_for_part(self, part: Part) -> str:
        # 1) get the first part operation
        part_ops: List[PartOperation] = PartOperation.find_part_operations(part_id=part.id)
        if len(part_ops) == 0:
            logger.info(f'No operations found for part {part.number}')
            return None

        # 2) get the op id of the first op
        op_id: str = part_ops[0].operationId

        # 3) get the op code
        operations: List[Operation] = Operation.find_operations(id=op_id)
        if len(operations) == 0:
            logger.info(f'No operations found with id {op_id}')
            return None

        return operations[0].code

    # Contact/Customer/Address functions
    def get_plex_customer_by_code(self, code: str) -> Customer:
        """
        raises Cancellation Integration Action if the Plex Customer Does not exist
        """
        existing_customers = Customer.find_customers(code=code)
        existing_customer: Customer = existing_customers[0] if len(existing_customers) > 0 else None
        if existing_customer is None:
            raise CancelledIntegrationActionException(f'Invalid Plex customer Code provided to importer: {code}')
        return existing_customer

    def get_existing_pp_account(self, code: str):
        accounts = Account.filter(code)
        if len(accounts) == 0:
            return None

        pp_account = Account.get(id=accounts[0].id)
        return pp_account

    def get_and_validate_contacts(self, erp_code) -> List[CustomerContact]:
        plex_customer_id = self._get_plex_customer_id(erp_code)
        plex_contacts = CustomerContact.find_customer_contacts(plex_customer_id)

        plex_contact: CustomerContact
        for plex_contact in plex_contacts:
            self._validate_contact_has_required_info(plex_contact, erp_code)

        return plex_contacts

    def get_contact_emails_for_account(self, pp_account: Account):
        emails = []
        pp_contacts = Contact.filter(account_id=pp_account.id)
        pp_contact: Contact
        for pp_contact in pp_contacts:
            emails.append(pp_contact.email)

        return emails

    def get_plex_addresses(self, plex_customer: Customer) -> tuple:
        """
        returns lists of billing, and ship to addresses, and one sold to address (the last one we get),
        """
        billing: List[CustomerAddress] = []
        facilities: List[CustomerAddress] = []
        sold_to: CustomerAddress = None

        plex_locations: [CustomerAddress] = CustomerAddress.find_customer_addresses(
            code=None,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': plex_customer.id
            }
        )

        plex_location: CustomerAddress
        for plex_location in plex_locations:
            if plex_location.billTo:
                billing.append(plex_location)
            if plex_location.soldTo:
                sold_to = plex_location
            if plex_location.shipTo:
                facilities.append(plex_location)

        return (billing, facilities, sold_to)

    def _validate_contact_has_required_info(self, plex_contact: CustomerContact, erp_code: str) -> None:
        """
        validates email, first name, last name
        """
        if plex_contact.email is None or plex_contact.email.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid email address. Please fix in order to import this account fully')
        if plex_contact.firstName is None or plex_contact.firstName.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid first name. Please fix in order to import this account fully')
        if plex_contact.lastName is None or plex_contact.lastName.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid last name. Please fix in order to import this account fully')

    def _get_plex_customer_id(self, erp_code) -> str:
        plex_customers = Customer.find_customers(code=erp_code)
        if len(plex_customers) == 0:
            raise CancelledIntegrationActionException(f'Invalid Plex customer Code provided to importer: {erp_code}')

        return plex_customers[0].id

    def create_address(self, plex_customer_id: str, pp_account: str, use_address_prefix: bool, use_addr_code_for_facility_name: bool):
        plex_locations: [CustomerAddress] = CustomerAddress.find_customer_addresses(
            code=None,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': plex_customer_id
            }
        )
        pp_facilities = Facility.list(account_id=pp_account.id)
        pp_billings = BillingAddress.list(account_id=pp_account.id)
        plex_location: CustomerAddress
        for plex_location in plex_locations:
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(plex_location.country.strip(),
                                                                                      plex_location.state.strip(),
                                                                                      plex_location.zip[0:5].strip(),
                                                                                      self.default_country)

            if plex_location.billTo:
                self.add_billing(plex_customer_id, pp_account.id, plex_location, pp_billings, state_province_name,
                                 country_alpha_3, use_address_prefix)

            if plex_location.shipTo:
                self.add_facility(plex_customer_id, pp_account.id, plex_location, pp_facilities, state_province_name,
                                  country_alpha_3, use_addr_code_for_facility_name)

    def add_facility(self, plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                     pp_facilities: [Facility], state_province_name: str, country_alpha_3: str, use_address_code_for_facility_name: bool):
        create = False
        pp_address = None
        name = plex_location.name
        if use_address_code_for_facility_name:
            name = plex_location.code
        for pp_facility in pp_facilities:
            if pp_facility.name == name:
                pp_address = Facility.get(id=pp_facility.id)
                break
        if pp_address is None:
            create = True
            pp_address = Facility(account_id=pp_account_id, name=name, attention=" ")
        pp_address.address = Address(address1=plex_location.address.strip(), city=plex_location.city.strip(),
                                     state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                     country=country_alpha_3)
        try:
            if create:
                pp_address.create(account_id=pp_account_id)
            else:
                pp_address.update()
        except PaperlessException:
            f_msg = f' {plex_customer_id}, Invalid Facility Address, street:{pp_address.address.address1}  ' \
                    f'city:{pp_address.address.city} state:{state_province_name} ' \
                    f'zip:{pp_address.address.postal_code}  country:{pp_address.address.country}'
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Facility address: {plex_customer_id}-{plex_location.name}')
            raise CancelledIntegrationActionException(f_msg)

    def add_billing(self, plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                    pp_billings: [BillingAddress], state_province_name: str, country_alpha_3: str, use_address_prefix: bool):
        for pp_billing in pp_billings:
            if pp_billing.address1 == plex_location.address.strip() and \
                    pp_billing.city == plex_location.city.strip() and \
                    pp_billing.country == country_alpha_3 and pp_billing.state == state_province_name and \
                    pp_billing.postal_code == plex_location.zip[0:5].strip():
                return
        address = plex_location.address.strip()
        if use_address_prefix:
            address = plex_location.code + '-' + address
        pp_address = BillingAddress(address1=address, city=plex_location.city.strip(),
                                    state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                    country=country_alpha_3)
        try:
            pp_address.create(account_id=pp_account_id)
        except PaperlessException:
            b_msg = f' {plex_customer_id}, Invalid Billing Address, street:{pp_address.address1} ' \
                    f'city:{pp_address.city} state:{pp_address.state} zip:{pp_address.postal_code} ' \
                    f'country:{pp_address.country}'
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Billing address: {plex_customer_id}-Billing-{plex_location.name}')
            raise CancelledIntegrationActionException(b_msg)
