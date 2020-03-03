"""
Module ai.py
=================

Contains all AI functions that allow the computer to make the best move.
Uses the minimax algorithm with alpha-beta pruning.
"""

__all__ = ['evaluate', 'has_won', 'make_move', 'pick_best', 'pick_starting_piece']
__version__ = '1.0'
__author__ = 'Eric G.D'

import random
from copy import deepcopy
from math import inf
from typing import List, Set, Tuple, Union

from src.option import Option
from src.piece import *

MAX_SCORE = 10 ** 5


# TODO: Get rid of similar starting moves


def has_won(board: List[List[Piece]]) -> bool:
    """
    :param board:   The current gamestate
    :return:        True if the board is full, false otherwise
    """
    return evaluate(board)[0] == MAX_SCORE


def evaluate(board: List[List[Piece]], max_player: bool = True) -> Tuple[int, List[int]]:
    """
    :param board:       The gamestate to evaluate
    :param max_player:  If the current player is maximising or minimising
    :return:            :board:'s static evaluation and what attributes the next piece needs to have in order to win
    """
    length = len(board)
    rows = get_rows_from_board(board)
    row_scores = []
    winning_attributes = [-1] * 4
    for row in rows:
        attributes, num_of_pieces = calculate_row_attributes(row)
        attributes_num = len(attributes) - attributes.count(-1) if num_of_pieces > 1 else num_of_pieces
        if attributes_num > 0:
            if num_of_pieces == length:
                row_scores = [MAX_SCORE]
                break
            elif num_of_pieces == length - 1:
                next_move_wins = update_winning_attributes(winning_attributes, attributes)
                if next_move_wins:
                    row_scores.append(-(MAX_SCORE // 2))
                    continue
            row_scores.append((2 ** num_of_pieces) * attributes_num)  # Multiple shared att's count as multiple rows
    score = sum(row_scores)  # TODO: Make score more accurate
    return score if max_player else -score, winning_attributes


def get_rows_from_board(board: List[List[Piece]]) -> List[List[Piece]]:
    """
    :param board:   The current gamestate that is being evaluated
    :return:        A list of all the rows in the board
    """
    length = len(board)
    rows = [[] for _ in range(length)]
    cols = [[] for _ in range(length)]
    diagonals = [[] for _ in range(2)]
    for i in range(length):
        assert len(board[i]) == length
        for j in range(length):
            piece = board[i][j]
            rows[i].append(piece)
            cols[j].append(piece)
            if i == j:
                diagonals[0].append(piece)
            if i == length - j - 1:
                diagonals[1].append(piece)
    return rows + cols + diagonals


def calculate_row_attributes(row: List[Piece]) -> Tuple[List[Union[bool, int]], int]:
    """
    :param row:     A row in the board
    :return:        A tuple containing the shared attributes and the number of pieces
    """
    attributes, num_of_pieces = [], 0
    for piece in row:
        if piece is None:
            continue
        if num_of_pieces == 0:
            attributes = [x for x in piece.attributes]
        else:
            attributes = [attributes[i] if attributes[i] == piece.attributes[i] else -1
                          for i in range(len(attributes))]
        num_of_pieces += 1
    return attributes, num_of_pieces


def update_winning_attributes(winning_attributes: List[Union[bool, int]],
                              attributes: List[Union[bool, int]]) -> bool:
    """
    :param winning_attributes:  The shared attributes of previous 3-in-a-rpw rows
    :param attributes:          The attributes of the current 3-in-a-row row
    :return:                    If the next player has a guaranteed win the next turn
    """
    assert len(winning_attributes) == len(attributes)
    next_move_wins = False
    for i in range(len(winning_attributes)):
        if winning_attributes[i] == -1:
            winning_attributes[i] = attributes[i]
        elif attributes[i] != -1 and attributes[i] != winning_attributes[i]:
            winning_attributes[i] = -2
            next_move_wins = True
    return next_move_wins


def pick_starting_piece(pieces_set: Set[Piece]) -> Piece:
    """
    :param pieces_set:  A set containing which pieces can be played
    :return:            Which piece the computer should give the player
    """
    return random.choice(tuple(pieces_set))


def pick_best(board: List[List[Piece]], piece: Piece,
              pieces_set: Set[Piece], max_player: bool = True) -> Option:
    """
    :param board:       The current gamestate
    :param piece:       The piece to insert
    :param pieces_set:  A set of available pieces to play
    :param max_player:      The player to pick the best move for
    :return:            The move with the highest score
    """
    if not isinstance(max_player, bool) or not isinstance(piece, Piece) or not isinstance(pieces_set, set):
        raise TypeError("One of the parameters is an invalid type!")
    options = get_options(board, piece, pieces_set)
    scores = [evaluate(option.game_state, max_player)[0] for option in options]
    best_score = max(scores) if max_player else min(scores)
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
    if piece in pieces_set:
        raise ValueError(":piece: should not be in :pieces_set:!")
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                option = deepcopy(board)
                option[i][j] = piece
                score, blacklist = evaluate(option)
                options = []
                for next_piece in pieces_set:
                    if -2 in blacklist:
                        break
                    if not any([p_att == bl_att for p_att, bl_att in zip(next_piece.attributes, blacklist)]):
                        options.append(Option(option, (i, j), next_piece))
                if not options:
                    options.append(Option(option, (i, j), list(pieces_set)[0]))
                out.append((options, score))
    out.sort(key=lambda x: x[1])
    out = [x for option_list in out for x in option_list[0]]  # Convert 2D list to 1D list
    return out


def make_move(board: List[List[Piece]], max_player: bool, piece: Piece, pieces_set: Set[Piece],
              alpha: float, beta: float, depth: int, idepth: int) -> Union[int, Option]:
    """
    :param board:       The current gamestate
    :param max_player:  Which player the function should play as
    :param piece:       The piece to use in the turn
    :param pieces_set:  A set of all piece that can be played
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param depth:       How many moves the computer can look ahead
    :param idepth:      The initial depth value
    :return:            The best score/index of the best move for :player: and the piece to play
    """
    val = evaluate(board, max_player)[0]
    if abs(val) == MAX_SCORE:
        return -val * (depth + 1)
    if depth == 0 or len(pieces_set) == 0:
        return -val
    options = get_options(board, piece, pieces_set)
    options = reversed(options) if not max_player else options
    rival = not max_player
    best_option, best_score = None, -inf if max_player else inf
    for option in options:
        pieces_set.remove(option.piece)
        score = make_move(option.game_state, rival, option.piece, pieces_set, alpha, beta, depth - 1, idepth)
        pieces_set.add(option.piece)
        if better_score(max_player, score, best_score):
            best_option = option
            best_score = score
        alpha = max(alpha, best_score) if max_player else alpha
        beta = min(beta, best_score) if not max_player else beta
        if beta <= alpha:
            break
    return best_score if depth != idepth else best_option


def better_score(max_player: bool, score: int, best_score: int) -> bool:
    """
    :param max_player: If the current player is the maximising player
    :param score:       The score of the current move
    :param best_score:  The score of the current best move
    :return:            The if the current move is better then the previous best
    """
    return score > best_score if max_player else score < best_score
