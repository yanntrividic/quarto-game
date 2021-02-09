'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg
from quarto.constants import DBROWN, SQUARE_SIZE
from quarto.pieces.piece import Piece
from quarto.pieces.types import Coloration, Hole, Shape, Size


# TODO: I'm not sure if having two additional classes is a good idea.
#  we might have to make it only one class
class Board:

    def __init__(self, name, storage, rows, cols, x_offset, y_offset, board_outline, light_color, dark_color):
        self.name = name
        self.storage = storage
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # _ is a standard placeholder to ignore the warning

        self.selected_piece = None  # if we have selected a piece or not
        self.pieces_count = 0  # number of pieces on the board
        self.rows = rows  # number of rows of the board
        self.cols = cols  # number of cols of the board

        self.x_offset = x_offset  # x position where we start drawing the board
        self.y_offset = y_offset  # y position where we start drawing the board
        self.board_outline = board_outline  # outline thickness of the board

        self.colors = (light_color, dark_color)  # colors of the board's squares
        self.init_pieces()

    def init_pieces(self):
        if(self.storage):
            row = 0
            for c in Coloration:
                col = 0
                for h in Hole:
                    for sh in Shape:
                        for si in Size:
                            self.board[row][col] = Piece(row, col, c, sh, si, h)
                            col += 1
                row += 1
            print("Initialization:")
        else:
            print("Initialization:")
        print(self.__repr__())

    def get_piece(self, row, col):
        return(self.board[row][col])

    def put_piece(self, piece, row, col):
        self.board[row][col] = piece
        piece.move_to_gameboard(row, col)

    def move_to_gameboard(self, game_board, piece, row, col):
        try:
            self.board[piece.row][piece.col] = 0
            game_board.put_piece(piece, row, col)
        except AttributeError:
            print("Type not valid.")

    def draw_cells(self, win):
        rect = (self.x_offset - self.board_outline,
                self.y_offset - self.board_outline,
                SQUARE_SIZE * self.cols + 2 * self.board_outline,
                SQUARE_SIZE * self.rows + 2 * self.board_outline)
        pg.draw.rect(win, DBROWN, rect)
        iter_colors = itertools.cycle(self.colors)
        for x in range(self.cols):
            for y in range(self.rows):
                rect = (x * SQUARE_SIZE + self.x_offset,
                        y * SQUARE_SIZE + self.y_offset,
                        SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(win, next(iter_colors), rect)
            next(iter_colors)

    def draw(self, win):
        self.draw_cells(win)
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col] != 0):
                    piece = self.board[row][col]
                    piece.draw(win)

    def __repr__(self):
        s = self.name + ":\n"
        for x in range(self.rows):
            for y in range(self.cols):
                s += ((str(self.board[x][y]) + " ") if(self.board[x][y]) != 0 else "---- ")
            s += '\n'
        return(s)
