"""Character fields module"""
from . import Field


class Varchar(Field):
    _type = 'varchar'

    def __init__(self, name, alias=None, max_length=None):
        if max_length is None:
            self.max_length = 1

        super(Varchar, self).__init__(name, alias)
