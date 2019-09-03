"""Binary field module"""
from ._field import Field


class Bytea(Field):
    _type = 'bytea'
