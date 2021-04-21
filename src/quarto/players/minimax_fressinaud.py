
# -*- coding: utf-8 -*-

import random

from models import Piece
import ui
from util import maximize_property, get_wining_properties, \
    get_board_values


class Intelligence:
    """
    Intelligence should be an abstract class.
    It designates, in fact, an artificial intelligence.
    The are different types of AI like Random, Novice or Minimax-D which
    heritated all of Intelligence
    """

    def selectPiece(self, match):
        pass

    def putOnBoard(self, match, piece):
        pass


class Minimax(Intelligence):
    """
    A Minimax intelligence implements Minimax algorithm
    with alpha-beta pruning. It must be the better player!
    """

    # MINIMAX_DEPTH_UNTIL = NUMBER OF PIECES AVAILABLE
    MINIMAX_1_UNTIL = 12
    MINIMAX_2_UNTIL = 10
    MINIMAX_3_UNTIL = 8

    # we can't search a depth further than that
    MAX_VAL_DEPTH = 4

    #  if we want to minimize or maximize
    STATE_MAX = 1
    STATE_MIN = 2

    # value of a win and value of a draw
    #  interestingly, a draw is not 0, which means he didn't implement this as a zero sum game per se
    EVAL_WIN = 500
    EVAL_DRAW = 490

    def __init__(self, depth):
        '''Constructor of the Minimax Intelligence
        Basically, the depth is set between 1 and MAX_VAL_DEPTH (=4)
        '''
        if depth < 1:
            depth = 1
        elif depth > Minimax.MAX_VAL_DEPTH:
            depth = Minimax.MAX_VAL_DEPTH

        self.max_depth = depth

    def evaluation(self, board, played_pos, state):
        '''The evaluation function is used to determine the value of a state.
        For example, a winning state (terminal state) will have the maximum evaluation
        A draw will have the second best evaluation
        And the eval_position function is called in order to compute the evaluation of the various other scenarios
        '''
        eval_pos = 0  #  the evaluation is set to 0

        if board.isWon():
            eval_pos = Minimax.EVAL_WIN
        elif board.isFull():
            eval_pos = Minimax.EVAL_DRAW
        else:
            eval_pos = min(
                Minimax.EVAL_WIN - 20, eval_position(board.board, played_pos)
                # the eval_position function is basically a heuristic function that computes a score based on the state
                # of the game. Ours will be way simpler but will still work
            )

        final_eval = eval_pos
        if state == Minimax.STATE_MAX:  # meaning, if we want to maximize the evaluation
            # the line below implies that the final_eval will be 0 if the current state is a winning state
            #  and that it will be superior if the current state is not a winning state
            final_eval = Minimax.EVAL_WIN - final_eval

        return final_eval

    def max_evaluation(self, board, played_piece, played_pos,
                       alpha, beta, depth):
        '''
        
        '''
        board.putPiece(played_piece, played_pos)

        available_pieces = board.unusedPieces()
        available_pos = board.unusedPositions()
        best_eval = 0  #  initializes the evaluation to 0

        # if win, draw, or max depth
        if board.isWon() or board.isFull() or depth >= self.max_depth:
            # we evaluate
            best_eval = self.evaluation(board, played_pos, Minimax.STATE_MAX)

        else:  #  that means we have to go deeper in the tree
            for piece in available_pieces:  #  for each available piece
                for pos in available_pos:  #  and for each available position
                    best_eval = max(#  the evaluation is equal to the maximum between
                        best_eval,  # the best evaluation (initialized at 0)
                        self.min_evaluation(#  and the evaluation of the deeper level
                            board, piece, pos,
                            alpha, beta, depth + 1  # depth is incremented, alpha and beta are for the pruning
                        )
                    )

                    if best_eval >= beta:
                        board.takeOff(played_piece)
                        return best_eval

                    alpha = max(alpha, best_eval)

        board.takeOff(played_piece)
        return best_eval

    def min_evaluation(self, board, played_piece, played_pos,
                       alpha, beta, depth):
        board.putPiece(played_piece, played_pos)

        available_pieces = board.unusedPieces()
        available_pos = board.unusedPositions()
        best_eval = Minimax.EVAL_WIN

        if board.isWon() or board.isFull() or depth >= self.max_depth:
            best_eval = self.evaluation(board, played_pos, Minimax.STATE_MIN)
        else:
            for piece in available_pieces:
                for pos in available_pos:
                    best_eval = min(
                        best_eval,
                        self.max_evaluation(
                            board, piece, pos,
                            alpha, beta, depth + 1
                        )
                    )

                    if alpha >= best_eval:
                        board.takeOff(played_piece)
                        return best_eval

                    beta = min(beta, best_eval)

        board.takeOff(played_piece)
        return best_eval

    def selectPiece(self, match):
        '''
        For us, the equivalent of this function is when it's time to pick
        '''
        available_pieces = match.board.unusedPieces()
        if len(available_pieces) < 1:
            # trick for tournament, when board is full
            return Piece({
                "color": "blue", "height": "small",
                "shape": "round", "state": "solid"
            })

        available_pos = match.board.unusedPositions()
        fallback_i = random.randint(0, len(available_pieces) - 1)
        chosen_piece = available_pieces[fallback_i]  #  init this with a real value to prevent bugs I guess
        alpha, beta = 0, Minimax.EVAL_WIN

        if len(available_pieces) >= Minimax.MINIMAX_1_UNTIL and \
                self.max_depth > 1:
            return Minimax(1).selectPiece(match)
        if len(available_pieces) >= Minimax.MINIMAX_2_UNTIL and \
                self.max_depth > 2:
            return Minimax(2).selectPiece(match)
        if len(available_pieces) >= Minimax.MINIMAX_3_UNTIL and \
                self.max_depth > 3:
            return Minimax(3).selectPiece(match)

        for piece in available_pieces:  #  for each available piece on the storage board
            alpha = 0  #  we instantiate alpha to 0

            for pos in available_pos:  #  for each possible move
                eval = self.min_evaluation(# we get the minimum evaluation
                    match.board, piece, pos,
                    alpha, beta, 1  #  the depth is one here
                )

                alpha = max(alpha, eval)

            if alpha < beta:
                beta = alpha
                chosen_piece = piece

        ui.showPlayer(match.active_player)
        ui.showSelectedPiece(chosen_piece)

        return chosen_piece

    def putOnBoard(self, match, piece):
        available_pos = match.board.unusedPositions()
        fallback_i = random.randint(0, len(available_pos) - 1)
        better_pos = available_pos[fallback_i]
        alpha, beta = 0, Minimax.EVAL_WIN

        if len(available_pos) >= Minimax.MINIMAX_1_UNTIL and \
                self.max_depth > 1:
            return Minimax(1).putOnBoard(match, piece)
        if len(available_pos) >= Minimax.MINIMAX_2_UNTIL and \
                self.max_depth > 2:
            return Minimax(2).putOnBoard(match, piece)
        if len(available_pos) >= Minimax.MINIMAX_3_UNTIL and \
                self.max_depth > 3:
            return Minimax(3).putOnBoard(match, piece)

        for pos in available_pos:
            eval = self.min_evaluation(
                match.board, piece, pos,
                alpha, beta, 1
            )

            if eval > alpha:
                alpha = eval
                better_pos = pos

        ui.showPlayer(match.active_player)
        ui.showSelectedPosition(better_pos)

        return better_pos


