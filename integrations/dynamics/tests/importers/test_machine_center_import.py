import random
from types import SimpleNamespace
import pytest

from baseintegration.integration import Integration

from dynamics.objects.item import MachineCenter
from dynamics.tests.utils import with_mocks, get_object_mocks


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.importer.importer import DynamicsMachineCenterImporter
    return DynamicsMachineCenterImporter(integration)


machine_center_num = str(random.randint(1, 100))

mock_dict = {
    MachineCenter: SimpleNamespace(
        No=machine_center_num,
        Name='test',
        Work_Center_No='test',
        Capacity=0,
        Efficiency=0,
        Search_Name='test',
        Overhead_Rate=0
    )
}

basic_mocks = get_object_mocks(mock_dict)


class TestDynamicsMachineCenterImport:
    def test_import_machine_center(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration.table_name = 'dynamics_machine_centers'
            setup_integration.run(work_center_id=machine_center_num)
            assert setup_integration._bulk_process_work_center([machine_center_num])

        with_mocks(run_test, basic_mocks)
