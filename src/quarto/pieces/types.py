'''
Created on Feb 6, 2021

@author: yann
'''

from enum import Enum
import quarto.constants


class Color(Enum):
    BEIGE = quarto.constants.BEIGE
    BROWN = quarto.constants.BROWN


class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"


class Size(Enum):
    TALL = "tall"
    LITTLE = "little"


class Hole(Enum):
    WITH = "w/ hole"
    WITHOUT = "w/o hole"
