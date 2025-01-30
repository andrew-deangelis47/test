import pytest
from baseintegration.integration import Integration
from baseintegration.exporter.exceptions import ProcessNotImplementedError


@pytest.fixture
def setup_exporter():
    integration = Integration()
    from excel.exporter.exporter import ExcelQuoteExporter
    exporter = ExcelQuoteExporter(integration)
    return exporter


class TestExcelQuoteExporter:
    def test_exporter_has_config(self, setup_exporter):
        assert type(setup_exporter._integration.config) is dict

    def test_exporter_runs(self, setup_exporter):
        with pytest.raises(ProcessNotImplementedError) as e_info:
            print(f'Exception properly raised {e_info}')
            setup_exporter.run(quote_num='281')
