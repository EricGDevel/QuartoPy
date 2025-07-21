"""
Module ai.py
=================

Contains all AI functions that allow the computer to make the best move.
Uses the NegaMax algorithm with alpha-beta pruning, symmetry detection and a transposition table.
"""

from __future__ import annotations

__all__ = [
    "evaluate",
    "has_won",
    "iterative_deepening",
    "pick_best",
    "pick_starting_piece",
]
__version__ = "1.3"
__author__ = "Eric G.D"

from copy import deepcopy
from math import inf
import random
from time import time

import numpy as np

from src.constants import BOTH_ATTRIBUTES, MAX_SCORE, MAX_TIME, NO_ATTRIBUTES
from src.option import (
    GameState,
    Option,
    Transposition,
    TTFlag,
)
from src.piece import Piece


def has_won(state: GameState) -> bool:
    """
    :param state:   The current GameState
    :return:        True if the board is full, false otherwise
    """
    return evaluate(state)[0] == MAX_SCORE


def evaluate(state: GameState) -> tuple[int, list[int]]:
    """
    :param state:       The GameState to evaluate
    :return:            :board:'s static evaluation and what attributes the next piece needs to have in order to win
    """
    length = len(state)
    assert length == Piece.NUM_OF_ATTRIBUTES
    rows = get_rows_from_board(state)
    row_scores = []
    winning_attributes = [NO_ATTRIBUTES] * Piece.NUM_OF_ATTRIBUTES
    for row in rows:
        attributes, num_of_pieces = calculate_row_attributes(row)
        attributes_num = (
            length - attributes.count(NO_ATTRIBUTES) if num_of_pieces > 1 else 0
        )
        if attributes_num == 0:
            continue
        if num_of_pieces == length:
            row_scores[:] = [MAX_SCORE]
            break
        if num_of_pieces == length - 1:
            next_move_wins = update_winning_attributes(winning_attributes, attributes)
            if next_move_wins:
                row_scores.append(-MAX_SCORE // 2)
                continue
        row_scores.append(
            (2**num_of_pieces) * attributes_num
        )  # Multiple shared attributes count as multiple rows
    score = sum(row_scores)
    return score, winning_attributes


def get_rows_from_board(board: GameState) -> list[list[Piece]]:
    """
    :param board:   The current gamestate that is being evaluated
    :return:        A list of all the rows in the board
    """
    length = len(board)
    rows = [[] for _ in range(length)]
    cols = [[] for _ in range(length)]
    diagonals = [[] for _ in range(2)]
    for i in range(length):
        for j in range(length):
            piece = board[i][j]
            rows[i].append(piece)
            cols[j].append(piece)
            if i == j:
                diagonals[0].append(piece)
            if i == length - j - 1:
                diagonals[1].append(piece)
    return rows + cols + diagonals


def calculate_row_attributes(row: list[Piece]) -> tuple[list[bool | int], int]:
    """
    :param row:     A row in the board
    :return:        A tuple containing the shared attributes and the number of pieces
    """
    attributes, num_of_pieces = [], 0
    for piece in row:
        if piece is None:
            continue
        attributes[:] = (
            piece.attributes
            if num_of_pieces == 0
            else map(
                lambda x, y: x if x == y else NO_ATTRIBUTES,
                attributes,
                piece.attributes,
            )
        )
        # [:] in order to avoid casting and mutate the list
        num_of_pieces += 1
    return attributes, num_of_pieces


def update_winning_attributes(
    winning_attributes: list[bool | int], attributes: list[bool | int]
) -> bool:
    """
    :param winning_attributes:  The shared attributes of previous 3-in-a-row rows
    :param attributes:          The attributes of the current 3-in-a-row row
    :return:                    If the next player has a guaranteed win the next turn
    """
    assert len(winning_attributes) == len(attributes) == Piece.NUM_OF_ATTRIBUTES
    next_move_wins = False
    for i in range(len(winning_attributes)):
        if winning_attributes[i] == NO_ATTRIBUTES:
            winning_attributes[i] = attributes[i]
        elif attributes[i] not in (NO_ATTRIBUTES, winning_attributes[i]):
            winning_attributes[i] = BOTH_ATTRIBUTES
            next_move_wins = True
    return next_move_wins


def pick_starting_piece(pieces_set: set[Piece]) -> Piece:
    """
    :param pieces_set:  A set containing which pieces can be played
    :return:            Which piece the computer should give the player
    """
    return random.choice(tuple(pieces_set))


def pick_best(board: GameState, piece: Piece, pieces_set: set[Piece]) -> Option:
    """
    :param board:       The current GameState
    :param piece:       The piece to insert
    :param pieces_set:  A set of available pieces to play
    :return:            The move with the highest score
    """
    pieces_set.remove(piece)
    options = get_options(board, piece, pieces_set, best_moves=True)
    blacklist = evaluate(options[0].game_state)[
        1
    ]  # All GameStates in options are the same
    option = options.pop(0)
    while len(options) > 0 and shared_attributes(option.piece.attributes, blacklist):
        option = options.pop(0)
    return option


def get_options(
    board: GameState, piece: Piece, pieces_set: set[Piece], best_moves: bool = False
) -> list[Option]:
    """
    :param board:               The current GameState
    :param piece:               The piece to insert
    :param pieces_set:          A set containing all playable moves
    :param best_moves:          If creating an options list for the pick_best function
    :return:                    A list of all possible moves
    """
    if piece in pieces_set:
        raise ValueError(":pieces_set: should contain :piece:!")
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                continue
            option = deepcopy(board)
            option[i][j] = piece
            if contains_symmetries(out, option):
                continue
            score, black_list = evaluate(option)
            if not out or BOTH_ATTRIBUTES not in black_list:
                option_list = get_playable_moves(option, pieces_set, i, j, black_list)
                tt_entry = GameState.transposition_table.get(option_list[0])
                score = tt_entry.value if tt_entry is not None else score
                out.append((option_list, score))
    assert len(out) > 0
    out.sort(
        key=lambda x: x[1], reverse=True
    )  # Sort moves by base score in descending order
    return (
        out[0][0] if best_moves else [x for option_list in out for x in option_list[0]]
    )
    # Return the list with the highest base score if generating options for pick_best, otherwise flatten the 2D list
    # into a regular list


def contains_symmetries(
    options: list[tuple[list[Option], int]], option: GameState
) -> bool:
    """
    :param options:     The current list of potential moves
    :param option:      The option to be added
    :return:            If options already contains an GameState that is a transformation of option
    """
    symmetries = get_symmetries(option.board)
    return any(
        any(np.array_equal(symmetry, board) for symmetry in symmetries)
        for board in (tuple_[0][0].game_state.board for tuple_ in options)
        # All options in options[i] have same game_state
    )


def get_symmetries(matrix: np.ndarray) -> list[np.ndarray]:
    """
    :param matrix:  A 2D matrix
    :return:        All flips and rotations of :matrix:z
    """
    flips = [np.flipud(matrix), np.fliplr(matrix)]
    rotations = [np.rot90(matrix, i) for i in range(1, 4)]
    rotated_flips = [np.rot90(flip, i) for flip in flips for i in range(1, 4)]
    return rotations + flips + rotated_flips


def get_playable_moves(
    option: GameState,
    pieces_set: set[Piece],
    i: int,
    j: int,
    blacklist: list[bool | int],
) -> list[Option]:
    """
    Checks what pieces can be given to the next player without them winning

    :param option:      The option's GameState
    :param pieces_set:  A set of all playable pieces
    :param i:           First index of inserted piece
    :param j:           Second index of inserted piece
    :param blacklist:   A piece attribute blacklist generated by the evaluate function
    :return:            A list of all playable moves with :option: as its GameState
    """
    options = [
        Option(option.board, piece, i, j)
        for piece in pieces_set
        if not shared_attributes(piece.attributes, blacklist)
    ]
    return (
        options
        if len(options) > 0
        else [Option(option.board, tuple(pieces_set)[0], i, j)]
    )


def shared_attributes(
    attributes: tuple[bool, ...], blacklist: list[bool | int]
) -> bool:
    """
    :param attributes:  A list of a pieces attributes
    :param blacklist:   A list of a second piece's attributes
    :return:            If :attributes: and :blacklist: have any shared attributes
    """
    assert len(attributes) == len(blacklist) == Piece.NUM_OF_ATTRIBUTES
    return any(
        blacklist[i] == BOTH_ATTRIBUTES or attributes[i] == blacklist[i]
        for i in range(Piece.NUM_OF_ATTRIBUTES)
    )


def iterative_deepening(
    board: GameState,
    piece: Piece,
    pieces_set: set[Piece],
    sign: int,
    alpha: float,
    beta: float,
    max_depth: int,
) -> Option:
    """
    :param board:       The current GameState
    :param piece:       The piece to use in the turn
    :param pieces_set:  A set of all piece that can be played
    :param sign:        The sign of the player (+1 for computer, -1 for human)
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param max_depth:   How many moves the computer can look ahead
    :return:            The best score/index of the best move for :player: and the piece to play

    .. seealso::        https://www.chessprogramming.org/Iterative_Deepening
    """
    if max_depth <= 0:
        raise ValueError(":max_depth: has to be a positive integer!")
    start_time = time()
    best_move = None
    depth, run_time = 0, 0
    while best_move is None or (depth <= max_depth and 1.5 * run_time < MAX_TIME):
        best_move, score = alpha_beta(
            Option(board, piece), deepcopy(pieces_set), sign, alpha, beta, depth
        )
        if evaluate(best_move.game_state)[0] >= MAX_SCORE:
            break
        depth += 1
        run_time = time() - start_time
    return best_move


def alpha_beta(
    move: Option,
    pieces_set: set[Piece],
    sign: int,
    alpha: float,
    beta: float,
    depth: int,
) -> tuple[Option, int]:
    """
    :param move:        An option object generated by get_options or iterative_deepening
    :param pieces_set:  A set of all piece that can be played
    :param sign:        The sign of the player (+1 for computer, -1 for human)
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param depth:       How many moves the computer can look ahead
    :return:            The best score/index of the best move for :player: and the piece to play

    .. seealso::        https://www.chessprogramming.org/Alpha-Beta\n
                        https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning\n
                        https://www.chessprogramming.org/Transposition_Table\n
                        https://en.wikipedia.org/wiki/Transposition_table
    """
    original_alpha = alpha
    tt_entry = GameState.transposition_table.get(move)
    if move.is_valid() and tt_entry is not None and tt_entry.depth >= depth:
        if tt_entry.flag == TTFlag.lower_bound:
            alpha = max(alpha, tt_entry.value)
        elif tt_entry.flag == TTFlag.upper_bound:
            beta = min(beta, tt_entry.value)
        if tt_entry.flag == TTFlag.exact or alpha >= beta:
            return tt_entry.move, tt_entry.value

    val = evaluate(move.game_state)[0]
    if val == MAX_SCORE:
        return move, -val * (depth + 1)
    if depth == 0 or len(pieces_set) <= 1:
        return move, sign * val

    pieces_set.remove(move.piece)
    options = get_options(move.game_state, move.piece, pieces_set)
    best_option, best_score = None, -inf
    for option in options:
        score = -alpha_beta(option, pieces_set, -sign, -beta, -alpha, depth - 1)[1]
        if score > best_score:
            best_option = option
            best_score = score
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    pieces_set.add(move.piece)
    assert best_option is not None and best_score != -inf

    flag = Transposition.get_flag(best_score, original_alpha, beta)
    GameState.transposition_table[move] = Transposition(
        best_option, best_score, flag, depth
    )
    return best_option, best_score
