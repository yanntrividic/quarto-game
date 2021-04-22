'''
Created on Feb 6, 2021

@author: yann
'''

import itertools

import pygame as pg
from .constants import DBROWN, SQUARE_SIZE
from .pieces.piece import Piece
from .pieces.types import Coloration, Hole, Shape, Size


class Board:

    def __init__(self, name, storage, rows, cols, x_offset, y_offset, board_outline, light_color, dark_color):
        '''
        A class to represent the game board

        Attributes
        ----------
        name : String
            The name of the board
        storage :
            The storage board
        board: int [][]
            the game board
        pieces_count: int
            number of pieces on the board
        rows: int
            number of rows of the board
        cols: int
            number of cols of the board
        x_offset: ints
            x position where we start drawing the board
        y_offset: int
            y position where we start drawing the board
        board_outline:
            outline thickness of the board
        colors: pygame.Color()
            colors of the board's squares
        selected_square:
            The square selected by the user
        '''
        self.__name__ = name
        self.storage = storage
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # _ is a standard placeholder to ignore the warning

        self.pieces_count = 0
        self.rows = rows
        self.cols = cols

        self.x_offset = x_offset
        self.y_offset = y_offset
        self.board_outline = board_outline

        self.__colors = (light_color, dark_color)
        self.__init_pieces()

        self.selected_square = None

    def __init_pieces(self):
        '''
        Initialize the pieces in the storage board, the 2^4 differents onew
        '''
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
        # Represent the storage board in the terminal
        print("Initialization:")
        print(self.__repr__())

    def get_piece(self, row, col):
        return(self.board[row][col])

    def put_piece(self, piece, row, col):
        '''
        Put the piece on the game board

        Parameters
        ----------

        piece : Piece
            The selected piece
        row : int
            the row of the piece
        col : int
            the column of the piece
        '''

        self.board[row][col] = piece
        piece.move_to_gameboard(row, col)

    def move_to_gameboard(self, game_board, piece, row, col):
        '''
        Put a piece on the game board

        Parameters
        ----------

        game_board : Board
            The game board
        piece : Piece
            The selected piece
        row : int
            the row where the piece will be on the game board
        col : int
            the column where the piece will be on the game board
        '''
        try:
            self.board[piece.row][piece.col] = 0
            game_board.put_piece(piece, row, col)
            return(piece)
        except AttributeError:
            print("Type not valid.")

    def get_row_col_from_mouse(self, pos):  # returns a row, a col or false
        '''
        Get the row and column of the selected cell with the mouse

        Parameters
        ----------

        pos : (int,int)
            the position of the selected cell
        '''
        x, y = pos
        if((x < (self.x_offset + self.cols * SQUARE_SIZE)) &
           (x > self.x_offset) &
           (y < self.y_offset + self.rows * SQUARE_SIZE) &
           (y > self.y_offset)):
            row = (y - self.y_offset) // SQUARE_SIZE
            col = (x - self.x_offset) // SQUARE_SIZE
            print('Clicked cell: ' + self.__name__ + "[" + str(row) + "," + str(col) + "]")
            return((row, col))
        else:
            return(-1, -1)

    def winner(self):
        '''
        Check if a player has won
        '''
        if self.__check_all_lines():
            return True
        return False

    def is_full(self):
        '''
        Check if the board is full
        '''
        for row in range(self.rows):
            if 0 in self.board[row]:
                return False
        return True

    def __is_winning_line(self, pieces):
        '''
        Check if a line is full of the same symbol

        Parameters
        ----------
        Pieces :  int[]
            the pieces in a line
        '''
        if 0 in pieces:
            return False
        p = pieces[0]
        ho, si, sh, co = True, True, True, True
        for piece in pieces:
            ho = (p.hole == piece.hole and ho)
            si = (p.size == piece.size and si)
            sh = (p.shape == piece.shape and sh)
            co = (p.coloration == piece.coloration and co)
        return(ho or si or sh or co)

    def __check_all_lines(self):
        '''
        Check each rows and columns to see if a player has won.
        '''
        for row in range(self.rows):  # checks every line
            if not(0 in self.board[row]):
                if self.__is_winning_line(self.board[row]):
                    return(True)

        for col in range(self.cols):  # check every cols
            pieces = []
            for row in range(self.rows):
                pieces.append(self.board[row][col])
            if not(0 in pieces):
                if self.__is_winning_line(pieces):
                    return(True)

        if(self.cols == self.rows):  # if we have a square board
            pieces = []
            pieces2 = []
            for col in range(self.cols):  # check all diagonals
                pieces.append(self.board[col][col])
                pieces2.append(self.board[col][self.cols - col - 1])
            if not(0 in pieces):
                if self.__is_winning_line(pieces):
                    return(True)
            if not(0 in pieces2):
                if self.__is_winning_line(pieces2):
                    return(True)

    def get_valid_moves(self, verbose=False):
        '''
        Check which are the valid moves

        Parameters
        ----------
        print : Boolean
            If we want to show the moves on the terminal
        '''
        m = ""
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if not self.storage:
                    if piece == 0:
                        moves.append((row, col))
                        m += str((row, col)) + ", "
                else:
                    if piece != 0:
                        moves.append((row, col))
                        m += str((row, col)) + ", "
        # Represents the moves on the terminal
        if verbose:
            print("moves = [" + m + "]")
        return moves

    def draw(self, win):
        '''
        Draw the board

        Parameters
        ----------
        win : Pygame window for display
        The window where the game is displayed
        '''
        self.__draw_cells(win)
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col] != 0):
                    piece = self.board[row][col]
                    piece.draw(win)

    def __draw_cells(self, win):
        '''
        Draw the cells of the board

        Parameters
        ----------
        win : Pygame window for display
        The window where the game is displayed

        '''
        rect = (self.x_offset - self.board_outline,
                self.y_offset - self.board_outline,
                SQUARE_SIZE * self.cols + 2 * self.board_outline,
                SQUARE_SIZE * self.rows + 2 * self.board_outline)

        pg.draw.rect(win, DBROWN, rect)
        iter_colors = itertools.cycle(self.__colors)

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

    def __repr__(self):
        '''
        represent the object in a string format
        '''
        s = self.__name__ + ":\n"
        for x in range(self.rows):
            for y in range(self.cols):
                s += ((str(self.board[x][y]) + " ") if(self.board[x][y]) != 0 else "---- ")
            s += '\n'
        return(s)

    def display(self, depth):
        '''
        represent the object in a string format
        '''
        s = "\t" * abs(2 - depth) + self.__name__ + ":\n"
        for x in range(self.rows):
            s += "\t" * abs(2 - depth)
            for y in range(self.cols):
                s += ((str(self.board[x][y]) + " ") if(self.board[x][y]) != 0 else "---- ")
            s += '\n'
        return(s)
