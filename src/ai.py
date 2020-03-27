"""
Module ai.py
=================

Contains all AI functions that allow the computer to make the best move.
Uses the NegaMax algorithm with alpha-beta pruning, symmetry detection and a transposition table.
"""

__all__ = ['evaluate', 'has_won', 'make_move', 'pick_best', 'pick_starting_piece']
__version__ = '1.2'
__author__ = 'Eric G.D'

import random
from copy import deepcopy
from math import inf
from typing import Set

from src.constants import MAX_SCORE
from src.option import *
from src.piece import Piece


def has_won(state: GameState) -> bool:
    """
    :param state:   The current GameState
    :return:        True if the board is full, false otherwise
    """
    return evaluate(state)[0] == MAX_SCORE


def evaluate(state: GameState) -> Tuple[int, List[int]]:
    """
    :param state:       The GameState to evaluate
    :return:            :board:'s static evaluation and what attributes the next piece needs to have in order to win
    """
    length = len(state)
    assert length == Piece.NUM_OF_ATTRIBUTES
    rows = get_rows_from_board(state.board)
    row_scores = []
    winning_attributes = [-1] * Piece.NUM_OF_ATTRIBUTES
    for row in rows:
        assert len(row) == length
        attributes, num_of_pieces = calculate_row_attributes(row)
        attributes_num = length - attributes.count(-1) if num_of_pieces > 1 else 0
        if attributes_num > 0:
            if num_of_pieces == length:
                row_scores = [MAX_SCORE]
                break
            elif num_of_pieces == length - 1:
                next_move_wins = update_winning_attributes(winning_attributes, attributes)
                if next_move_wins:
                    row_scores.append(-MAX_SCORE // 2)
                    continue
        row_scores.append((2 ** num_of_pieces) * attributes_num)  # Multiple shared attributes count as multiple rows
    score = sum(row_scores)
    return score, winning_attributes


def get_rows_from_board(board: np.ndarray) -> List[List[Piece]]:
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
            attributes = list(piece.attributes)
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


def pick_best(board: GameState, piece: Piece,
              pieces_set: Set[Piece]) -> Option:
    """
    :param board:       The current GameState
    :param piece:       The piece to insert
    :param pieces_set:  A set of available pieces to play
    :return:            The move with the highest score
    """
    pieces_set.remove(piece)
    options = get_options(board, piece, pieces_set, best_moves=True)
    assert len(options) > 0
    # The move with the highest base score appears first
    blacklist = evaluate(options[0].game_state)[1]  # All GameStates in options are the same
    option = options.pop(0)
    while len(options) > 0 and shared_attributes(option.piece.attributes, blacklist):
        option = options.pop(0)
    return option


def get_options(board: GameState, piece: Piece,
                pieces_set: Set[Piece], best_moves: bool = False) -> List[Option]:
    """
    :param board:               The current GameState
    :param piece:               The piece to insert
    :param pieces_set:          A set containing all playable moves
    :param best_moves:           If creating an options list for the pick_best function
    :return:                    A list of all possible moves
    """
    assert piece not in pieces_set
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
            if -2 not in black_list:
                out.append((get_playable_moves(option, pieces_set, i, j, black_list), score))
    if out:
        out.sort(key=lambda x: x[1], reverse=True)  # Sort moves by base score in descending order
        return out[0][0] if best_moves else [x for option_list in out for x in option_list[0]]
    return []
    # Return the list with the highest base score if generating options for pick_best, otherwise flatten the 2D list
    # into a regular list


def contains_symmetries(options: List[Tuple[List[Option], int]], option: GameState) -> bool:
    """
    :param options:     The current list of potential moves
    :param option:      The option to be added
    :return:            If options already contains an GameState that is a transformation of option
    """
    for tuple_ in options:
        game_state = tuple_[0][0].game_state.board  # All options in current list have same game_state
        flips = [np.flip(option, i) for i in range(2)]
        rotations = [np.rot90(option, i) for i in range(1, 4)]
        rotated_flips = [np.rot90(flip, i) for flip in flips for i in range(1, 4)]
        transformations = rotations + flips + rotated_flips
        if any(np.array_equal(transformation, game_state) for transformation in transformations):
            return True
    return False


def get_playable_moves(option: GameState, pieces_set: Set[Piece], i: int, j: int,
                       blacklist: List[Union[bool, int]]) -> List[Option]:
    """
    Checks what pieces can be given to the next player without them winning
    :param option:      The option's GameState
    :param pieces_set:  A set of all playable pieces
    :param i:           First index of inserted piece
    :param j:           Second index of inserted piece
    :param blacklist:   A piece attribute blacklist generated by the evaluate function
    :return:            A list of all playable moves with :option: as its GameState
    """
    options = []
    if -2 not in blacklist:
        for piece in pieces_set:
            if shared_attributes(piece.attributes, blacklist):
                continue
            options.append(Option(option.board, piece, i, j))
    if not options:
        options.append(Option(option.board, tuple(pieces_set)[0], i, j))
    return options


def shared_attributes(attributes: Tuple[bool, ...], blacklist: List[Union[bool, int]]) -> bool:
    """
    :param attributes:  A list of a pieces attributes
    :param blacklist:   A list of a second piece's attributes
    :return:            If :attributes: and :blacklist: have any shared attributes
    """
    assert len(attributes) == len(blacklist) == Piece.NUM_OF_ATTRIBUTES
    return any(attributes[i] == blacklist[i] for i in range(Piece.NUM_OF_ATTRIBUTES))


def make_move(board: GameState, piece: Piece, pieces_set: Set[Piece], sign: int, alpha: float, beta: float,
              depth: int, get_move: bool) -> Union[int, Option]:
    """
    :param board:       The current GameState
    :param piece:       The piece to use in the turn
    :param pieces_set:  A set of all piece that can be played
    :param sign:        The sign of the player (+1 for computer, -1 for human)
    :param alpha:       Lower bound for best_score
    :param beta:        Upper bound for best_score
    :param depth:       How many moves the computer can look ahead
    :param get_move:    Whether to return the best option or the score of the best option
    :return:            The best score/index of the best move for :player: and the piece to play
    """
    original_alpha = alpha
    entry_key = Option(board.board, piece)
    tt_entry = GameState.transposition_table.get(entry_key)
    if not get_move and tt_entry is not None and tt_entry.depth >= depth:
        if tt_entry.flag == TTFlag.exact:
            return tt_entry.value
        if tt_entry.flag == TTFlag.lower_bound:
            alpha = max(alpha, tt_entry.value)
        elif tt_entry.flag == TTFlag.upper_bound:
            beta = min(beta, tt_entry.value)
        if alpha >= beta:
            return tt_entry.value

    val = evaluate(board)[0]
    if val == MAX_SCORE:
        return -val * (depth + 1)
    if depth == 0 or len(pieces_set) <= 1:
        return sign * val

    pieces_set.remove(piece)
    options = get_options(board, piece, pieces_set)
    assert len(options) > 0
    best_option, best_score = None, -inf
    for option in options:
        score = -make_move(option.game_state, option.piece, pieces_set, -sign, -beta, -alpha, depth - 1, False)
        if score > best_score:
            best_option = option
            best_score = score
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    pieces_set.add(piece)

    flag = Transposition.get_flag(best_score, original_alpha, beta)
    tt_entry = Transposition(best_score, flag, depth)
    GameState.transposition_table[best_option] = tt_entry
    return best_option if get_move else best_score
