'''
Created on Feb 12, 2021

@author: yann
'''

import pygame as pg
from quarto.board import Board
from quarto.constants import (BOARDOUTLINE, SQUARE_SIZE,
                              GROWS, GCOLS, GXOFFSET, GYOFFSET,
                              SROWS, SCOLS, SXOFFSET, SYOFFSET,
                              LGREEN, GREEN, DGREEN, DBROWN, BG,
                              PLAYER1, PLAYER2, TIE)


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
        board where the game takes place 
    storage_board : Board
        board where the pieces are located before being chosed
    valid_moves : dict
        all the valids moves that the player can do
    turn : bool
        True if PLAYER1 has to play, False if PLAYER2 has to play
    pick :
         True if the player has to pick a piece, False if the player has to move the piece
    Methods
    -------
    update()
        Updates the positions of the pieces relative to the boards in the window.
    reset()
        Resets the game.
    select(row, col)
        when the player choose a piece from the storage board
    move(row, col)
        when the player put a piece on the game board
    '''

    def __init__(self, win):
        '''
        Instantiates a new Game object.

        Parameters
        ----------
        win : Pygame window for display
        The window where the game is displayed
            
        '''
        self._init()  # initialization of the baords
        self.win = win

    def update(self, font):
        '''
        Updates the window

        Parameters
        ----------
        font : String
            The font of the caracters in the game

        '''
        self.win.fill(BG)
        self.game_board.draw(self.win)
        self.storage_board.draw(self.win)
        # self.draw_valid_moves(self.valid_moves)
        self.draw_turn_txt(font)
        pg.display.update()

    def _init(self):
        self.selected_piece = None  # if we have selected a piece or not
        self.game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
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
        Select a piece from the storage board

        Parametres
        ----------
        row : int
            the row of the selected piece
        col : int
            the column of the selected piece 
        '''
        #print this as a text on the terminal
        print("Selected piece:", row, col, self.selected_piece)
        if self.pick:  # when it's time to pick a piece from the storage board.
            if self.storage_board.get_piece(row, col) != 0:
                self.selected_piece = self.storage_board.get_piece(row, col)
                self.valid_moves = self.game_board.get_valid_moves()
                self.storage_board.selected_square = (col, row)
                self.change_turn()
                self.change_pick_move()
            else:
                self.selected_piece = None

        else:
            result = self._move(row, col)

            if not result:
                print("Invalid position, try again")
                return False

            self.selected_piece = None
            self.valid_moves = []
            self.storage_board.selected_square = None
            self.change_turn()
            self.change_pick_move()

        return True

    def winner(self):
        '''
        Say if there is a winner and who is the winner
        '''
        if self.game_board.winner():
            return(PLAYER1 if self.turn else PLAYER2)
        elif self.game_board.is_full():
            return TIE
        return None

    def _move(self, row, col):
        '''
        Moves the selected_piece to the x, y position given as parameter on the game_board
        Parameters
        ----------
        row : int
            the row of the selected piece
        col : int
            the column of the selected piece 
        
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
        ----------
        moves: list of (int, int)
            list of valid moves represented as tuples of board coordinates (row, col)
        '''
        for move in moves:
            row, col = move
            pg.draw.circle(self.win, DGREEN,
                           (self.game_board.x_offset + int(SQUARE_SIZE * col) + SQUARE_SIZE // 2,
                            self.game_board.y_offset + int(SQUARE_SIZE * row) + SQUARE_SIZE // 2), 15)

    def draw_turn_txt(self, font):
        '''
        Displays on the window a text that tell:

        Parameters
        ----------
        font : the font used for the text
        '''
        if self.winner():
            if self.winner() == TIE :
                txt = "Tie! Nobody won."
            else :
                txt = (PLAYER1 if self.turn else PLAYER2) + " wins!!"
        else:
            txt = (PLAYER1 if self.turn else PLAYER2) + ", " + str("pick a" if self.pick else "move the") + " piece!"
        text_surface, _ = font.render(txt, DBROWN)
        self.win.blit(text_surface, (40, 250))

    def change_turn(self):
        '''
        Changes the turn value.
        '''
        if self.pick:
            self.turn = not(self.turn)
        print("This is now " + (PLAYER1 if self.turn else PLAYER2) + "'s turn.")

    def get_row_col_from_mouse(self, pos):
        '''
        Gets the (row, col) coordinates of where the player clicked depending on
        the self.pick value (i.e. depending on if it was time to pick a piece or
        to move one.

        Parameters
        ----------
        pos : (int, int)
            (x, y) position of the pixel clicked.
        '''
        if(self.pick):
            return(self.storage_board.get_row_col_from_mouse(pos))
        else:
            return(self.game_board.get_row_col_from_mouse(pos))

    def change_pick_move(self):
        '''
        Changes the pick value.
        '''
        self.pick = not(self.pick)
        print("This is now time to " + ("pick a" if self.turn else "move the") + " piece.")

    def __repr__(self):
        '''
        represent the object in a string format
        '''
        return(self.game_board.__repr__() +
            self.storage_board.__repr__() + "\n")
