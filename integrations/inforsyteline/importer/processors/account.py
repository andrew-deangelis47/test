from baseintegration.importer.import_processor import BaseImportProcessor
from inforsyteline.models import CustomerMst, CustaddrMst
from baseintegration.datamigration import logger
from paperless.objects.customers import Account, Address
from baseintegration.utils import set_blank_to_default_value, create_or_update_account


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, account_id: str):  # noqa: C901
        logger.info(f"Processing {account_id}")
        # need to strip whitespace due to weird left justification of IDs
        account: CustomerMst = CustomerMst.objects.extra(where=[f"LOWER(REPLACE(cust_num,' ','')) = '{account_id}'"]).first()
        addr: CustaddrMst = CustaddrMst.objects.extra(where=[f"LOWER(REPLACE(cust_num,' ','')) = '{account_id}'"]).first()
        if not account:
            logger.info("Account not processed")
            return
        pp_account, account_is_new = create_or_update_account(integration=self._importer._integration,
                                                              erp_code=account_id,
                                                              account_name=addr.name)
        logger.info(f'Found customer with account_id {account_id} in the CustomerCode table in E2')
        # Create a Paperless Parts record for this account
        name = addr.name
        erp_code = account_id

        pp_account.name = name
        pp_account.erp_code = erp_code

        should_assign_sold_to_address = True
        if should_assign_sold_to_address:
            # Assign the billing information for this account
            billing_address1 = set_blank_to_default_value(addr.addr_1, None)
            billing_address2 = set_blank_to_default_value(addr.addr_2, None)
            billing_city = set_blank_to_default_value(addr.city, None)
            # todo update this
            billing_country = "USA"
            billing_postal_code = set_blank_to_default_value(addr.zip, None)
            billing_state = set_blank_to_default_value(addr.state, None)

            # Set the sold to address to be the billing address from E2
            sold_to_address = Address(
                address1=billing_address1,
                address2=billing_address2,
                city=billing_city,
                country=billing_country,
                postal_code=billing_postal_code,
                state=billing_state
            )

            pp_account.sold_to_address = sold_to_address

        try:
            if account_is_new:
                pp_account.create()
            else:
                pp_account.update()
        except Exception as e:
            logger.warning(e)
            if "This group already has an account with this name" in e.args[0]:
                account: Account = self.get_account_by_name(name)
                if account:
                    try:
                        account = Account.get(account.id)
                        account.erp_code = account_id
                        account.update()
                        logger.info("Updated erp code!")
                    except Exception as e:
                        logger.info(e)
                        logger.info("Did not update erp code, skipping")
            logger.warning(f'Encountered an error importing account: {name} - skipping.')
        logger.info(f"Account {account_id} was updated or created!")

    def get_account_by_name(self, name):
        accounts = Account.list()
        for account in accounts:
            if account.name == name:
                return account
        else:
            return None
