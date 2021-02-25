'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg
from quarto.constants import DBROWN, SQUARE_SIZE
from quarto.pieces.piece import Piece
from quarto.pieces.types import Coloration, Hole, Shape, Size


class Board:

    def __init__(self, name, storage, rows, cols, x_offset, y_offset, board_outline, light_color, dark_color):
        '''
        A class to represent the game board

        Attributes
        ----------
        name : String
        storage :
        board:
        pieces_count:
        rows:
        cols:
        x_offset:
        y_offset:
        board_outline:
        colors:
        selected_square:
        '''
        self.name = name
        self.storage = storage
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # _ is a standard placeholder to ignore the warning

        self.pieces_count = 0  # number of pieces on the board
        self.rows = rows  # number of rows of the board
        self.cols = cols  # number of cols of the board

        self.x_offset = x_offset  # x position where we start drawing the board
        self.y_offset = y_offset  # y position where we start drawing the board
        self.board_outline = board_outline  # outline thickness of the board

        self.colors = (light_color, dark_color)  # colors of the board's squares
        self.init_pieces()

        self.selected_square = None

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
            return(piece)
        except AttributeError:
            print("Type not valid.")

    def get_row_col_from_mouse(self, pos):  # returns a row, a col or false
        x, y = pos
        if((x < (self.x_offset + self.cols * SQUARE_SIZE)) &
           (x > self.x_offset) &
           (y < self.y_offset + self.rows * SQUARE_SIZE) &
           (y > self.y_offset)):
            row = (y - self.y_offset) // SQUARE_SIZE
            col = (x - self.x_offset) // SQUARE_SIZE
            print('Clicked cell: ' + self.name + "[" + str(row) + "," + str(col) + "]")
            return((row, col))
        else:
            return(-1, -1)

    def winner(self):
        if self._check_all_lines():
            return True
        return False

    def _is_winning_line(self, pieces):
        if 0 in pieces:
            return False
        p = pieces[0]
        h, s, sh, c = True, True, True, True
        for piece in pieces:
            h = (p.coloration == piece.coloration and h)
            s = (p.size == piece.coloration and s)
            sh = (p.shape == piece.shape and sh)
            c = (p.coloration == piece.coloration and c)
        return(h or s or sh or c)

    def _check_all_lines(self):
        for row in range(self.rows):  # checks every line
            if self._is_winning_line(self.board[row]):
                return(True)

        for col in range(self.cols):  # check every cols
            pieces = []
            for row in range(self.rows):
                pieces.append(self.board[row][col])
            if self._is_winning_line(pieces):
                return(True)

        if(self.cols == self.rows):  # if we have a square board
            pieces = []
            pieces2 = []
            for col in range(self.cols):  # check all diagonals
                pieces.append(self.board[col][col])
                pieces2.append(self.board[col][self.cols - col - 1])
            if self._is_winning_line(pieces) | self._is_winning_line(pieces2):
                return(True)

    def get_valid_moves(self, print=False):
        m = ""
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece == 0:
                    moves.append((row, col))
                    m += str((row, col)) + ", "
        if print:
            print("moves = [" + m + "]")
        return moves

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
                if self.selected_square != (x, y):
                    pg.draw.rect(win, next(iter_colors), rect)
                else:
                    pg.draw.rect(win, DBROWN, rect)
                    next(iter_colors)
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
