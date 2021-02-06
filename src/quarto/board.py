'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg

from .constants import LGREEN, DGREEN, SQUARE_SIZE, COLS, ROWS


class Board:

    def __init__(self):
        self.board = [[]]  # 4 by 4 grid
        self.selected_piece = None  # if we have selected a piece or not
        self.pieces_count = 0  # number of pieces on the board

    def draw_cells(self, win):
        colors = itertools.cycle((LGREEN, DGREEN))
        for x in range(COLS):
            for y in range(ROWS):
                rect = (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(colors), rect)
            next(colors)
