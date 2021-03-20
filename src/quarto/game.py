'''
Created on Feb 12, 2021

@author: yann
'''

from random import randint
from time import sleep

import pygame as pg
from quarto.board import Board
from quarto.constants import (BOARDOUTLINE, SQUARE_SIZE,
                              GROWS, GCOLS, GXOFFSET, GYOFFSET,
                              SROWS, SCOLS, SXOFFSET, SYOFFSET,
                              LGREEN, GREEN, DGREEN, BROWN, DBROWN, WHEAT, PAYAYA, BG,
                              PLAYER1, PLAYER2, AI1, AI2, AI3, TIE,
                              RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT,
                              TXT_X, TXT_Y,
                              X_LEFT_ARROWS, X_RIGHT_ARROWS, Y_TOP_ARROWS, Y_BOT_ARROWS)


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

    def __init__(self, win, font):
        '''
        Instantiates a new Game object.

        Parameters
        ----------
        win : Pygame window for display
        The window where the game is displayed
        '''
        self._init()  # initialization of the baords
        self.win = win
        self.font = font

    def update(self):
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
        # self._draw_valid_moves(self.valid_moves)
        self._draw_players_txt()
        self._draw_turn_txt()
        self._draw_change_players(self.win)
        pg.display.update()

    def _init(self):
        self.selected_piece = None  # if we have selected a piece or not
        self.game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.turn = True  # TODO: how to handle this ? Technically, we only need a boolean
        self.players1 = [PLAYER1, AI1, AI2, AI3]
        self.players2 = [PLAYER2, AI1, AI2, AI3]
        self.player1 = 0  # is the index in the players1 array
        self.player2 = 0
        self.pick = True
        self.valid_moves = []  # at first, no piece is selected so no valid moves

    def reset(self):
        '''
        Resets the game.
        '''
        print("The game is being reset.")
        self._init()
        print(self)

    def select(self, row, col):
        '''
        Select a piece from the storage board

        Parameters
        ----------
        row : int
            the row of the selected piece
        col : int
            the column of the selected piece
        '''
        # print this as a text on the terminal
        print("Selected piece:", row, col, self.selected_piece)

        if (self.player1 == 0 and self.turn) or (self.player2 == 0 and not self.turn):
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

                # FIXME: Unsuccessful attempt at building a random "AI"
