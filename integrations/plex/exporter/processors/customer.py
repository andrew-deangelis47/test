from plex.exporter.processors.base import PlexProcessor
from paperless.objects.orders import OrderAccount, AddressInfo, OrderContact
from plex.objects.customer import Customer, CustomerAddress, CustomerPart, CustomerContacts
from plex.objects.part import Part
from baseintegration.datamigration import logger


class CustomerAddressProcessor(PlexProcessor):
    def _process(
            self,
            customer: Customer,
            address_info: AddressInfo,
            address_functions,
            code_suffix,
            billing_address_id=None,
            create=True
    ):
        address_functions_kwargs = {func: True for func in address_functions}
        if address_info is None:
            if self._exporter.erp_config.use_plex_address_as_fallback:
                for add_type in address_functions:
                    address_functions_kwarg = {func: True for func in [add_type]}
                    customer_addresses = CustomerAddress.find_customer_addresses(**address_functions_kwarg,
                                                                                 resource_name_kwargs={
                                                                                     'customer_id': customer.id})
                    customer_address = customer_addresses[0] if len(customer_addresses) > 0 else None
                    return customer_address
            else:
                return None
        alt_code = f'{address_info.city}, {address_info.state if address_info is not None else address_info.country} - {code_suffix}'
        has_facility_name = getattr(address_info, 'facility_name',
                                    None) and address_info.facility_name is not None and address_info.facility_name != ''
        if has_facility_name:
            logger.info(f'This address has a facility name, "{address_info.facility_name}"! '
                        f'Using this to match an address')
            addresses = CustomerAddress.find_customer_addresses(
                code=address_info.facility_name,
                billTo=None,
                remitTo=None,
                shipTo=None,
                soldTo=None,
                resource_name_kwargs={
                    'customer_id': customer.id
                }
            )
            address: CustomerAddress = addresses[0] if len(addresses) > 0 else None
            if address is not None and address.code.lower() == address_info.facility_name.lower():
                if address.shipTo is False and 'shipTo' in address_functions:
                    address.shipTo = True
                    address.customerId = customer.id
                    address.update()
                if address.billTo is False and 'billTo' in address_functions:
                    address.billTo = True
                    address.customerId = customer.id
                    address.update()
                logger.info('Matching address with facility name found')
                return address
            else:
                logger.info('Matching address with facility name was not found, creating one')
                address = CustomerAddress(
                    customerId=customer.id,
                    active=True,  # Hopefully this can tell the engineers that they need to go modify the code here?
                    code=address_info.facility_name,
                    address=f'{address_info.address1} {address_info.address2}',
                    city=address_info.city,
                    state=address_info.state,
                    zip=address_info.postal_code,
                    country=address_info.country,
                    phone=address_info.phone,
                    billToAddressId=billing_address_id,
                    billTo=True,
                    remitTo=True,
                    shipTo=True,
                    soldTo=True
                )
                if create is True:
                    return address.create()
                else:
                    return address
        else:
            logger.info('No facility name found, Checking for paperless parts formatted address names')
            addresses = CustomerAddress.find_customer_addresses(
                code=alt_code,
                billTo=None,
                remitTo=None,
                shipTo=None,
                soldTo=None,
                resource_name_kwargs={
                    'customer_id': customer.id
                }
            )
            address: CustomerAddress = addresses[0] if len(addresses) > 0 else None

            if address is not None:
                code: str = address.code
                if code.lower() == alt_code.lower():
                    logger.info('Matching address with formatted address names found')
                    return address

        address = CustomerAddress(
            customerId=customer.id,
            active=True,
            code=alt_code,
            address=f'{address_info.address1} {address_info.address2}',
            city=address_info.city,
            state=address_info.state,
            zip=address_info.postal_code,
            country=address_info.country,
            phone=address_info.phone,
            billToAddressId=billing_address_id,
            **address_functions_kwargs,
        )
        matching_address = address.fuzzy_extract_matching_address(
            CustomerAddress.find_customer_addresses(**address_functions_kwargs, resource_name_kwargs={
                'customer_id': customer.id
            })
        )
        if matching_address is None and create is True:
            logger.info('Creating new address {}'.format(repr(address)))
            return address.create()
        elif matching_address is None:
            logger.info('Creating new address {}'.format(repr(address)))
            return address
        else:
            logger.info('Found fuzzy matching address for {}'.format(repr(address)))
            return matching_address


