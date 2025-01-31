import decimal

from ...baseintegration.utils.data import sqlize_value, sqlize_str, safe_trim, sqlize_bool


class TestDataUtils:
    def test_sqlize_val(self):
        """
        Ensure that mutliple data types are correctly "sqlized" for use in a
        query
        """

        int_val = 123
        float_val = 456.32221
        decimal_val = decimal.Decimal('44.5567')
        none_val = None

        int_str = sqlize_value(int_val)
        assert int_str
        assert int_str == f"{str(int_val)}"

        float_str = sqlize_value(float_val)
        assert float_str
        assert float_str == f"{str(float_val)}"

        decimal_str = sqlize_value(decimal_val)
        assert decimal_str
        assert decimal_str == f"{str(decimal_val)}"

        null_str = sqlize_value(none_val)
        assert null_str
        assert null_str == "null"

    def test_sqlize_str(self):
        """
        Ensure the string is properly encapsulated in quotes else is null
        """

        test_str = 'wafflecopter'
        str_result = sqlize_str(test_str)
        assert str_result
        assert str_result == f"'{test_str}'"

        null_result = sqlize_str(None)
        assert null_result
        assert null_result == 'null'

    def test_safe_trim(self):
        """
        Test stripping whitespace off a string, or None
        """

        empty_str = ''
        none_str = None
        prefix_str = '    words and words'
        suffix_str = 'words and words  '
        padded_str = '   words and words   '
        easy_str = 'words and words'

        res = safe_trim(empty_str)
        assert res == empty_str

        res = safe_trim(none_str)
        assert res is None

        res = safe_trim(prefix_str)
        assert res == easy_str

        res = safe_trim(suffix_str)
        assert res == easy_str

        res = safe_trim(padded_str)
        assert res == easy_str

        res = safe_trim(easy_str)
        assert res == easy_str

    def test_sqlize_bool(self):
        result = sqlize_bool(None)
        assert result == 'null'
        result = sqlize_bool(True)
        assert result == '1'
        result = sqlize_bool(False)
        assert result == '0'
