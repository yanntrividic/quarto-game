'''
Created on Apr 22, 2021

@author: yann
'''

from copy import deepcopy
from ..board import Board


def can_line_win(game, line, sboard=None):
    '''
    Checks if a line has the potential to win (if one of the available pieces can fill it to make it a winning line)

    game -- a Game object
    line -- a list of four (x, y) coordinates
    '''
    count, pos = count_zeros_in_line(game, line)
    if count == 1:  # meaning one piece is missing
        storage = sboard.board if sboard else game.storage_board.board

        for row in storage:  # for each row in the storage board
            for piece in row:  # and each piece in each rowhttps://github.com/marienfressinaud/AI_quarto
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

    if isinstance(game, Board):
        game = game.board
    else:
        game = game.game_board.board

    for col, row in line:
        if game[row][col] == 0:
            count += 1
            pos = (col, row)
    return count, pos


def update_pos_set(game, line, set, sboard=None):
    pos = can_line_win(game, line, sboard)  # false is no pos, the pos otherwise
    if pos:
        set.update({pos})  #  adds pos to the set, if it's already in there, nothing changes
    return set


def get_coor_selected_piece(storage_board, selected_piece):
    for i, row in enumerate(storage_board.board):
        for j, col in enumerate(row):
            if col == selected_piece:
                return (i, j)


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

    if isinstance(game, Board):
        game_board_copy = deepcopy(game)  #  we generate a copy of the game_board
    else:
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
