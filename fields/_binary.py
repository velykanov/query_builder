"""Binary field module"""
from . import Field


class Bytea(Field):
    _type = 'bytea'
