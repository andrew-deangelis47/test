# import standard libraries
import os
from epicor.importer.repeat_work_importer import EpicorRepeatWorkImporter

# append to path
import sys
import requests_mock
import json
import re
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration


def load_file(file_name: str, wrap_value=True) -> json:
    with open(os.path.join(os.path.dirname(__file__), f"data/{file_name}"), 'r') as f:
        if wrap_value:
            return json.dumps({'value': [json.load(f)]})
        else:
            return json.dumps(json.load(f))


@pytest.fixture
def setup_repeat_work_importer() -> EpicorRepeatWorkImporter:
    integration = Integration()
    from epicor.importer.repeat_work_importer import EpicorRepeatWorkImporter
    i = EpicorRepeatWorkImporter(integration)
    return i


def register_mocks(mocker):
    part_matcher = re.compile("Erp.BO.PartSvc/Parts")
    quote_header_matcher = re.compile("ERP.BO.QuoteSvc/Quotes")
    quote_detail_matcher = re.compile("Erp.BO.QuoteSvc/QuoteDtls")
    quote_detail_search_matcher = re.compile("Erp.BO.QuoteDtlSearchSvc/QuoteDtlSearches")
    quote_assemblies_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteAsms")
    quote_quantities_matcher = re.compile("Erp.BO.QuoteSvc/QuoteQties")
    quote_operation_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteOprs")
    quote_material_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteMtls")
    job_entry_matcher = re.compile("ERP.BO.JobEntrySvc/JobEntries")
    ewb_rev_matcher = re.compile("ERP.BO.EngWorkBenchSvc/ECORevs")

    # register mockers
    mocker.get(part_matcher, text=load_file("get_part_response_2.json"), status_code=200)
    mocker.get(quote_header_matcher, text=load_file("get_quote_response.json"), status_code=200)
    mocker.get(quote_detail_matcher, text=load_file("get_quote_line_response.json"), status_code=200)
    mocker.get(quote_detail_search_matcher, text=load_file("get_quote_detail_search_response.json"), status_code=200)
    mocker.get(quote_assemblies_matcher, text=load_file("get_quote_assembly2.json"), status_code=200)
    mocker.get(quote_quantities_matcher, text=load_file("get_quote_qtys.json"), status_code=200)
    mocker.get(quote_operation_matcher, text=load_file("get_quote_operation.json"), status_code=200)
    mocker.get(quote_material_matcher, text=load_file("quote_material.json"), status_code=200)
    mocker.get(job_entry_matcher, text=load_file("get_job_entry_response.json"), status_code=200)
    mocker.get(ewb_rev_matcher, text=load_file("get_ewb_rev_response.json"), status_code=200)


empty_data = json.dumps({'value': []})


def url_is_in_request_history(url, method, mocker):
    for req in mocker.request_history:
        if url in str(req.url) and method == str(req.method):
            return True
    else:
        return False


class TestRepeatWorkImporter:

    def test_repeat_part_processor(self, setup_repeat_work_importer, caplog):
        integration = Integration()
        repeat_part_importer = EpicorRepeatWorkImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            repeat_part_importer.run("ABC-123:_:A")
            assert "Processing repeat work part from Epicor with part number ABC-123 and revision number A" in caplog.text
            assert url_is_in_request_history("ERP.BO.JobEntrySvc/JobEntries", "GET", m)
            assert url_is_in_request_history("Erp.BO.QuoteDtlSearchSvc/QuoteDtlSearches", "GET", m)
            assert url_is_in_request_history("ERP.BO.EngWorkBenchSvc/ECORevs", "GET", m)

    def test_processors(self, caplog):
        integration = Integration()
        repeat_part_importer = EpicorRepeatWorkImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            repeat_part_importer.run("ABC-123:_:A")
            assert "MethodOfManufactureProcessor - Attempting to create MethodOfManufacture" in caplog.text
            assert "OperationProcessor - Attempting to create Operations" in caplog.text
            assert "RequiredMaterialProcessor - Attempting to create RequiredMaterials" in caplog.text
            assert "Creating headers for repeat work part from Epicor with part number ABC-123" in caplog.text
            assert "ChildProcessor - Attempting to create Children" in caplog.text
