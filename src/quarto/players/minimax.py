'''
Created on Apr 20, 2021

@author: yann
'''

from copy import deepcopy
from .player import Player

EVAL_LOSS = -1
EVAL_DRAW = 8  #  this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 9

MAX_DEPTH = 4


def minimax(game, depth: int, max_player: bool, playing_player: Player):
    '''
    Implementation of the minimax algorithm based on:
     * https://github.com/techwithtim/Python-Checkers-AI/blob/master/minimax/algorithm.py
     * https://github.com/marienfressinaud/AI_quarto

    position -- a (x, y) coordinates to evaluate
    game -- a Game object that contains the current state of the game (a storage board and a game board)
    depth -- int that represents the maximum depth we will explore
    max_player -- the player trying to maximize its evaluation, True if maximizing, False if minimizing
    playing_player -- the actual Player object for which we run the calculation

    returns --
    A move, i.e. a tuple of (x, y) coordinates.
    If pick: the move is the cell from the storage board in which the piece to select is.
    If not pick: the move is the cell from the game board in which to put the selected piece in.
    '''

    # Terminal state or max depth reached
    if depth == 0 or game.winner():
        return game  #  FIXME: return eval value

    # TODO: we need to discriminate two cases : when we have to put a piece on the board, and when we have to pick a piece

    # When it's time to pick a piece, we have to (according to Marien Fressinaud):
    # 1) for each available pieces, maximize its position on the board
    # 2) minimize the evaluation (i.e. select the less dangerous piece)

    # When it's time to put a piece on the board, we must calculate what would maximize the heuristic and keep
    # the best one

    # FIXME: THE REST OF THIS FUNCTION IS NOT FINISHED AT ALL DONT OVERTHINK IT
    if max_player:  #  meaning we are trying to maximize the evaluation
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(game, False):  #  we get all the positions in which we can put the current piece
            for piece in get_all_moves(game, True):  # and then we get all the pickable pieces

                # TODO: we might have to store the original game&storage boards somewhere before doing that
                game.game_board, game.storage_board = simulate_move(game, move, piece)

                evaluation = minimax(move, game, depth - 1, False, playing_player, False)[0]
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_move = move

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(game, True):
            evaluation = minimax(move, game, depth - 1, True, playing_player, False)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def get_all_moves(game, pick):
    #  TODO: verify if the return value is alright, I have a doubt
    if pick:
        return game.storage_board.get_valid_moves()  # all the moves possible
    else:
        return game.game_board.get_valid_moves()


def simulate_move(game, position_played, picked_piece):
    '''
    Function that simulates a move, i.e. that generates a new storage board and a new game board by taking the
    picked_piece from the game board and putting in the position_played.

    picked_piece -- a tuple of (x, y) coordinates tuple on the storage board
    game -- a Game object that will be updated with new boards
    position -- the position with which we need to deal in order to simulate the move
    '''

    # Where we do the picking
    picked_piece_row, picked_piece_col = picked_piece
    storage_board_copy = deepcopy(game.storage_board)
    game.selected_piece = storage_board_copy.board[picked_piece_row][picked_piece_col]
    storage_board_copy.board[picked_piece_row][picked_piece_col] = 0

    # Where we do the putting
    position_played_row, position_played_col = position_played
    game_board_copy = deepcopy(game.game_board)  #  we generate a copy of the game_board
    piece_copy = deepcopy(game.storage_board.board[position_played_row][position_played_col])
    game_board_copy.put_piece(piece_copy, position_played_row, position_played_col)  #  and put the selected piece in the selected spot

    return game_board_copy, storage_board_copy
