def pad_part_num(part_num: str) -> str:
    """
    This utility right pads the provided string so that it is at least 17
    characters.

    Global Shop requires a 17 character string value for a part number, as the
    full part number is part_num + rev to make up to 20 character string. The
    rev is max of 3 chars, and if the part isn't right padded to 17 chars then
    the rev will appear in the part instead of the rev.
    """
    if part_num:
        while len(part_num) < 17:
            part_num += ' '

    return part_num
