"""Quotation module"""


def quote_ident(ident):
    """
    Quotes identity

    Args:
        ident (str): Identity (**required**)

    Returns:
        str: Quoted identity
    """
    ident = str(ident).replace("'", "''").replace("\\", "\\\\")

    return "'{}'".format(ident)


def quote_literal(literal):
    """
    Quotes literal

    Args:
        literal (str): DB literal (**required**)

    Returns:
        str: Quoted literal
    """
    if literal is None:
        return None

    if '.' in literal:
        table, column = literal.split('.', 1)

        return '"{}"."{}"'.format(table, column)

    return '"{}"'.format(literal)
