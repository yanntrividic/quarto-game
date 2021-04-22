'''
Created on Mar 21, 2021

@author: yann
'''

from random import randint
from time import sleep

from ..constants import (SCOLS, SROWS)
from .minimax import minimax, heuristic
from .player import Player
from .utils import get_not_losing_moves, get_winning_moves


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
                rand_row = randint(0, SROWS - 1)
                rand_col = randint(0, SCOLS - 1)
                if game.storage_board.get_piece(rand_row, rand_col) != 0:
                    break
            game.selected_piece = game.storage_board.get_piece(rand_row, rand_col)
            game.valid_moves = game.game_board.get_valid_moves()
            selected_piece = (rand_col, rand_row)

        else:
            # And in this case we have to move the piece to the game board
            rand_move = get_random_move(game)
            game.move(rand_move[0], rand_move[1])
            game.selected_piece = None
            game.valid_moves = []

        game.end_turn(selected_piece)
        sleep(1)

        return True


class AI_level2(Player):
    '''
    This AI uses a very naive algorithm that allows it to verify if the piece that was given to it can allow it to win,
    and which won't pick a piece if it allows the opponent to immediately win (unless there is no other choice).
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name + " (lvl 2)"

    def select(self, game, row, col):
        '''
        '''
        selected_piece = None
        winning_moves = []
        not_losing_moves = []

        if game.pick:
            #  At this point, we have to pick a piece from the storage board
            not_losing_moves = get_not_losing_moves(game)
            if not not_losing_moves:
                print("Oh no...")

            while True:
                rand_move = get_random_move(game) if not not_losing_moves else not_losing_moves[0]  # not random
                if game.storage_board.get_piece(rand_move[0], rand_move[1]) != 0:
                    break

            game.selected_piece = game.storage_board.get_piece(rand_move[0], rand_move[1])
            game.valid_moves = game.game_board.get_valid_moves()
            selected_piece = (rand_move[1], rand_move[0])

        else:
            # And in this case we have to move the piece to the game board
            winning_moves = get_winning_moves(game)

            if winning_moves:
                row, col = winning_moves[0]
                game.move(row, col)

            else:
                rand_move = get_random_move(game, True)
                game.move(rand_move[0], rand_move[1])

            game.selected_piece = None
            game.valid_moves = []

        game.end_turn(selected_piece)
        print("heuristic of the current state: " + str(heuristic(game)))
        sleep(1)

        return True


def get_random_move(game, verbose=False):
    '''Returns a random move
    '''
    if game.pick:
        move = game.storage_board.get_valid_moves()[randint(0, len(game.storage_board.get_valid_moves()) - 1)]
    else:
        move = game.valid_moves[randint(0, len(game.valid_moves) - 1)]
    if verbose:
        print(move)
    return move


class AI_level3(Player):
    '''
    This AI uses the minmax algorithm.
    '''

    def __init__(self, name, depth):
        '''
        Constructor
        '''
        self.__name__ = name + " (lvl 3)"
        self.depth = depth

    def select(self, game, row, col):
        '''
        This select method is a bit different from the past ones as we don't give control back to the game after the
        piece is placed, we don't the placing and the picking at once
        '''

        # FIXME: might not work
        # before picking the first piece
        if len(game.game_board.get_valid_moves()) == SCOLS * SROWS and game.pick:
            move = get_random_move(game)
            print(move)
            game.selected_piece = game.storage_board.get_piece(move[0], move[1])
            game.valid_moves = game.game_board.get_valid_moves()
            game.end_turn(game.selected_piece)
            return True

        result = minimax(game, self.depth, True, self)
        position_played, picked_piece = result[1]
        #  the position played and the picked piece are both returned at the same time

        print("position_played=", position_played, ", picked_piece=", picked_piece, ", final_eval=", result[0])

        print(game.game_board)
        game.move(position_played[0], position_played[1])

        game.selected_piece = None
        game.valid_moves = []
        game.end_turn(None)

        game.selected_piece = game.storage_board.get_piece(picked_piece[0], picked_piece[1])
        game.valid_moves = game.game_board.get_valid_moves()

        selected_piece = (picked_piece[1], picked_piece[0])
        game.end_turn(selected_piece)

        print("heuristic of the current state: " + str(heuristic(game)))
        sleep(1)

        return True
