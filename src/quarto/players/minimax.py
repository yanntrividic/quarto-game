'''
Created on Apr 20, 2021

@author: yann
'''

from copy import deepcopy
from .player import Player


def minimax(game, depth: int, max_player: bool, playing_player: Player):
    '''
    Implementation of the minimax algorithm based on:
    https://github.com/techwithtim/Python-Checkers-AI/blob/master/minimax/algorithm.py

    game -- a Game object that contains the current state of the game (a storage board and a game board)
    depth -- int that represents the maximum depth we will explore
    max_player -- the player trying to maximize its evaluation, True if maximizing, False if minimizing
    playing_player -- the actual Player object for which we run the calculation
    '''

    if depth == 0 or game.winner() == playing_player:
        return

    if max_player:
        max_eval = float('-inf')
        best_move = None
        pass
