import random
from types import SimpleNamespace
import pytest

from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent

from baseintegration.integration import Integration

from dynamics.objects.item import PurchasedComponent
from dynamics.tests.utils import with_mocks, get_object_mocks


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.importer.importer import DynamicsPurchasedComponentImporter
    return DynamicsPurchasedComponentImporter(integration)


item_num = str(random.randint(1, 10000))

mock_dict = {
    PurchasedComponent: SimpleNamespace(
        No=item_num,
        Description='test',
        Unit_Cost=4
    )
}


basic_mocks = get_object_mocks(mock_dict)


class TestDynamicsPurchasedComponentImport:
    @staticmethod
    def get_purchased_component(num) -> PaperlessPurchasedComponent:
        purchased_components = PaperlessPurchasedComponent.search(num)
        filtered_purchased_components = [c for c in purchased_components if c.oem_part_number == num]
        return filtered_purchased_components[0]

    def test_import_purchased_component(self, setup_integration):

        def run_test(call_data, get_args):
            setup_integration.run(purchased_component_id=item_num)

            purchased_component = self.get_purchased_component(item_num)

            assert purchased_component.oem_part_number == mock_dict[PurchasedComponent].No
            assert purchased_component.internal_part_number == mock_dict[PurchasedComponent].No
            assert purchased_component.description == mock_dict[PurchasedComponent].Description
            assert float(purchased_component.piece_price) == mock_dict[PurchasedComponent].Unit_Cost

            mock_dict[PurchasedComponent].Unit_Cost = 7.5

            setup_integration.run(purchased_component_id=item_num)

            purchased_component = self.get_purchased_component(item_num)

            assert float(purchased_component.piece_price) == mock_dict[PurchasedComponent].Unit_Cost

            purchased_component.delete()

        with_mocks(run_test, basic_mocks)

    def test_bulk_import_purchased_component(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration.run(purchased_component_id=item_num)

            purchased_component = self.get_purchased_component(item_num)

            assert purchased_component.oem_part_number == mock_dict[PurchasedComponent].No
            assert purchased_component.internal_part_number == mock_dict[PurchasedComponent].No
            assert purchased_component.description == mock_dict[PurchasedComponent].Description
            assert float(purchased_component.piece_price) == mock_dict[PurchasedComponent].Unit_Cost

            mock_dict[PurchasedComponent].Unit_Cost = 7.5

            setup_integration._bulk_process_purchased_component([item_num])

            purchased_component = self.get_purchased_component(item_num)

            assert float(purchased_component.piece_price) == mock_dict[PurchasedComponent].Unit_Cost

            purchased_component.delete()

        with_mocks(run_test, basic_mocks)
