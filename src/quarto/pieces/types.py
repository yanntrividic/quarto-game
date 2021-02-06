'''
Created on Feb 6, 2021

@author: yann
'''

from enum import Enum


class Color(Enum):
    BEIGE = "beige"
    BROWN = "brown"


class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"


class Size(Enum):
    TALL = "tall"
    LITTLE = "little"


class Hole(Enum):
    WITH = "w hole"
    WITHOUT = "w/o hole"
