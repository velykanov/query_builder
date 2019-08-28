"""Monetary field module"""
from . import Field


class Monetary(Field):
    _type = 'monetary'
    _min = -92233720368547758.08
    _min = 92233720368547758.07
    _max_scale = 2

    def __add__(self, other):
        return self._general_operation(other, '+')

    def __sub__(self, other):
        return self._general_operation(other, '-')

    def __truediv__(self, other):
        return self._general_operation(other, '/', True)

    def __mul__(self, other):
        return self._general_operation(other, '*', True)
