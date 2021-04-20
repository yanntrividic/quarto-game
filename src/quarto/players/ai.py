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
    This AI uses the minmax algorithm.
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


def can_line_win(game, line):
    '''
    Checks if a line has the potential to win (if one of the available pieces can fill it to make it a winning line)
    
    game -- a Game object
    line -- a list of four (x, y) coordinates
    '''
    count, pos = count_zeros_in_line(game, line)
    if count == 1:  # meaning one piece is missing
        for row in game.storage_board.board:  # for each row in the storage board
            for piece in row:  # and each piece in each row
                # we check if this move would be winning

                col, row = pos
                inversed_pos = row, col  #  inversion of the order

                if piece != 0 and is_winning_move(game, inversed_pos, piece):  # pos might have to be inverted
                    # print("winning pos found =", pos)
                    return pos
    # if nothing was found, we return False
    return False


def count_zeros_in_line(game, line):
    count = 0
    pos = (-1, -1)
    for col, row in line:
        if game.game_board.board[row][col] == 0:
            count += 1
            pos = (col, row)
    return count, pos


def heuristic(game):
    '''
    Heuristic function for the level 3 and 4 AIs. The return values can range from 0 to 7 depending on the number
    of lines that result in a win if the right piece is put during the next turn.
    
    game -- a Game object at the current state of the game
    '''

    h = set()  # heuristics value

    # Rows and columns
    for col in range(GCOLS):
        row_line = []
        col_line = []

        for row in range(GROWS):
            col_line.append((col, row))
            row_line.append((row, col))

        h = __update_pos_set(game, row_line, h)
        h = __update_pos_set(game, col_line, h)

    #  Diagonals
    top_left_diagonal_line = []
    top_right_diagonal_line = []

    for col in range(GCOLS):  #  for diagonals
        top_left_diagonal_line.append((col, col))
        top_right_diagonal_line.append((GCOLS - col - 1, col))

    h = __update_pos_set(game, top_right_diagonal_line, h)
    h = __update_pos_set(game, top_left_diagonal_line, h)

    # print(h)
    return len(h)


def __update_pos_set(game, line, set):
    pos = can_line_win(game, line)  # false is no pos, the pos otherwise
    if pos:
        set.update({pos})  #  adds pos to the set, if it's already in there, nothing changes
    return set
