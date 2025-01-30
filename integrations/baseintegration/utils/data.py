def safe_trim(string: str) -> str:
    """
    Safely trim a nullable string, and return the trimmed string or None
    """
    ret_str = None
    if string is not None:
        ret_str = string.strip()

    return ret_str if ret_str is not None else None


def sqlize_str(sql_str: str,
               remove_newlines: bool = True,
               replace_newline_char: str = None) -> str:
    """
    Used for inserting a string value into a SQL command. Return the string
    value else null
    """

    if sql_str is None:
        return 'null'
    else:
        # escape single quotes:
        sql_str = sql_str.replace("'", "''")

        # There could be an option to escape newlines. For now, GlobalShop
        # needs to have then removed by default, as it breaks some internal
        # importer data if newlines are present.
        if remove_newlines:
            sql_str = sql_str.replace("\\n", "")
            sql_str = sql_str.replace("\\r", "")
            sql_str = sql_str.replace("\n", "")
            sql_str = sql_str.replace("\r", "")
        elif replace_newline_char:
            sql_str = sql_str.replace("\\n", replace_newline_char)
            sql_str = sql_str.replace("\\r", replace_newline_char)
            sql_str = sql_str.replace("\n", replace_newline_char)
            sql_str = sql_str.replace("\r", replace_newline_char)

        return f"'{sqlize_value(sql_val=sql_str)}'"


def sqlize_value(sql_val) -> str:
    """
    Used for inserting a value into a SQL command. Return the string
    value else null
    """

    # TODO: add escape strings
    if sql_val is None:
        return 'null'
    else:
        return f"{str(sql_val)}"


def sqlize_bool(sql_val: bool) -> str:
    """
    Used for inserting a value into a SQL command. Return the bool
    value else null
    """

    # TODO: add escape strings
    if sql_val is None:
        return 'null'
    elif sql_val:
        return '1'
    else:
        return '0'
