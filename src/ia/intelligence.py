
from random import randint
from time import sleep

from quarto.game import Game
from quarto.constants import (SCOLS, SROWS)

class Intelligence:
    def select(self,Game):
        pass
    def put(self,Game):
        pass

class AI1:
    '''
    '''
    def select(self, game):
        '''
        '''
        if (self.player1 == 1 and self.turn) or (self.player2 == 1 and not self.turn):
                rand_col = randint(0, SCOLS - 1)
                rand_row = randint(0, SROWS - 1)

                if self.pick:
                    if self.storage_board.get_piece(rand_row, rand_col) != 0:
                        self.selected_piece = self.storage_board.get_piece(rand_row, rand_col)
                        self.valid_moves = self.game_board.get_valid_moves()
                        self.storage_board.selected_square = self.valid_moves[randint(0, len(self.valid_moves) - 1)]
                        self.change_turn()
                        self.change_pick_move()
                    else:
                        self.selected_piece = None

                else:
                    rand_valid_move = self.valid_moves[randint(0, len(self.valid_moves))]
                    sleep(1)
                    result = self._move(rand_valid_move[0], rand_valid_move[1])
                    self.selected_piece = None
                    self.valid_moves = []
                    self.storage_board.selected_square = None
                    self.change_turn()
                    self.change_pick_move()

    def put(self, game, piece):
        pass


