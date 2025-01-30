import json
import os
from typing import List
from unittest.mock import Mock
from pydantic.error_wrappers import ValidationError

from epicor.part import PurchasedComponentPart
from epicor.api_models.epicor_part_models import EpicorPartsModel
import pytest


@pytest.fixture
def valid_paperless_model_data():
    return dict(
        oem_part_number="OEM-12",
        internal_part_number="OEM-12",
        piece_price="123.4500",
        description="12 foot sheet metal.",
    )


@pytest.fixture
def valid_epicor_model_data():
    return dict(
        Company="EX",
        UnitPrice=123.45,
        PartNum="OEM-12",
        PartDescription="12 foot sheet metal.",
        ClassID="P",
        TypeCode="M",
        NonStock=True,
        ProdCode="C",
        IUM="P",
        OUM="P",
        PUM="P",
        InternalUnitPrice=12.3
    )


class TestEpicorPurchasedComponentModel:
    def test_success_incorrect_unit_price_type_string_but_correct_value(self, valid_epicor_model_data):
        valid_epicor_model_data["UnitPrice"] = "123.45"
        EpicorPartsModel(**valid_epicor_model_data)

    def test_failure_incorrect_unit_price_type(self, valid_epicor_model_data):
        with pytest.raises(ValidationError):
            valid_epicor_model_data["UnitPrice"] = "String"
            EpicorPartsModel(**valid_epicor_model_data)

    def test_success_part_description_truncates_100_max_chars(self, valid_epicor_model_data):
        valid_epicor_model_data["PartDescription"] = """I'm too long of a description.
                                                    I'm too long of a description.
                                                    I'm too long of a description.
                                                    I'm too long of a description.
                                                    I'm too long of a description.
                                                """
        part = EpicorPartsModel(**valid_epicor_model_data)
        assert len(part.part_description) <= 100

    def test_success_unit_price_4_decimal_places_from_too_large_float(self, valid_epicor_model_data):
        valid_epicor_model_data["UnitPrice"] = 123.456123
        part = EpicorPartsModel(**valid_epicor_model_data)
        just_decimal_values = part.unit_price.split(".")[1]
        assert len(just_decimal_values) == 4, f"Original Value: '{just_decimal_values}'"

    def test_success_unit_price_4_decimal_places_from_too_small_float(self, valid_epicor_model_data):
        valid_epicor_model_data["UnitPrice"] = 123.45
        part = EpicorPartsModel(**valid_epicor_model_data)
        just_decimal_values = part.unit_price.split(".")[1]
        assert len(just_decimal_values) == 4, f"Original Value: '{just_decimal_values}'"


class TestEpicorPurchasedComponentHelper:
    with open(os.path.join(os.path.dirname(__file__), "data/epicor_exact_3_parts_list.json"), 'r') as f:
        parts_full_response: json = json.load(f)

    def test_successful_purchased_component_filter_from_single_type_and_item(self):
        expected = "(ClassID eq 'MFG')"
        criteria = dict(ClassID=["MFG"])
        actual: str = PurchasedComponentPart.construct_query_filter(criteria)
        assert expected == actual

    def test_successful_purchased_component_filter_from_single_type_and_multiple_items(self):
        expected = "(ClassID eq 'MFG' or ClassID eq 'HDW')"
        criteria = dict(ClassID=["MFG", "HDW"])
        actual: str = PurchasedComponentPart.construct_query_filter(criteria)
        assert expected == actual

    def test_successful_purchased_component_filter_from_multiple_types(self):
        expected = "(ClassID eq 'MFG' or ClassID eq 'HDW') and (TypeCode eq 'P')"
        criteria = dict(ClassID=["MFG", "HDW"], TypeCode=["P"])
        actual: str = PurchasedComponentPart.construct_query_filter(criteria)
        assert expected == actual

    def test_all_purchased_component_ids_returns_ids(self):
        epicor_client = Mock()
        epicor_client.get_resource.return_value = self.parts_full_response
        expected = [" 10411603", " 3048-C-440-SS", "# 1/4 FLAT WASHER"]
        actual: List[str] = PurchasedComponentPart.get_all_purchased_component_ids(client=epicor_client)
        assert expected == actual
