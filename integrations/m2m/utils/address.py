from paperless.objects.address import AddressInfo

import m2m.models as mm


class AddressHelper:
    """
    This is a utility class for handling address records in M2M.
    """
    @staticmethod
    def create_address(address_info: AddressInfo, company: mm.Slcdpmx, addr_type: str) -> mm.Syaddr:
        """
        This a utility method for create address records in the M2M database using paperless parts addresses as source
        data.

        @param address_info : This is the Paperless Parts address that is to be converted to an M2M address record.
        @type address_info : AddressInfo

        @param company : This is the M2M company record that corresponds to the Paperless Parts account tied to the
        address information object that is to be converted.
        @type company : mm.Slcdpmx

        @param addr_type : This a string value to be used for address type in M2M.
        @type addr_type : str

        @return: This method will return the M2M address record that was created from the Paperless Parts address info.
        @rtype: mm.Syaddr
        """
        if AddressHelper.validate_address_type(addr_type) is False:
            raise ValueError(f'Invalid address type({addr_type}) passed to AddressHelper create_address method')
        address = mm.Syaddr(
            fllongdist=False,
            fcaddrtype=addr_type,
            fcaliaskey=company.fcustno,
            fcalias='SLCDPM',
            fcfname=address_info.attention,
            fccompany=company.fcompany,
            fccity=address_info.city,
            fccountry=address_info.country,
            fcphone=address_info.phone,
            fcstate=address_info.state,
            fczip=address_info.postal_code,
            fmstreet=f'{address_info.address1} {address_info.address2}',
            fncrmmod=0,
            fac='Default')
        address.save_with_number()
        return address

    @staticmethod
    def validate_address_type(addr_type: str):
        """
        This method validates potential address types to be used for creating new addresses on M2M.  The acceptable
        values for M2M address types are 'B', 'O' and 'S'.

        'B' - Business Address
        'O' - Sold-to Address
        'S' - Shipping Address

        @param addr_type : This a string value to be used for address type in M2M and needs to be validated.
        @type addr_type : str

        @return: True is valid and False if not
        @rtype: bool
        """
        if addr_type in ['S', 'O', 'B']:
            return True
        return False
