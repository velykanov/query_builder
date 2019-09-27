"""Binary field module"""
from ._field import Field


class Bytea(Field):
    """Byte field type"""
    _type = 'bytea'