def eval_position(board, pos):
    eval_pos = 0

    piece = board[pos["x"]][pos["y"]]
    board[pos["x"]][pos["y"]] = None

    board_values = get_board_values(board)
    better_color = maximize_property(
        board,
        {"propriety": "color", "value": piece.color},
        board_values
    )
    better_height = maximize_property(
        board,
        {"propriety": "height", "value": piece.height},
        board_values
    )
    better_shape = maximize_property(
        board,
        {"propriety": "shape", "value": piece.shape},
        board_values
    )
    better_state = maximize_property(
        board,
        {"propriety": "state", "value": piece.state},
        board_values
    )

    if better_color["position"] == pos:
        eval_pos += 1
    if better_height["position"] == pos:
        eval_pos += 1
    if better_shape["position"] == pos:
        eval_pos += 1
    if better_state["position"] == pos:
        eval_pos += 1

    board[pos["x"]][pos["y"]] = piece

    winning_props = get_wining_properties(board)
    eval_pos += len(winning_props)

    if ("red" in winning_props and "blue" in winning_props) or \
            ("short" in winning_props and "tall" in winning_props) or \
            ("round" in winning_props and "square" in winning_props) or \
            ("solid" in winning_props and "hollow" in winning_props):
        # two different winning values for a same property,
        # it's like this board will be won on the next turn
        eval_pos = 0

    return eval_pos
