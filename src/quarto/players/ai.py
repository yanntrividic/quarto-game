'''
Created on Mar 21, 2021

@author: yann
'''

from copy import deepcopy
from random import randint
from time import sleep

from ..constants import (SCOLS, SROWS, GCOLS, GROWS)
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


def get_winning_moves(game, piece=None):
    '''Returns a list of moves that can be done by the AI to win (used when it's time to move the piece)
    '''
    moves = []
    for move in game.game_board.get_valid_moves():  # we get all the valid moves
        if is_winning_move(game, move, game.selected_piece if not piece else piece):  # try all the valids moves
            # and if the move results in a win, we append it to the list
            moves.append(move)
    return moves


def is_winning_move(game, move, piece):
    '''Checks is a move is winning or not
    '''
    row, col = move

    game_board_copy = deepcopy(game.game_board)  #  we generate a copy of the game_board
    piece_copy = deepcopy(piece)

    game_board_copy.put_piece(piece_copy, row, col)  #  and put the selected piece in the selected spot
    return game_board_copy.winner()  #  and return the result


def get_not_losing_moves(game):
    ''' Returns a list of moves that won't make the other player win (used when it's time to pick)
    '''
    not_losing_moves = []
    valid_moves = game.storage_board.get_valid_moves()  # all the moves possible

    for move in valid_moves:  #  for each move
        game.selected_piece = game.storage_board.get_piece(move[0], move[1])  # we select the piece
        losing_moves = get_winning_moves(game)  # and check if the piece can result in a loss
        if not losing_moves:  # if it can't result in a loss
            not_losing_moves.append(move)  #  we add it to the possible plays

    return not_losing_moves


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
