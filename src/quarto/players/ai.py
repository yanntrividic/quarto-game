'''
Created on Mar 21, 2021

@author: yann
'''

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
            # And in this case we have to move the piece to the storage board
            rand_move = game.valid_moves[randint(0, len(game.valid_moves) - 1)]

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
        wining_moves = []
        not_losing_moves = []

        if game.pick:
            #  At this point, we have to pick a piece from the storage board
            not_losing_moves = self.notLosingMoves(game)
            rand_move = game.storage_board.get_valid_moves()[0]
            if not(len(not_losing_moves) == 0):
                while True:
                    rand_index = randint(0, len(not_losing_moves) - 1)
                    rand_move = not_losing_moves[rand_index]
                    if game.storage_board.get_piece(rand_move[0], rand_move[1]) != 0:
                        break
            game.selected_piece = game.storage_board.get_piece(rand_move[0], rand_move[1])
            game.valid_moves = game.game_board.get_valid_moves()
            selected_piece = (rand_move[1], rand_move[0])

        else:
            # And in this case we have to move the piece to the storage board
            wining_moves = self.winingMoves(game)
            if len(wining_moves) != 0:
                row, col = wining_moves[0]
                game.move(row, col)
            else:
                rand_move = game.valid_moves[randint(0, len(game.valid_moves) - 1)]
                game.move(rand_move[0], rand_move[1])

            game.selected_piece = None
            game.valid_moves = []

        game.end_turn(selected_piece)
        sleep(1)

        return True

    def winingMoves(self, game, piece=None):
        '''
        '''
        moves = []
        for move in game.valid_moves:
            if self.isWiningMove(game, move, piece):  # try all the valids moves
                moves.append(move)
        return moves

    def isWiningMove(self, game, move, piece):
        row, col = move

        if row is col :  # check the diagonal top-left -> buttom-right
            pieces = []
            for i in range(GCOLS):
                pieces.append(game.game_board.board[i][i])
            if self.checkLine(game, pieces, piece):
                return True

        if row == (GCOLS - col - 1) : #check the diagonal bottom-left -> to-right
            pieces = []
            for i in range (GCOLS):
                pieces.append(game.game_board.board[GROWS - i - 1][i])
            if self.checkLine(game, pieces, piece):
                return True

        if self.checkLine(game, game.game_board.board[row], piece):  # check the row
            return True

        pieces = []  # check the col
        for i in range(GROWS):
            pieces.append(game.game_board.board[i][col])
        if self.checkLine(game, pieces, piece):
            return True

        return False

    def checkLine(self, game, line, p):
        if self.zeroCount(line) == 1:
            pieces = []
            if p is None:
                pieces.append(game.selected_piece)
            else:
                pieces.append(p)
            for piece in line:
                if piece != 0:
                    pieces.append(piece)
            return game.game_board._Board__is_winning_line(pieces)
        return False

    def zeroCount(self, pieces):
        r = 0
        for p in pieces:
            if p == 0:
                r += 1
        return r

    def notLosingMoves(self, game):
        moves = []
        losing_moves = []
        valid_moves = game.storage_board.get_valid_moves()
        for move in valid_moves:
            losing_moves = self.winingMoves(game, game.storage_board.get_piece(move[0], move[1]))
            if len(losing_moves) == 0:
                moves.append(move)
        return moves


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


