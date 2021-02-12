'''
Created on Feb 12, 2021

@author: yann
'''

import pygame as pg
from quarto.board import Board
from quarto.constants import (BOARDOUTLINE, SQUARE_SIZE,
                              GROWS, GCOLS, GXOFFSET, GYOFFSET,
                              SROWS, SCOLS, SXOFFSET, SYOFFSET,
                              LGREEN, GREEN, DGREEN)


class Game:
    '''
    A class used to represent a Quarto! game.

    ...

    Attributes
    ----------
    win : Pygame window for display
        The window where the game is displayed
    selected_piece : Piece
        None is no piece is selected, a Piece object waiting to be moved if a piece is selected
    game_board : Board
        bla
    storage_board : Board
        bla
    valid_moves : dict
        bla
    turn : bool
        True if player1 has to play, False if player2 has to play
    pick :
         True if the player has to pick a piece, False if the player has to move the piece
    Methods
    -------
    update()
        Updates the positions of the pieces relative to the boards in the window.
    reset()
        Resets the game.
    select(row, col)
        bla
    move(row, col)
        bla
    '''

    def __init__(self, win):
        '''
        Instantiates a new Game object.

        Parameters
        ---------
        win:
            bla
        '''
        self._init()  # initialization of the baords
        self.win = win

    def update(self):
        '''
        Updates the window
        '''
        self.game_board.draw(self.win)
        self.storage_board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pg.display.update()

    def _init(self):
        self.selected_piece = None  # if we have selected a piece or not
        self.game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE - 5, LGREEN, GREEN)
        self.turn = True  # TODO: how to handle this ? Technically, we only need a boolean
        self.pick = True
        self.valid_moves = []  # at first, no piece is selected so no valid moves

    def reset(self):
        '''
        Resets the game.
        '''
        self._init()

    def select(self, row, col):
        '''
        Displays on the window a circle at position where a move is valid to the player

        Parameters
        ---------
        row : int
            bla
        col : int
        '''
        if self.selected_piece:  # if we've already selected something, we move it to the position passed as a parameter
            print("Selected piece:", row, col, self.selected_piece)
            self.change_turn()
            self.change_pick_move()
            result = self._move(row, col)  # return either a valid position or false
            if not result:
                self.selected_piece = None  # resets the selected piece to None
                self.select(row, col)  # gets us into the else block just below

        else:
            piece = self.storage_board.get_piece(row, col)  # gets the value of the piece at this position in the storage board
            if piece != 0:  # if this value is not zero (i.e. if there is a piece in it)
                self.selected_piece = piece  # this piece becomes the new selected piece
                self.valid_moves = self.game_board.get_valid_moves()  # and we get the list of valid moves available
                return True

        return False  # no piece could be selected with this iteration

    def _move(self, row, col):
        '''
        Displays on the window a circle at position where a move is valid to the player

        Parameters
        ---------
        moves : list of (int, int)
            list of valid moves represented as tuples of board coordinates (row, col)
        '''
        if self.selected_piece and (row, col) in self.valid_moves:
            self.storage_board.move_to_gameboard(self.game_board, self.selected_piece, row, col)
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        '''
        Displays on the window a circle at position where a move is valid to the player

        Parameters
        ---------
        moves: list of (int, int)
            list of valid moves represented as tuples of board coordinates (row, col)
        '''
        for move in moves:
            row, col = move
            pg.draw.circle(self.win, DGREEN,
                           (self.game_board.x_offset + int(SQUARE_SIZE * row) + SQUARE_SIZE // 2,
                            self.game_board.y_offset + int(SQUARE_SIZE * col) + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        '''
        Changes the turn value.
        '''
        self.turn = not(self.turn)
        print("This is now " + ("Player1" if self.turn else "Player2") + "'s turn.")

    def change_pick_move(self):
        '''
        Changes the pick value.
        '''
        self.pick = not(self.pick)
        print("This is now time to " + ("pick a" if self.turn else "move the") + " piece.")

    def __repr__(self):
        return(# ("Player 1" if self.turn else "Player 2") + "\n" +
               self.game_board.__repr__() +
               self.storage_board.__repr__() + "\n")
