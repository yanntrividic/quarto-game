'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg
from quarto.pieces.piece import Piece
from quarto.pieces.types import Coloration, Hole, Shape, Size

from .constants import (GREEN, DGREEN, LGREEN, DBROWN,
                        SQUARE_SIZE, GCOLS, GROWS, SCOLS, SROWS,
                        GXOFFSET, GYOFFSET, SXOFFSET, SYOFFSET, BOARDOUTLINE)


# TODO: I'm not sure if having two additional classes is a good idea.
#  we might have to make it only one class
class Board:

    def __init__(self):
        self.board = [[]]  # 4 by 4 grid
        self.selected_piece = None  # if we have selected a piece or not
        self.pieces_count = 0  # number of pieces on the board
        self.init_storage_pieces()

    def draw_cells(self, win):
        pass

    def __repr__(self):
        s = ""
        for x in range(len(self.board) - 1):
            for y in range(len(self.board[0])):
                s += str(self.board[x][y]) + " "
            s += '\n'
        return(s)


class GameBoard(Board):

    def draw_cells(self, win):
        rect = (GXOFFSET - BOARDOUTLINE, GYOFFSET - BOARDOUTLINE,
                SQUARE_SIZE * GCOLS + 2 * BOARDOUTLINE, SQUARE_SIZE * GROWS + 2 * BOARDOUTLINE)
        pg.draw.rect(win, DBROWN, rect)
        colors = itertools.cycle((LGREEN, GREEN))
        for x in range(GCOLS):
            for y in range(GROWS):
                rect = (x * SQUARE_SIZE + GXOFFSET, y * SQUARE_SIZE + GYOFFSET, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(colors), rect)
            next(colors)

    def init_storage_pieces(self):
        for x in range(GCOLS):
            self.board.append([])
            for y in range(GROWS):
                self.board[x].append(0)
        print(self.__repr__())

    def put_piece(self, piece, row, col):
        self.board[row][col] = piece
        piece.move(row, col)


class StorageBoard(Board):

    def draw_cells(self, win):
        rect = (SXOFFSET - 10, SYOFFSET - 10,
                SQUARE_SIZE * SCOLS + 20, SQUARE_SIZE * SROWS + 20)
        pg.draw.rect(win, DBROWN, rect)
        colors = itertools.cycle((DGREEN, GREEN))
        for x in range(SCOLS):
            for y in range(SROWS):
                rect = (x * SQUARE_SIZE + SXOFFSET, y * SQUARE_SIZE + SYOFFSET, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(colors), rect)
            next(colors)

    def init_storage_pieces(self):
        row = 0
        for c in Coloration:
            col = 0
            self.board.append([])
            for h in Hole:
                for sh in Shape:
                    for si in Size:
                        self.board[row].append(Piece(row, col, c, sh, si, h))
                        col += 1
            row += 1
            print(self.__repr__())

    def get_piece(self, row, col):
        return(self.board[row][col])

    def draw(self, win):
        self.draw_cells(win)
        for row in range(SROWS):
            for col in range(SCOLS):
                piece = self.board[row][col]
                piece.draw(win)

    def move_to_gameboard(self, game_board, piece, row, col):
        self.board[piece.row][piece.col] = 0
        game_board.put_piece(piece, row, col)
