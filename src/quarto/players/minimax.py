'''
Created on Apr 20, 2021

@author: yann
'''

from copy import deepcopy

from ..constants import GROWS, GCOLS
from .utils import update_pos_set, get_coor_selected_piece

EVAL_LOSS = -1
EVAL_TIE = 8  #  this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 9

MAX_DEPTH = 4


def minimax(game_state, depth: int, max_player: bool, verbose=False):
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

    if verbose:
        print("\n\n", "\t" * abs(2 - depth), "ENTERING MINIMAX DEPTH", depth, "MAX =", max_player)
        print("\t" * abs(2 - depth), "Game State:")
        print(game_state[0].display(depth))
        print(game_state[1].display(depth))
        print("\t" * abs(2 - depth), "Selected_piece:" + str(game_state[2]))

    # Terminal state or max depth reached
    if depth == 0 or game_state[0].winner():
        if verbose:
            print("\t" * abs(2 - depth), "State_eval:", state_eval(game_state), "\n\n")
        return state_eval(game_state), game_state  # * (-1 if max_player else 1) ??, move

    if max_player:  #  meaning we are trying to maximize the evaluation
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(game_state):  #  we get all the positions in which we can put the current piece
            # TODO: we might have to store the original game&storage boards somewhere before doing that

            evaluation = minimax(move, depth - 1, False)[0]  # we get the evaluation at index 0
            max_eval = max(max_eval, evaluation)
            if verbose:
                print("\t" * abs(2 - depth), "evaluation ", evaluation)
            if max_eval == evaluation:
                if verbose:
                    print("\t" * abs(2 - depth), "max_evaluation updated:", max_eval)
                best_move = move  # we consider moves as a tuple

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(game_state):  #  we get all the positions in which we can put the current piece
            # TODO: we might have to store the original game&storage boards somewhere before doing that

            evaluation = -minimax(move, depth - 1, True)[0]  # we get the evaluation at index 0
            min_eval = min(min_eval, evaluation)
            if verbose:
                print("\t" * abs(2 - depth), "evaluation ", evaluation)
            if min_eval == evaluation:
                if verbose:
                    print("\t" * abs(2 - depth), "min_evaluation updated:", min_eval)
                best_move = move  # we consider moves as a tuple

        return min_eval, best_move


def state_eval(game_state):
    if game_state[0].winner():
        return EVAL_WIN
    elif game_state[0].is_full():
        return EVAL_TIE
    else:
        return heuristic(game_state)


def heuristic(game_state):
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

        h = update_pos_set(game_state[0], row_line, h, game_state[1])
        h = update_pos_set(game_state[0], col_line, h, game_state[1])

    #  Diagonals
    top_left_diagonal_line = []
    top_right_diagonal_line = []

    for col in range(GCOLS):  #  for diagonals
        top_left_diagonal_line.append((col, col))
        top_right_diagonal_line.append((GCOLS - col - 1, col))

    h = update_pos_set(game_state[0], top_right_diagonal_line, h, game_state[1])
    h = update_pos_set(game_state[0], top_left_diagonal_line, h, game_state[1])

    # print(h)
    return len(h)


def get_all_submoves(game_state, pick):
    #  TODO: verify if the return value is alright, I have a doubt
    if pick:
        valid_moves = game_state[1].get_valid_moves()

        # print("piece to remove:", game.selected_piece, "coor_selected_piece_to_remove", coor_selected_piece_to_revove)
       # print("REMOVED PIECE: ", game_state[2])
        valid_moves.remove(game_state[2])

        # print("valid_moves atfer removal:", valid_moves)

        return valid_moves  # all the moves possible
    else:
        # print("get_all_moves game_board: ", game.game_board.get_valid_moves())
        return game_state[0].get_valid_moves()


def get_all_moves(game_state):
    moves = []

    # print("get_all_submoves position:", get_all_submoves(game_state, False))
    #  print("get_all_submoves piece:", get_all_submoves(game_state, True))
    for position_played in get_all_submoves(game_state, False):
        for piece_picked in get_all_submoves(game_state, True):
            temp_game_state = deepcopy(game_state)
            new_game_state = simulate_move(temp_game_state, position_played, piece_picked)
            moves.append(new_game_state)

    return moves


def simulate_move(game_state, position_played, piece_picked):
    '''
    Function that simulates a move, i.e. that generates a new storage board and a new game board by taking the
    position_picked_piece from the game board and putting in the position_played.

    position_picked_piece -- a tuple of (x, y) coordinates tuple on the storage board
    game -- a Game object that will be updated with new boards
    position -- the position with which we need to deal in order to simulate the move
    '''
    game_board, game_storage, selected_piece_coor = game_state
    selected_piece = game_storage.board[selected_piece_coor[0]][selected_piece_coor[1]]
    game_storage.board[selected_piece_coor[0]][selected_piece_coor[1]] = 0
    game_board.put_piece(selected_piece, position_played[0], position_played[1])

    return game_state[0], game_state[1], piece_picked
