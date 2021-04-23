'''
Created on Feb 6, 2021

@author: yann
'''

from enum import Enum
import quarto.constants


class Coloration(Enum):
    """
    Enumeration for the 2 play colors, brown and beige
    """
    BEIGE = quarto.constants.BEIGE
    BROWN = quarto.constants.BROWN


class Shape(Enum):
    """
    Enumeration for the shape of the symbol, circle and square
    """
    CIRCLE = "circle"
    SQUARE = "square"


class Size(Enum):
    """
    Enumaration for the size of the symbol, tall orsmall
    """
    TALL = "tall"
    LITTLE = "little"


class Hole(Enum):
    """
    Enumeration for the existance of a hole in the symbol, with and without a hole
    """
    WITH = "w/ hole"
    WITHOUT = "w/o hole"