#         if (self.player1 == 1 and self.turn) or (self.player2 == 1 and not self.turn):
#
#             rand_col = randint(0, SCOLS - 1)
#             rand_row = randint(0, SROWS - 1)
#
#             if self.pick:
#                 if self.storage_board.get_piece(rand_row, rand_col) != 0:
#                     self.selected_piece = self.storage_board.get_piece(row, col)
#                     self.valid_moves = self.game_board.get_valid_moves()
#                     self.storage_board.selected_square = self.valid_moves[randint(0, len(self.valid_moves) - 1)]
#                     self.change_turn()
#                     self.change_pick_move()
#                 else:
#                     self.selected_piece = None
#
#             else:
#                 rand_valid_move = self.valid_moves[randint(0, len(self.valid_moves))]
#                 sleep(1)
#                 result = self._move(rand_valid_move[0], rand_valid_move[1])
#                 self.selected_piece = None
#                 self.valid_moves = []
#                 self.storage_board.selected_square = None
#                 self.change_turn()
#                 self.change_pick_move()

        return True

    def winner(self):
        '''
        Says if there is a winner and if there is, says who is the winner
        '''
        if self.game_board.winner():
            self._draw_reset_button()
            return(self.__get_player1() if self.turn else self.__get_player2())
        elif self.game_board.is_full():
            self._draw_reset_button()
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

    def _draw_valid_moves(self, moves):
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

    def _draw_turn_txt(self):
        '''
        Displays on the window a text that tell:

        Parameters
        ----------
        font : the font used for the text
        '''
        if self.winner():
            if self.winner() == TIE:
                txt = "Tie! Nobody won."
            else:
                txt = (self.__get_player1() if self.turn else self.__get_player2()) + " wins!!"
        else:
            txt = (self.__get_player1() if self.turn else self.__get_player2()) + ", " + str("pick a" if self.pick else "move the") + " piece!"
        text_surface, _ = self.font.render(txt, DBROWN)
        self.win.blit(text_surface, (TXT_X, TXT_Y))

    def _draw_reset_button(self):
        '''
        Method to display the reset button once the game is over
        '''
        rect_outline = (RESET_X - BOARDOUTLINE, RESET_Y - BOARDOUTLINE,
                        RESET_WIDTH + 2 * BOARDOUTLINE, RESET_HEIGHT + 2 * BOARDOUTLINE)
        pg.draw.rect(self.win, DBROWN, rect_outline)

        rect = (RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT)
        pg.draw.rect(self.win, BROWN, rect)

        text_surface_reset, _ = self.font.render("RESET", DBROWN)
        self.win.blit(text_surface_reset, (RESET_X + 60, RESET_Y + 25))

    def is_reset_clicked(self, pos):
        '''
        Checks if the user clicks the reset button or not
        '''
        x, y = pos  # unpacks the mouse button
        if x > RESET_X and x < RESET_X + RESET_WIDTH and y > RESET_Y and y < RESET_Y + RESET_HEIGHT:
            return True
        return False

    def _draw_players_txt(self):
        '''
        Draws the top left texts
        '''
        text_surface1, _ = self.font.render(self.__get_player1(), WHEAT)
        text_surface2, _ = self.font.render(self.__get_player2(), WHEAT)
        self.win.blit(text_surface1, (X_LEFT_ARROWS + 20, Y_TOP_ARROWS - 12))
        self.win.blit(text_surface2, (X_LEFT_ARROWS + 20, Y_BOT_ARROWS - 12))

    def _draw_change_players(self, win):
        '''
        Draws the top right texts (Players, arrows, etc)
        '''

        text_surface, _ = self.font.render("Players", DBROWN)
        self.win.blit(text_surface, (X_LEFT_ARROWS + 30, Y_TOP_ARROWS - 60))

        points_player1_arrow_left = [(X_LEFT_ARROWS, Y_TOP_ARROWS), (X_LEFT_ARROWS - 20, Y_TOP_ARROWS),
                                     (X_LEFT_ARROWS - 20, Y_TOP_ARROWS + 7), (X_LEFT_ARROWS - 32, Y_TOP_ARROWS - 5),
                                     (X_LEFT_ARROWS - 20, Y_TOP_ARROWS - 10 - 7), (X_LEFT_ARROWS - 20, Y_TOP_ARROWS - 10),
                                     (X_LEFT_ARROWS, Y_TOP_ARROWS - 10)]

        points_player1_arrow_right = [(X_RIGHT_ARROWS, Y_TOP_ARROWS), (X_RIGHT_ARROWS + 20, Y_TOP_ARROWS),
                                      (X_RIGHT_ARROWS + 20, Y_TOP_ARROWS + 7), (X_RIGHT_ARROWS + 32, Y_TOP_ARROWS - 5),
                                      (X_RIGHT_ARROWS + 20, Y_TOP_ARROWS - 10 - 7), (X_RIGHT_ARROWS + 20, Y_TOP_ARROWS - 10),
                                      (X_RIGHT_ARROWS, Y_TOP_ARROWS - 10)]

        points_player2_arrow_left = [(X_LEFT_ARROWS, Y_BOT_ARROWS), (X_LEFT_ARROWS - 20, Y_BOT_ARROWS),
                                     (X_LEFT_ARROWS - 20, Y_BOT_ARROWS + 7), (X_LEFT_ARROWS - 32, Y_BOT_ARROWS - 5),
                                     (X_LEFT_ARROWS - 20, Y_BOT_ARROWS - 10 - 7), (X_LEFT_ARROWS - 20, Y_BOT_ARROWS - 10),
                                     (X_LEFT_ARROWS, Y_BOT_ARROWS - 10)]

        points_player2_arrow_right = [(X_RIGHT_ARROWS, Y_BOT_ARROWS), (X_RIGHT_ARROWS + 20, Y_BOT_ARROWS),
                                      (X_RIGHT_ARROWS + 20, Y_BOT_ARROWS + 7), (X_RIGHT_ARROWS + 32, Y_BOT_ARROWS - 5),
                                      (X_RIGHT_ARROWS + 20, Y_BOT_ARROWS - 10 - 7), (X_RIGHT_ARROWS + 20, Y_BOT_ARROWS - 10),
                                      (X_RIGHT_ARROWS, Y_BOT_ARROWS - 10)]

        pg.draw.polygon(win, PAYAYA, points_player1_arrow_left)
        pg.draw.polygon(win, PAYAYA, points_player1_arrow_right)
        pg.draw.polygon(win, PAYAYA, points_player2_arrow_left)
        pg.draw.polygon(win, PAYAYA, points_player2_arrow_right)

    def __get_arrow_bounding_box(self, x, y):
        '''
        Returns a stupid bounding box for the arrows, could be better
        '''
        return x - 32, x + 32, y - 17, y + 7

    def is_arrow_clicked(self, pos):
        '''
        Checks if the user clicks within one of the bounding boxes and returns the associated coordinates
        '''
        x, y = pos
        for x_arrow in [X_LEFT_ARROWS, X_RIGHT_ARROWS]:
            for y_arrow in [Y_TOP_ARROWS, Y_BOT_ARROWS]:
                x1, x2, y1, y2 = self.__get_arrow_bounding_box(x_arrow, y_arrow)
                if x > x1 and x < x2 and y > y1 and y < y2:
                    return x_arrow, y_arrow
        return None

    def swap_players(self, clicked_arrow):
        '''
        Swaps players according to the arrow that was clicked.
        '''
        x_arrow, y_arrow = clicked_arrow

        if x_arrow == X_LEFT_ARROWS:
            if y_arrow == Y_TOP_ARROWS:
                self.player1 = (self.player1 - 1) % len(self.players1)
                p = self.__get_player1()
            else:
                self.player2 = (self.player2 - 1) % len(self.players2)
                p = self.__get_player2()

        else:
            if y_arrow == Y_TOP_ARROWS:
                self.player1 = (self.player1 + 1) % len(self.players1)
                p = self.__get_player1()
            else:
                self.player2 = (self.player2 + 1) % len(self.players2)
                p = self.__get_player2()

        print("Player changed:", p)

    def change_turn(self):
        '''
        Changes the turn value.
        '''
        if self.pick:
            self.turn = not(self.turn)
        print("This is now " + (self.__get_player1() if self.turn else self.__get_player2()) + "'s turn.")

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

    def __get_player1(self):
        return self.players1[self.player1]

    def __get_player2(self):
        return self.players2[self.player2]

    def __repr__(self):
        '''
        represent the object in a string format
        '''
        return(self.game_board.__repr__() +
               self.storage_board.__repr__() + "\n")
