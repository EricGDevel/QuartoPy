"""
Module minimax.py
=================

Contains all AI functions that allow the computer to make the best move.
Uses the minimax algorithm with alpha-beta pruning.
"""

__all__ = ['evaluate', 'has_won', 'minimax', 'pick_piece']
__version__ = '0.2'
__author__ = 'Eric G.D'

from copy import deepcopy
from math import inf
from typing import List, Set, Union

from src.constants import Player
from src.option import Option
from src.piece import *

MAX_SCORE = 10 ** 5


def has_won(board: List[List[Piece]]) -> bool:
    """
    :param board:   The current gamestate
    :return:        True if the board is full, false otherwise
    """
    return evaluate(board) == MAX_SCORE


def evaluate(board: List[List[Piece]]) -> float:
    """
    :param board:  The option to evaluate
    :return:        :board:'s ranking
    """
    ...


def pick_piece(cell_list: List[List[Cell]], pieces_set: Set[Piece], depth: int) -> Piece:
    """
    :param cell_list:   A 2D List containing the board's buttons
    :param pieces_set:  A set containing which pieces can be played
    :param depth:       The maximum recursion depth for the function
    :return:            Which piece the computer should play
    """
    ...


def minimax(board, piece: Piece, pieces_set: Set[Piece],
            depth: int, player: Player = Player.COMPUTER) -> Option:
    """
    :param board:           The board object
    :param piece:           The piece to use in the turn
    :param pieces_set:      A set of all piece that can be played
    :param depth:           The maximum recursion depth for the function
    :param player:          The player to play as
    :return:                The indexes of the best move for the computer (Maximising player)
    """
    board = board.convert()
    if depth <= 0:
        return pick_best(board, piece, pieces_set, player)
    alpha = -inf
    beta = inf
    return make_move(board, player, piece, pieces_set, alpha, beta, depth, depth)


def pick_best(board: List[List[Piece]], piece: Piece,
              pieces_set: Set[Piece], player: Player = Player.COMPUTER) -> Option:
    """
    :param board:       The current gamestate
    :param piece:       The piece to insert
    :param pieces_set:  A set of available pieces to play
    :param player:      The player to pick the best move for
    :return:            The move with the highest score
    """
    if not isinstance(player, Player) or not isinstance(piece, Piece) or not isinstance(pieces_set, set):
        raise TypeError("One of the paramters is an invalid type!")
    options = get_options(board, piece, pieces_set)
    scores = [evaluate(option.game_state) for option in options]
    best_score = max(scores) if player == Player.COMPUTER else min(scores)
    return options[scores.index(best_score)]


def get_options(board: List[List[Piece]], piece: Piece, pieces_set: Set[Piece]) -> List[Option]:
    """
    :param board:               The current gamestate
    :param piece:               The piece to insert
    :param pieces_set:          A set containing all playable moves
    :return:                    A list of all possible moves
    """
    if not isinstance(piece, Piece) or not isinstance(pieces_set, set):
        raise TypeError(":piece: needs to be a Piece object and :pieces_set: needs to be a set!")
    if piece not in pieces_set:
        raise ValueError(":piece: has to be in :pieces_set:!")
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                option = deepcopy(board)
                option[i][j] = piece
                # TODO: Optimise this section using pick_best instead of iteration over all possible pieces
                for next_piece in pieces_set:
                    if next_piece is piece:
                        continue
                    out.append(Option(option, (i, j), next_piece))
    return out


def make_move(board: List[List[Piece]], player: Player, piece: Piece, pieces_set: Set[Piece],
              alpha: float, beta: float, depth: int, idepth: int) -> Union[float, Option]:
    """
    :param board:       The current gamestate
    :param player:      The player to play as
    :param piece:       The piece to use in the turn
    :param pieces_set:  A set of all piece that can be played
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param depth:       How many moves the computer can look ahead
    :param idepth:      The initial depth value
    :return:            The best score/index of the best move for :player: and the piece to play
    """
    val = evaluate(board)
    if abs(val) == MAX_SCORE:
        return val * (depth + 1)
    if depth == 0 or len(pieces_set) == 0:
        return val
    options = get_options(board, piece, pieces_set)
    rival = Player.HUMAN if player == Player.COMPUTER else Player.COMPUTER
    new_set = deepcopy(pieces_set)
    new_set.remove(piece)
    best_option = options[0]
    best_score = make_move(options[0].game_state, rival, options[0].piece, new_set, alpha, beta, depth - 1, idepth)
    for option in options[1:]:
        score = make_move(option.game_state, rival, option.piece, new_set, alpha, beta, depth - 1, idepth)
        if better_move(player, score, best_score):
            best_option = option
            best_score = score
        if alpha < best_score and player == Player.COMPUTER:
            alpha = best_score
        elif beta > best_score and player == Player.HUMAN:
            beta = best_score
        if beta <= alpha:
            break
    best_score = -best_score if player == Player.HUMAN else best_score
    return best_score if depth != idepth else best_option


def better_move(player: Player, score: float, best_score: float) -> bool:
    """
    :param player:      Tells the computer if looking for min or max scores (str, Player.HUMAN/Player.COMPUTER)
    :param score:       The new score
    :param best_score:  The previous best score
    :return:            If :score: is better than :best_score:
    """
    return (score > best_score) if player == Player.COMPUTER else (score < best_score)
