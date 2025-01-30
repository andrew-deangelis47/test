from plex_v2.objects.raw_material_attribute import RawMaterialAttribute


class TestRawMaterialAttribute:
    def test_model(self):
        attribute = RawMaterialAttribute(
            field='test_field',
            type='str',
            value='1234'
        )

        assert attribute.field == 'test_field'
        assert attribute.type == 'str'
        assert attribute.value == '1234'
