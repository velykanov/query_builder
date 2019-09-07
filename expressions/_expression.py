"""Expressions module"""


# TODO: probably implement | and & operations
class Expression:
    """
    Expression class helps write raw SQL queries

    Args:
        expression (str): Raw SQL query
    """
    def __init__(self, expression):
        self._expression = expression

    def __repr__(self):
        return "<Expression '{}'>".format(self)

    def __str__(self):
        return self._expression
