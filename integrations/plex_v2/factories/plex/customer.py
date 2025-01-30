from paperless.objects.customers import Account
from plex_v2.objects.customer import Customer
from plex_v2.factories.base import BaseFactory


class PlexCustomerFactory(BaseFactory):

    def to_plex_customer(self, account: Account) -> Customer:
        return Customer(
            name=self._get_name(account),
            code=self._get_code(account),
            status=self._get_status(),
            type=self._get_type(),
            note=self._get_note(account)
        )

    def _get_name(self, account: Account) -> str:
        return account.name

    def _get_code(self, account: Account) -> str:
        if account.erp_code is not None:
            return account.erp_code

        return account.name

    def _get_status(self) -> str:
        return self.config.default_customer_status

    def _get_type(self):
        return self.config.default_customer_type

    def _get_note(self, account: Account) -> str:
        if account.notes is not None:
            return account.notes

        return ''
