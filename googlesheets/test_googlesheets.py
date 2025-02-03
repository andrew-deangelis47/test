import os
import sys
import pytest
import requests_mock

# append to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))

from baseintegration.integration import Integration


@pytest.fixture
def setup_material_importer():
    integration = Integration()
    from googlesheets.importer.importer import GoogleSheetsMaterialImporter
    i = GoogleSheetsMaterialImporter(integration)
    return i


class TestGoogleSheetsImport:

    def test_google_sheets_listener(self, setup_material_importer, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            int_id = setup_material_importer._integration.managed_integration_uuid
            m.post(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions",
                text='{"action_type": '
                     '"test",'
                     '"action_uuid": '
                     '"abc-123",'
                     '"updated": "2021-11-30T17:09:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            m.get(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"action_type": '
                     '"test",'
                     '"action_uuid": '
                     '"abc-123",'
                     '"updated": "2021-11-30T17:09:39.052737Z",'
                     '"created": "2021-11-30T17:08:41.811913Z",'
                     '"status": "queued",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            m.patch(
                f"https://release.paperlessparts.com/api/managed_integrations/public/{int_id}/integration_actions/abc-123",
                text='{"action_type": '
                     '"test",'
                     '"action_uuid": '
                     '"abc-123",'
                     '"status": "in_progress",'
                     '"status_message": '
                     'null,"entity_id": '
                     '"1"}',
                status_code=200)
            setup_material_importer.run()
            assert "Processed testing123 successfully" in caplog.text
            assert "No item number, quitting early" in caplog.text
            assert "Not bringing over testing123 because family is not populated"
