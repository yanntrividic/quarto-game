'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg
from ..constants import SQUARE_SIZE, SXOFFSET, SYOFFSET, GXOFFSET, GYOFFSET, DBROWN
from .types import Shape, Size, Hole, Coloration


class Piece:
    '''
    This class represent a piece in game.

    Attributes
    ----------
    row : int
        The row where the piece is located
    col : int
        The column where the piece is located
    coloration : Coloration(Enum)
        The color of the piece BEIGE or BROWN
    shape : Shape(Enum)
        The shape of the piece SQUARE or CIRCLE
    size : Size(Enum)
        The size of the piece TALL or LITTLE
    hole : Hole(Enum)
        If there is a hole or not in the piece With or WITHOUT
    '''

    PADDING = 15  # space between the border of a cell and the piece
    OUTLINE = 2  # outline of the piece
    INNER_PADDING = 3  # space between the hole of the piece (if there is one) and the border of the piece

    def __init__(self, row, col, coloration, shape, size, hole):
        '''
        Piece's constructor :
            -the row and col helps to locate the piece
            -each of the 2^4 pieces is unique this is the reason why it recquires the coloration, shape, size and hole attributes
        '''

        self.row = row
        self.col = col

        self.size = size
        self.coloration = coloration
        self.shape = shape
        self.hole = hole

        self.x = 0
        self.y = 0
        self.calc_pos(True)  # initializes the (x,y) position of the piece on the board

    def calc_pos(self, init=False):
        '''
        calc_pos calculates the x y position where we need to draw the piece

        Parameters
        ----------
        init : Boolean
            if the game is being initialized, init == true, otherwise it's false
        '''

        if(init):  # when we first initialize the game
            self.x = SQUARE_SIZE * self.col + SXOFFSET + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.row + SYOFFSET + SQUARE_SIZE // 2
        else:  # when a piece is being put on the board
            self.x = SQUARE_SIZE * self.col + GXOFFSET + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.row + GYOFFSET + SQUARE_SIZE // 2

    def move_to_gameboard(self, row, col):
        '''
        Change the row and col of the piece

        Parameters
        ----------
        row : int
            the row of the piece
        col : int
            the column of the piece
        '''
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):
        '''
        displays a piece on the board. Each piece is unique as we have 2^4 caracteristics to represent

        Parameters
        ----------
        win : Pygame window for display
            The window where the game is displayed
        '''
        radius = SQUARE_SIZE // 2 - self.PADDING
        if(self.size == Size.LITTLE):
            radius -= radius // 3  # if this piece is tall, then its original size is decreased by 33%
        if(self.shape == Shape.CIRCLE):  # for the shapes
            pg.draw.circle(win, DBROWN, (self.x, self.y), radius + self.OUTLINE)  # the outline
            pg.draw.circle(win, self.coloration.value, (self.x, self.y), radius)  # includes the coloration
            if(self.hole == Hole.WITH):  # for the hole
                pg.draw.circle(win, DBROWN, (self.x, self.y), int(radius * 0.8))  # TODO: tweak the colors
        else:  # if it's not a circle
            rect = (self.x - radius, self.y - radius, radius * 2, radius * 2)
            rect_outline = (self.x - (radius + self.OUTLINE), self.y - (radius + self.OUTLINE),
                            (radius + self.OUTLINE) * 2, (radius + self.OUTLINE) * 2)
            pg.draw.rect(win, DBROWN, rect_outline)  # the outline
            pg.draw.rect(win, self.coloration.value, rect)
            if(self.hole == Hole.WITH):
                rect_hole = (self.x - int(radius) // 1.5, self.y - int(radius) // 1.5, int(radius * 4 / 3), int(radius * 4 / 3))
                pg.draw.rect(win, DBROWN, rect_hole)

    def __repr__(self, verbose=False):
        '''
        Represent the object in a string format of 4 caracters
        each caracter represent a caracteristic

        Parameters
        ----------
        verbose : Boolean
        '''

        if(verbose):
            return(str(self.size) + ", " + str(self.coloration) + ", " + str(self.shape) +
                   ", " + str(self.hole))
        else:
            return(str("X" if(self.size == Size.TALL) else "O") +
                   str("X" if(self.coloration == Coloration.BEIGE) else "O") +
                   str("X" if(self.shape == Shape.SQUARE) else "O") +
                   str("X" if(self.hole == Hole.WITHOUT) else "O"))
