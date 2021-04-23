'''
Created on Mar 21, 2021

@author: yann
'''

from random import randint
from time import sleep

from ..constants import (SCOLS, SROWS)
from .minimax import minimax, heuristic
from .player import Player
from .utils import get_not_losing_moves, get_winning_moves, get_coor_selected_piece


class AI_level1(Player):
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
        self.__name__ = name

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

            game.valid_moves = []

        game.end_turn(selected_piece)

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

    def __init__(self, name):
        '''
        Constructor
        '''
        self.__name__ = name
        self.depth = 2

        self.DEPTH_2_UNTIL = (2, 7)  # (depth, nb of turns left)
        self.DEPTH_3_UNTIL = (3, 4)  # (depth, nb of turns left)
        self.DEPTH_4_UNTIL = (4, 0)

        self.depths = [self.DEPTH_2_UNTIL,  # (depth, nb of turns left)]
                       self.DEPTH_3_UNTIL,
                       self.DEPTH_4_UNTIL]

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
            # game.selected_piece = game.storage_board.get_piece(move[0], move[1])
            game.valid_moves = game.game_board.get_valid_moves()
            game.end_turn(game.selected_piece)
            return True

        game_state = (game.game_board, game.storage_board, get_coor_selected_piece(game.storage_board, game.selected_piece))
        result = minimax(game_state, self.depth, True)

        if result[1]:  # if none, that means there is no piece left
            game.game_board, game.storage_board, selected_piece_coor = result[1]
            #  the position played and the picked piece are both returned at the same time
            print(game.game_board, game.storage_board, "\n", selected_piece_coor)

        game.end_turn(None)

        game.selected_piece = game.storage_board.get_piece(selected_piece_coor[0], selected_piece_coor[1])
        game.valid_moves = game.game_board.get_valid_moves()

        selected_piece = (selected_piece_coor[1], selected_piece_coor[0])
        game.end_turn(selected_piece)
        self.update_depth(game)

        return True

    def update_depth(self, game):
        nb_turns = len(game.game_board.get_valid_moves())

        print("nb_turns =", nb_turns)
        if nb_turns > self.DEPTH_2_UNTIL[1]:
            self.depth = self.DEPTH_2_UNTIL[0]
        elif nb_turns > self.DEPTH_3_UNTIL[1]:
            self.depth = self.DEPTH_3_UNTIL[0]
        elif nb_turns > self.DEPTH_4_UNTIL[1]:
            self.depth = self.DEPTH_4_UNTIL[0]
        print("depth =", self.depth)


class AI_level4(AI_level2):
    '''
    This AI uses the minmax algorithm but starts by using the AI_level2 algorithm
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        super().__init__(name)

        self.level2 = True
        self.depth = 2
        self.AI_LEVEL2_UNTIL = 10
        self.DEPTH_2_UNTIL = 5

    def select(self, game, row, col):
        self.update_depth(game)
        if self.level2:
            return AI_level2.select(self, game, row, col)
        else:
            return self.select_ai_level4(game, row, col)

    def select_ai_level4(self, game, row, col):
        '''
        This select method is a bit different from the past ones as we don't give control back to the game after the
        piece is placed, we don't the placing and the picking at once
        '''

        # FIXME: might not work
        # before picking the first piece
#         if len(game.game_board.get_valid_moves()) == SCOLS * SROWS and game.pick:
#             move = get_random_move(game)
#             print(move)
#             game.selected_piece = game.storage_board.get_piece(move[0], move[1])
#             game.valid_moves = game.game_board.get_valid_moves()
#             game.end_turn(game.selected_piece)
#             return True

        print("GAME SELECTED PIECE =", game.selected_piece)
        game_state = (game.game_board, game.storage_board, get_coor_selected_piece(game.storage_board, game.selected_piece))
        print("GAME SELECTED PIECE =", game.selected_piece)
        result = minimax(game_state, self.depth, True)

        if result[1]:  # if none, that means there is no piece left
            game.game_board, game.storage_board, selected_piece_coor = result[1]
            #  the position played and the picked piece are both returned at the same time
            print(game.game_board, game.storage_board, "\n", selected_piece_coor)

        game.end_turn(None)

        game.selected_piece = game.storage_board.get_piece(selected_piece_coor[0], selected_piece_coor[1])
        game.valid_moves = game.game_board.get_valid_moves()

        selected_piece = (selected_piece_coor[1], selected_piece_coor[0])
        game.end_turn(selected_piece)

        return True

    def update_depth(self, game):
        nb_turns = len(game.game_board.get_valid_moves())

        print("nb_turns =", nb_turns)
        if nb_turns < self.AI_LEVEL2_UNTIL:
            self.level2 = False
        elif nb_turns < self.DEPTH_2_UNTIL:
            self.depth = 3
        print("depth =", self.depth)
