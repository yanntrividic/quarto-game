'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg
from quarto.pieces.piece import Piece
from quarto.pieces.types import *

from .constants import (GREEN, DGREEN, LGREEN, SQUARE_SIZE,
                        GCOLS, GROWS, SCOLS, SROWS,
                        GXOFFSET, GYOFFSET, SXOFFSET, SYOFFSET)


class Board:

    def __init__(self):
        self.board = [[]]  # 4 by 4 grid
        self.selected_piece = None  # if we have selected a piece or not
        self.pieces_count = 0  # number of pieces on the board
        self.init_storage_pieces()

    def draw_cells(self, win):
        pass


class GameBoard(Board):

    def draw_cells(self, win):
        colors = itertools.cycle((LGREEN, GREEN))
        for x in range(GCOLS):
            for y in range(GROWS):
                rect = (x * SQUARE_SIZE + GXOFFSET, y * SQUARE_SIZE + GYOFFSET, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(colors), rect)
            next(colors)

    def init_storage_pieces(self):
        pass


class StorageBoard(Board):

    def draw_cells(self, win):
        colors = itertools.cycle((DGREEN, GREEN))
        for x in range(SCOLS):
            for y in range(SROWS):
                rect = (x * SQUARE_SIZE + SXOFFSET, y * SQUARE_SIZE + SYOFFSET, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(colors), rect)
            next(colors)

    def init_storage_pieces(self):
        row = 0
        for c in Color:
            col = 0
            self.board.append([])
            for h in Hole:
                for sh in Shape:
                    for si in Size:
                        self.board[row].append(Piece(row, col, c, sh, si, h))
                        col += 1
            row += 1

    def draw(self, win):
        self.draw_cells(win)
        for row in range(SROWS):
            for col in range(SCOLS):
                piece = self.board[row][col]
                piece.draw(win)
