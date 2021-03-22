'''
Created on Mar 21, 2021

@author: yann
'''

from random import randint
from time import sleep

from ..constants import (SCOLS, SROWS)
from .player import Player


class AI_level1(Player):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name + " (lvl 1)"

    def select(self, game, row, col):
        '''
        '''
        selected_piece = None

        if game.pick:
            #  At this point, we have to pick a piece from the storage board
            while True:
                rand_col = randint(0, SCOLS - 1)
                rand_row = randint(0, SROWS - 1)
                if game.storage_board.get_piece(rand_row, rand_col) != 0:
                    break

            game.selected_piece = game.storage_board.get_piece(rand_row, rand_col)
            game.valid_moves = game.game_board.get_valid_moves()
            selected_piece = (rand_col, rand_row)

        else:
            # And in this case we have to move the piece to the storage board
            rand_move = game.valid_moves[randint(0, len(game.valid_moves) - 1)]

            game.move(rand_move[0], rand_move[1])
            game.selected_piece = None
            game.valid_moves = []

        game.end_turn(selected_piece)
        sleep(1)

        return True


class AI_level2(Player):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name + " (lvl 2)"

    def select(self, game, row, col):
        '''
        '''
        pass


class AI_level3(Player):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name + " (lvl 3)"

    def select(self, game, row, col):
        '''
        '''
        pass
