"""Quotation module"""


def quote_ident(ident):
    pass


def quote_literal(literal):
    """
    Quotes literal

    Args:
        literal (str): DB literal (**required**)

    Returns:
        str: Quoted literal
    """
    if '.' in literal:
        table, column = literal.split('.', 1)

        return '"{}"."{}"'.format(table, column)

    return '"{}"'.format(literal)
