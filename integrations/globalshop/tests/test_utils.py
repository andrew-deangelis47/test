from globalshop.utils import pad_part_num


class TestUtils:

    def test_part_pad(self):
        # 13 characters
        un_padded = '1234567890123'
        padded = pad_part_num(un_padded)

        # 17 characters
        assert padded == un_padded + "    "
