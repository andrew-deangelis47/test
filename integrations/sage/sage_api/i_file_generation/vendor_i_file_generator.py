from sage.models.sage_models import Supplier


def _get_i_file_string_from_array(i_file_array: list):
    i_file_str = ''
    for val in i_file_array:
        i_file_str += val + ';'
    i_file_str += '|'
    return i_file_str


class VendorIFileGenerator:

    TOTAL_I_FILE_FIELDS = 48

    def generate(self, sage_vendor: Supplier):
        i_file_array = self._get_non_populated_i_file_array()
        for object_property in sage_vendor.SEQUENCE:
            field, position = object_property
            field_value = getattr(sage_vendor, field)
            i_file_array[position] = field_value
        return _get_i_file_string_from_array(i_file_array)

    def _get_non_populated_i_file_array(self):
        i_file_array = []
        for i in range(self.TOTAL_I_FILE_FIELDS):
            i_file_array.append('')
        return i_file_array
