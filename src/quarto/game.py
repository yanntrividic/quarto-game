'''
Created on Feb 12, 2021

@author: yann
'''

import pygame as pg
from quarto.board import Board
from quarto.constants import (BOARDOUTLINE,
                              GROWS, GCOLS, GXOFFSET, GYOFFSET,
                              SROWS, SCOLS, SXOFFSET, SYOFFSET,
                              LGREEN, GREEN)


class Game:
    '''
    classdocs
    '''

    def __init__(self, win):
        '''
        Constructor
        '''

        self.selected_piece = None  # if we have selected a piece or not
        self.game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE - 5, LGREEN, GREEN)
        # self.turn = PLAYER1
        self.valid_moves = {}
        self.win = win

    def update(self):
        self.game_board.draw(self.win)
        self.storage_board.draw(self.win)
        pg.display.update()