class CustomerProcessor(PlexProcessor):
    def _process(self, account: OrderAccount, billing_info: AddressInfo, shipping_info: AddressInfo,
                 create=True) -> Customer:
        code = account.erp_code
        name = account.name

        existing_customers = Customer.find_customers(
            code=code
        ) if code is not None else Customer.find_customers(
            name=name
        )

        existing_customer = existing_customers[0] if len(existing_customers) > 0 else None

        if existing_customer \
                and existing_customer.status in self._exporter.erp_config.import_customer_status_include_filter:
            logger.info('Existing customer (code: {}) found, using this one'.format(existing_customer.code))
            return existing_customer
        elif existing_customer and existing_customer.status == 'Deleted' \
                and self._exporter.erp_config.account_reactivation_enabled:
            # Undo the soft-delete
            logger.info('Existing customer (code: {}) found, but it was soft-deleted; un-deleting it'.format(
                existing_customer.code
            ))
            existing_customer.status = self._exporter.erp_config.account_reactivation_status
            existing_customer.update()
            return existing_customer
        else:
            if create is True:
                logger.info('Creating new customer with code {} and name {}'.format(account.erp_code, account.name))
                new_customer = Customer(
                    name=account.name,
                    code=account.erp_code if account.erp_code is not None else name,
                    status='Active',
                    type=self._exporter.erp_config.default_customer_type,
                    note=account.notes if account.notes else '',
                )
                return new_customer.create()
            else:
                logger.info('Customer creation disabled')
                return None


class CustomerPartProcessor(PlexProcessor):
    def _process(self, part: Part, customer: Customer, create=True):
        existing_customer_parts = CustomerPart.find_customer_parts(
            number=part.number,
            partId=part.id,
            customerId=customer.id,
        )
        # FIXME: Seems like naively picking the first of the list of results is a bad assumption, since it has caused
        #  some problems...
        existing_customer_part = existing_customer_parts[0] if len(existing_customer_parts) > 0 else None

        if existing_customer_part \
                and part.number == existing_customer_part.number \
                and part.revision == existing_customer_part.revision \
                and customer.id == existing_customer_part.customerId:
            logger.info('Using existing customer part with number {} and revision {}'.format(
                existing_customer_part.number,
                existing_customer_part.revision,
            ))
            return existing_customer_part
        else:
            logger.info('Creating new customer part with number {} and revision {}'.format(
                part.number,
                part.revision,
            ))
            return CustomerPart(
                number=part.number,
                partId=part.id,
                revision=part.revision,
                customerId=customer.id,
                description=self.create_description(part),
            ).create()

    @staticmethod
    def create_description(part: Part) -> str:
        description = part.name
        if description and part.description:
            description += f"\n {part.description}"
        elif part.description:
            description = part.description
        return description


class CustomerContactProcessor(PlexProcessor):
    def _process(
            self,
            customer: Customer,
            contact: OrderContact,
            create=True
    ):
        exists = False
        list_contacts: [CustomerContacts] = CustomerContacts.find_customer_contacts(customer_id=customer.id)
        for plex_contact in list_contacts:
            if plex_contact.email.lower().strip() == contact.email.lower().strip():
                exists = True
                break
        if create and not exists:
            new_contact = CustomerContacts(
                email=contact.email,
                customerId=customer.id,
                firstName=contact.first_name,
                lastName=contact.last_name,
                phone=contact.phone,
                note=contact.notes
            )
            new_contact.create()
