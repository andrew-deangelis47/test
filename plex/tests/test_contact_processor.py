import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration

import requests_mock


@pytest.fixture
def setup_export():
    integration = Integration()
    from plex.exporter.exporter import PlexOrderExporter
    i = PlexOrderExporter(integration)
    return i


class TestCustomerProcessor:
    def test_contact_export(self, setup_export):
        from plex.exporter.processors.customer import CustomerContactProcessor
        from plex.objects.customer import CustomerContacts, Customer
        from paperless.objects.orders import OrderContact
        customer = Customer(
            id="00000000-0000-0000-0000-000000000000",
            code="string",
            name="string",
            status="string",
            type="string",
        )
        contact = OrderContact(
            id=213453,
            account=None,
            first_name='test',
            last_name='test',
            email='test@test.com',
            notes='test',
            phone='2135466534',
            phone_ext='7896'
        )
        with requests_mock.Mocker(real_http=True) as mock:
            json_list = '[]'
            mock.get("https://test.connect.plex.com/mdm/v1/contacts",
                     text=json_list,
                     status_code=200)
            json = '{"id":"00000000-0000-0000-0000-000000000000","customerId":"00000000-0000-0000-0000-000000000000","firstName":"string","lastName":"string","supplierId":"00000000-0000-0000-0000-000000000000","phone":"string","fax":"string","mobilePhone":"string","title":"string","note":"string","email":"string","companyName":"string","officeAddress":"string","homeAddress":"string","private":0,"description":"string","birthDate":"2023-09-22T23:23:49Z","url":"string","sortOrder":0,"type":"string","associatedWithId":"00000000-0000-0000-0000-000000000000","modifiedById":"00000000-0000-0000-0000-000000000000","modifiedDate":"2023-09-22T23:23:49Z","createdById":"00000000-0000-0000-0000-000000000000","createdDate":"2023-09-22T23:23:49Z",}'
            mock.post("https://test.connect.plex.com/mdm/v1/contacts",
                      text=json,
                      status_code=200)
            setup_export.register_processor(CustomerContacts, CustomerContactProcessor)
            setup_export.process_resource(
                CustomerContacts,
                customer,
                contact,
                create=True,
            )
