'''
Created on Apr 20, 2021

@author: yann
'''

from copy import deepcopy

from ..constants import GROWS, GCOLS
from ..game import TIE
from .utils import update_pos_set

EVAL_LOSS = -1
EVAL_TIE = 8  #  this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 9

MAX_DEPTH = 4


def minimax(game, depth: int, max_player: bool, move=None):
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
        return state_eval(game), move  # TODO: not sure about the heuristic is implemented in the correct way

    # TODO: we need to discriminate two cases : when we have to put a piece on the board, and when we have to pick a piece

    # When it's time to pick a piece, we have to (according to Marien Fressinaud):
    # 1) for each available pieces, maximize its position on the board
    # 2) minimize the evaluation (i.e. select the less dangerous piece)

    # When it's time to put a piece on the board, we must calculate what would maximize the heuristic and keep
    # the best one

    # FIXME: THE REST OF THIS FUNCTION IS NOT FINISHED AT ALL DONT OVERTHINK IT
    saved_game_board = game.game_board
    saved_storage_board = game.storage_board

    if max_player:  #  meaning we are trying to maximize the evaluation
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(game, False):  #  we get all the positions in which we can put the current piece
            print(move)
            for piece in get_all_moves(game, True):  # and then we get all the pickable pieces

                # TODO: we might have to store the original game&storage boards somewhere before doing that
                game.game_board, game.storage_board = simulate_move(game, move, piece)
                print("MAX simulated game_board:\n" + str(game.game_board))
                print("MAX simulated storage_board:\n" + str(game.storage_board))

                evaluation = minimax(game, depth - 1, False, (move, piece))[0]  # we get the evaluation at index 0
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    print("\t\tmax_evaluation ", evaluation)
                    best_move = (move, piece)  # we consider moves as a tuple

                game.game_board = saved_game_board
                game.storage_board = saved_storage_board

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(game, False):  #  we get all the positions in which we can put the current piece
            print(get_all_moves(game, False))
            for piece in get_all_moves(game, True):  # and then we get all the pickable pieces

                # TODO: we might have to store the original game&storage boards somewhere before doing that
                game.game_board, game.storage_board = simulate_move(game, move, piece)
                print("MIN simulated game_board:\n" + str(game.game_board))
                print("MIN simulated storage_board:\n" + str(game.storage_board))

                evaluation = minimax(game, depth - 1, True, (move, piece))[0]  # negamax with the - sign
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    print("\t\tmin_evaluation ", evaluation)
                    best_move = (move, piece)

                game.game_board = saved_game_board
                game.storage_board = saved_storage_board

        return min_eval, best_move


def state_eval(game):
    if game.winner() == TIE:
        return EVAL_TIE
    elif isinstance(game.winner(), str):
        return EVAL_WIN
    else:
        return heuristic(game)


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

        h = update_pos_set(game, row_line, h)
        h = update_pos_set(game, col_line, h)

    #  Diagonals
    top_left_diagonal_line = []
    top_right_diagonal_line = []

    for col in range(GCOLS):  #  for diagonals
        top_left_diagonal_line.append((col, col))
        top_right_diagonal_line.append((GCOLS - col - 1, col))

    h = update_pos_set(game, top_right_diagonal_line, h)
    h = update_pos_set(game, top_left_diagonal_line, h)

    # print(h)
    return len(h)


def get_all_moves(game, pick):
    #  TODO: verify if the return value is alright, I have a doubt
    if pick:
        coor_selected_piece_to_revove = get_coor_selected_piece(game)
        valid_moves = deepcopy(game.storage_board.get_valid_moves())

        print("piece to remove:", game.selected_piece, "coor_selected_piece_to_remove", coor_selected_piece_to_revove)
        if coor_selected_piece_to_revove:
            valid_moves.remove(coor_selected_piece_to_revove)

        print("valid_moves atfer removal:", valid_moves)

        return valid_moves  # all the moves possible
    else:
        print("get_all_moves game_board: ", game.game_board.get_valid_moves())
        return game.game_board.get_valid_moves()


def get_coor_selected_piece(game):
    for idx, row in enumerate(game.storage_board.board):
        try:
            return (idx, row.index(game.selected_piece))
        except ValueError:
            # this isn't in this row
            pass


def simulate_move(game, position_played, position_picked_piece):
    '''
    Function that simulates a move, i.e. that generates a new storage board and a new game board by taking the
    position_picked_piece from the game board and putting in the position_played.

    position_picked_piece -- a tuple of (x, y) coordinates tuple on the storage board
    game -- a Game object that will be updated with new boards
    position -- the position with which we need to deal in order to simulate the move
    '''

    # Where we do the picking
    picked_piece_row, picked_piece_col = position_picked_piece
    storage_board_copy = deepcopy(game.storage_board)

    picked_piece = storage_board_copy.board[picked_piece_row][picked_piece_col]
    storage_board_copy.board[picked_piece_row][picked_piece_col] = 0

    # Where we do the putting
    position_played_row, position_played_col = position_played
    game_board_copy = deepcopy(game.game_board)  #  we generate a copy of the game_board
    print(type(picked_piece), picked_piece)
    game_board_copy.put_piece(picked_piece, position_played_row, position_played_col)  #  and put the selected piece in the selected spot

    return game_board_copy, storage_board_copy
