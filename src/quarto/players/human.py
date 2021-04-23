'''
Created on Mar 21, 2021

@author: yann
'''

from .player import Player


class Human(Player):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name

    def select(self, game, row, col):
        '''
        '''
        selected_piece = None

        if game.pick:  # when it's time to pick a piece from the storage board.
            if game.storage_board.get_piece(row, col) != 0:
                game.selected_piece = game.storage_board.get_piece(row, col)
                print("HUMAN GAME SELECTED PIECE", game.selected_piece)
                game.valid_moves = game.game_board.get_valid_moves()
                selected_piece = (col, row)

        else:
            result = game.move(row, col)
            if not result:
                print("Invalid position, try again")
                return False

            game.selected_piece = None
            game.valid_moves = []

        game.end_turn(selected_piece)

        return True
