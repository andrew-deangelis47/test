from paperless.objects.common import Money


class BaseObject:

    TOTAL_ELEMENTS = 0
    SEQUENCE = []
    FIELD_DELIMITER = ';'

    def to_i_file(self):
        data_list = [''] * self.TOTAL_ELEMENTS
        for field, position in self.SEQUENCE:
            value = getattr(self, field)
            if value is not None:

                if isinstance(value, Money):
                    data_list[position] = value.raw_amount
                else:
                    data_list[position] = value

        i_file = ''
        for i in range(self.TOTAL_ELEMENTS):
            i_file += f'{data_list[i]};'
        i_file += '|'

        return i_file
