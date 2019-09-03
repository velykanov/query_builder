"""Expressions module"""


class Expression:
    def __init__(self, expression):
        self._expression = expression

    def __repr__(self):
        return "<Expression '{}'>".format(self)

    def __str__(self):
        return self._expression
