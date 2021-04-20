'''
Created on Apr 20, 2021

@author: yann
'''

from copy import deepcopy
from .player import Player


def minimax(game, depth: int, max_player: bool, playing_player: Player, pick: bool):
    '''
    Implementation of the minimax algorithm based on:
    https://github.com/techwithtim/Python-Checkers-AI/blob/master/minimax/algorithm.py

    game -- a Game object that contains the current state of the game (a storage board and a game board)
    depth -- int that represents the maximum depth we will explore
    max_player -- the player trying to maximize its evaluation, True if maximizing, False if minimizing
    playing_player -- the actual Player object for which we run the calculation
    pick -- bool, True when it's time to pick a piece, False when it's time to place a piece
    '''

    if depth == 0 or game.winner() == playing_player:
        return

    # TODO: we need to discriminate two cases : when we have to put a piece on the board, and when we have to pick a piece

    if pick:
        # When it's time to pick a piece, we have to (according to Marien Fressinaud):
        # 1) for each available pieces, maximize its position on the board
        # 2) minize the evaluation (i.e. select the less dangerous piece)

        if max_player:
            max_eval = float('-inf')
            best_move = None
            pass

    else:
        # When it's time to put a piece on the board, we must calculate what would maximize the heuristic and keep
        # the best one
        pass
