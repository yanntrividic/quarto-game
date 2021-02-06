'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg
from quarto.constants import SQUARE_SIZE, SXOFFSET, SYOFFSET, LBEIGE, BEIGE, BROWN, LBROWN, DBROWN
from .types import *


class Piece:
    PADDING = 15  # space between the border of a cell and the piece
    OUTLINE = 2  # outline of the piece
    INNER_PADDING = 3  # space between the hole of the piece (if there is one) and the border of the piece

    def __init__(self, row, col, color, shape, size, hole):
        self.row = row
        self.col = col

        self.size = size
        self.color = color
        self.shape = shape
        self.hole = hole

        self.x = 0
        self.y = 0
        self.calc_pos(True)  # initializes the position of the piece on the board

        self.activated = False  # a piece which hasn't been picked yet in not activated

    # calc_pos calculates the x y position where we need to draw the piece
    # if the game is being initialized, init == true, otherwise it's false
    def calc_pos(self, init):
        if(init):  # when we first initialize the game
            self.x = SQUARE_SIZE * self.col + SXOFFSET + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.row + SYOFFSET + SQUARE_SIZE // 2
        else:  # when a piece is being put on the board
            pass

    # when a piece has been played on the board, activated == True
    def activate(self):
        self.activated = True

    # displays a piece on the board. Each piece is unique as we have 2^4 caracteristics to represent
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        if(self.size == Size.LITTLE):
            radius -= radius // 10  # if this piece is tall, then its original size is decreased by 10%
        if(self.shape == Shape.CIRCLE):  # for the shapes
            pg.draw.circle(win, DBROWN, (self.x, self.y), radius + self.OUTLINE)  # the outline
            pg.draw.circle(win, self.color.value, (self.x, self.y), radius)  # includes the color
            if(self.hole == Hole.WITH):  # for the hole
                pg.draw.circle(win, DBROWN, (self.x, self.y), int(radius * 0.8))  # TODO: tweak the colors
        else:  # if it's not a circle
            rect = (self.x - radius, self.y - radius, radius * 2, radius * 2)
            rect_outline = (self.x - (radius + self.OUTLINE), self.y - (radius + self.OUTLINE),
                            (radius + self.OUTLINE) * 2, (radius + self.OUTLINE) * 2)
            # FIXME: always picks de black rectangle
            pg.draw.rect(win, DBROWN, rect_outline)  # the outline
            pg.draw.rect(win, self.color.value, rect)
            if(self.hole == Hole.WITH):
                rect_hole = (self.x - int(radius) // 1.5, self.y - int(radius) // 1.5, int(radius * 4 / 3), int(radius * 4 / 3))
                pg.draw.rect(win, DBROWN, rect_hole)

    # equivalent of Java's toString() method
    def __repr__(self):
        return str(self.size + ", " + self.color + ", " + self.shape + ", " + self.hole + ", " + self.activated)
