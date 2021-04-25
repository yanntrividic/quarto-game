'''
Created on Feb 12, 2021

@author: yann
'''

# from random import randint
# from time import sleep

import pygame as pg
from quarto.players.agents import AI_level1, AI_level2, AI_level3

from .board import Board
from .constants import (BOARDOUTLINE, SQUARE_SIZE,
                        GROWS, GCOLS, GXOFFSET, GYOFFSET,
                        SROWS, SCOLS, SXOFFSET, SYOFFSET,
                        LGREEN, GREEN, DGREEN, BROWN, DBROWN, WHEAT, PAYAYA, BG, LGRAY,
                        PLAYER1, PLAYER2, AI1, AI2, TIE,
                        RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT,
                        TXT_X, TXT_Y,
                        X_LEFT_ARROWS, X_RIGHT_ARROWS, Y_TOP_ARROWS, Y_BOT_ARROWS)
from .players.human import Human


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
        self.__init()  # initialization of the baords
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
        self.__draw_players_txt()
        self.__draw_turn_txt()
        self.__draw_change_players(self.win)
        pg.display.update()

    def __init(self):
        self.selected_piece = None  # if we have selected a piece or not
        self.game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.turn = True
        self.players1 = self.__init_players(PLAYER1, 1)
        self.players2 = self.__init_players(PLAYER2, 2)
        self.player1 = self.players1[0]  # is the index in the players1 array
        self.player2 = self.players2[3]
        self.pick = True
        self.valid_moves = []  # at first, no piece is selected so no valid moves

    def __init_players(self, p, number):
        human = Human(p)
        ai_lvl1 = AI_level1("RANDOM" + str(number))  # TODO add ai
        ai_lvl2 = AI_level2("NOVICE" + str(number))
        ai_lvl3 = AI_level3("MINIMAX" + str(number))
        return [human, ai_lvl1, ai_lvl2, ai_lvl3]

    def reset(self):
        '''
        Resets the game.
        '''
        print("The game is being reset.")
        self.__init()
        print(self)

    def select(self, row=-1, col=-1):
        '''
        Select a piece from the storage board if no piece is selected, or moves
        the selected piece to the selected location otherwise

        Parameters
        ----------
        row : int
            the row of the selected piece
        col : int
            the column of the selected piece
        '''
        # print this as a text on the terminal
        print("Selected piece:", row, col, self.selected_piece)

        if self.turn:
            return self.player1.select(self, row, col)
        else:
            return self.player2.select(self, row, col)

    def winner(self):
        '''
        Says if there is a winner and if there is, says who is the winner
        '''
        if self.game_board.winner():
            self.__draw_reset_button()
            return(self.__get_player1() if self.turn else self.__get_player2())
        elif self.game_board.is_full():
            self.__draw_reset_button()
            return TIE
        return None

    def move(self, row, col):
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

    def __draw_valid_moves(self, moves):
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

    def __draw_turn_txt(self):
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

    def __draw_reset_button(self):
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

    def __draw_players_txt(self):
        '''
        Draws the top left texts
        '''
        text_surface1, _ = self.font.render(self.__get_player1(), LGRAY if self.turn else WHEAT)
        text_surface2, _ = self.font.render(self.__get_player2(), WHEAT if self.turn else LGRAY)
        self.win.blit(text_surface1, (X_LEFT_ARROWS + 20, Y_TOP_ARROWS - 14))
        self.win.blit(text_surface2, (X_LEFT_ARROWS + 20, Y_BOT_ARROWS - 14))

    def __draw_change_players(self, win):
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

        pg.draw.polygon(win, LGRAY if self.turn else PAYAYA, points_player1_arrow_left)
        pg.draw.polygon(win, LGRAY if self.turn else PAYAYA, points_player1_arrow_right)
        pg.draw.polygon(win, PAYAYA if self.turn else LGRAY, points_player2_arrow_left)
        pg.draw.polygon(win, PAYAYA if self.turn else LGRAY, points_player2_arrow_right)

    def __get_arrow_bounding_box(self, x, y):
        '''
        Returns a stupid bounding box for the arrows, could be better
        '''
        return x - 32, x + 32, y - 17, y + 7

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

    def is_reset_clicked(self, pos):
        '''
        Checks if the user clicks the reset button or not
        '''
        x, y = pos  # unpacks the mouse button
        if x > RESET_X and x < RESET_X + RESET_WIDTH and y > RESET_Y and y < RESET_Y + RESET_HEIGHT:
            return True
        return False

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

    def is_human_turn(self):
        if (self.turn and isinstance(self.player1, Human) or
           (not self.turn and isinstance(self.player2, Human))):
            return True
        return False

    def swap_players(self, clicked_arrow):
        '''
        Swaps players according to the arrow that was clicked.
        '''
        x_arrow, y_arrow = clicked_arrow

        p = None

        if x_arrow == X_LEFT_ARROWS:
            if y_arrow == Y_TOP_ARROWS and not self.turn:
                self.player1 = self.players1[(self.players1.index(self.player1) - 1) % len(self.players1)]
                p = self.__get_player1()
            if y_arrow == Y_BOT_ARROWS and self.turn:
                self.player2 = self.players2[(self.players2.index(self.player2) - 1) % len(self.players2)]
                p = self.__get_player2()

        else:
            if y_arrow == Y_TOP_ARROWS and not self.turn:
                self.player1 = self.players1[(self.players1.index(self.player1) + 1) % len(self.players1)]
                p = self.__get_player1()
            if y_arrow == Y_BOT_ARROWS and self.turn:
                self.player2 = self.players2[(self.players2.index(self.player2) + 1) % len(self.players2)]
                p = self.__get_player2()

        if p is not None:
            print("Player changed:", p)

    def __change_turn(self):
        '''
        Changes the turn value.
        '''
        if self.pick:
            self.turn = not(self.turn)
        print("This is now " + (self.__get_player1() if self.turn else self.__get_player2()) + "'s turn.")

    def __change_pick_move(self):
        '''
        Changes the pick value.
        '''
        self.pick = not(self.pick)
        print("This is now time to " + ("pick a" if self.turn else "move the") + " piece.")

    def end_turn(self, selected_square=None):
        self.storage_board.selected_square = selected_square
        self.__change_turn()
        self.__change_pick_move()

    def __get_player1(self):
        return self.player1.__name__

    def __get_player2(self):
        return self.player2.__name__

    def __repr__(self):
        '''
        represent the object in a string format
        '''
        return(self.game_board.__repr__() +
               self.storage_board.__repr__() + "\n")
