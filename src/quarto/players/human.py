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
        if game.pick:  # when it's time to pick a piece from the storage board.
            if game.storage_board.get_piece(row, col) != 0:
                game.selected_piece = game.storage_board.get_piece(row, col)
                game.valid_moves = game.game_board.get_valid_moves()
                game.storage_board.selected_square = (col, row)
                game.change_turn()
                game.change_pick_move()
            else:
                game.selected_piece = None

        else:
            result = game.move(row, col)
            if not result:
                print("Invalid position, try again")
                return False

            game.selected_piece = None
            game.valid_moves = []
            game.storage_board.selected_square = None
            game.change_turn()
            game.change_pick_move()

        return True
