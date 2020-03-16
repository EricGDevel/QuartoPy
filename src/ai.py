"""
Module ai.py
=================

Contains all AI functions that allow the computer to make the best move.
Uses the minimax algorithm with alpha-beta pruning.
"""

__all__ = ['evaluate', 'has_won', 'make_move', 'pick_best', 'pick_starting_piece']
__version__ = '1.1'
__author__ = 'Eric G.D'

import random
from copy import deepcopy
from math import inf
from typing import List, Set, Tuple, Union

import numpy as np

from src.constants import MAX_SCORE
from src.option import Option
from src.piece import Piece


# TODO: Get rid of similar starting moves


def has_won(board: List[List[Piece]]) -> bool:
    """
    :param board:   The current gamestate
    :return:        True if the board is full, false otherwise
    """
    return evaluate(board)[0] == MAX_SCORE


def evaluate(board: List[List[Piece]]) -> Tuple[int, List[int]]:
    """
    :param board:       The gamestate to evaluate
    :return:            :board:'s static evaluation and what attributes the next piece needs to have in order to win
    """
    length = len(board)
    rows = get_rows_from_board(board)
    row_scores = []
    winning_attributes = [-1] * length
    for row in rows:
        attributes, num_of_pieces = calculate_row_attributes(row)
        attributes_num = length - attributes.count(-1) if num_of_pieces > 1 else num_of_pieces
        if attributes_num == 0:
            continue
        if num_of_pieces == length:
            row_scores = [MAX_SCORE]
            break
        elif num_of_pieces == length - 1:
            next_move_wins = update_winning_attributes(winning_attributes, attributes)
            if next_move_wins:
                row_scores.append(-MAX_SCORE // 2)
                continue
        row_scores.append((2 ** num_of_pieces) * attributes_num)  # Multiple shared att's count as multiple rows
    score = sum(row_scores)  # TODO: Make score more accurate
    return score, winning_attributes


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
            attributes = [attributes[i] if attributes[i] == piece.attributes[i] else -1 for i in range(len(attributes))]
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
              pieces_set: Set[Piece]) -> Option:
    """
    :param board:       The current gamestate
    :param piece:       The piece to insert
    :param pieces_set:  A set of available pieces to play
    :return:            The move with the highest score
    """
    options = get_options(board, piece, pieces_set)
    scores = [evaluate(option.game_state)[0] for option in options]
    best_score = max(scores)
    return options[scores.index(best_score)]


def get_options(board: List[List[Piece]], piece: Piece, pieces_set: Set[Piece]) -> List[Option]:
    """
    :param board:               The current gamestate
    :param piece:               The piece to insert
    :param pieces_set:          A set containing all playable moves
    :return:                    A list of all possible moves
    """
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                option = deepcopy(board)
                option[i][j] = piece
                if contains_symmetries(out, option):
                    continue
                out.append(get_playable_moves(option, pieces_set, i, j))
    out.sort(key=lambda x: x[1])  # Sort moves by base score
    out = [x for option_list in out for x in option_list[0]]  # Convert 2D list to 1D list
    return out


def contains_symmetries(options: List[Tuple[List[Option], int]], option: List[List[Piece]]) -> bool:
    """
    :param options:     The current list of potential moves
    :param option:      The option to be added
    :return:            If options already contains an gamestate that is a transformation of option
    """
    for tuple_ in options:
        game_state = tuple_[0][0].game_state  # All options in current list have same game_state
        flips = [np.flip(option, i) for i in range(2)]
        rotations = [np.rot90(option, i) for i in range(1, 4)]
        rotated_flips = [np.rot90(flip, i) for flip in flips for i in range(1, 4)]
        transformations = rotations + flips + rotated_flips
        if any(np.array_equal(transformation, game_state) for transformation in transformations):
            return True
    return False


def get_playable_moves(option: List[List[Piece]], pieces_set: Set[Piece], i: int, j: int) -> Tuple[List[Option], int]:
    """
    Checks what pieces can be given to the next player without them winning
    :param option:      The option's gamestate
    :param pieces_set:  A set of all playable pieces
    :param i:           First index of inserted piece
    :param j:           Second index of inserted piece
    :return:            A list of all playable moves with :option: as its gamestate
    """
    score, blacklist = evaluate(option)
    options = []
    if -2 not in blacklist:
        for next_piece in pieces_set:
            if not any(p_att == bl_att for p_att, bl_att in zip(next_piece.attributes, blacklist)):
                options.append(Option(option, i, j, next_piece))
    if not options:
        options.append(Option(option, i, j, tuple(pieces_set)[0]))
    return options, score


def make_move(board: List[List[Piece]], piece: Piece, pieces_set: Set[Piece], sign: int, alpha: float, beta: float,
              depth: int, get_move: bool) -> Union[int, Option]:
    """
    :param board:       The current gamestate
    :param piece:       The piece to use in the turn
    :param pieces_set:  A set of all piece that can be played
    :param sign:        The sign of the player (+1 for computer, -1 for human)
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param depth:       How many moves the computer can look ahead
    :param get_move:    Whether to return the best option or the score of the best option
    :return:            The best score/index of the best move for :player: and the piece to play
    """
    val = evaluate(board)[0]
    if abs(val) == MAX_SCORE or depth == 0:
        return sign * val * (depth + 1)
    if len(pieces_set) == 0:
        return sign * val
    options = get_options(board, piece, pieces_set)
    best_option, best_score = None, -inf
    for option in options:
        pieces_set.remove(option.piece)
        score = -make_move(option.game_state, option.piece, pieces_set, -sign, -beta, -alpha, depth - 1, False)
        pieces_set.add(option.piece)
        if score > best_score:
            best_option = option
            best_score = score
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break
    return best_option if get_move else best_score
