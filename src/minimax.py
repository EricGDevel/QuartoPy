from copy import deepcopy
from math import inf
from src.piece import Piece
from src.enums import Player
from src.option import Option

MAX_SCORE = 10 ** 5


def convert(button_list):
    """
    :param button_list:     The list of all buttons in Board
    :return:                A simplified version of :button_list:
    """
    return [[cell.piece for cell in row] for row in button_list]


def is_full(board):
    """
    :param board:   The current gamestate/Set of pieces that can be played
    :return:        True if the board is full, false otherwise
    """
    if isinstance(board, list):
        return not any([piece is None for row in board for piece in row])
    if isinstance(board, set):
        return len(board) == 0
    raise TypeError(":board: must be a board list or the set of available pieces!")


def evaluate(board, player=Player.COMPUTER):
    """
    :param board:   The current gamestate
    :param player:  The player to evaluate for
    :return:        :board:'s ranking
    """
    pass


def pick_piece(button_list, pieces_set, depth):
    """
    :param button_list: A 2D List containing the board's buttons
    :param pieces_set:  A set containing which pieces can be played
    :param depth:       The maximum recursion depth for the function
    :return:            Which piece the computer should play
    """
    pass


def minimax(button_list, piece, pieces_set, depth, player=Player.COMPUTER):
    """
    :param button_list:     A matrix containing the buttons in the game_board
    :param piece:           The piece to use in the turn
    :param pieces_set:      A set of all piece that can be played
    :param depth:           The maximum recursion depth for the function
    :return:                The indexes of the best move for the computer (Maximising player)
    """
    board = convert(button_list)
    if depth <= 0:
        return pick_best(board, player, pieces_set, piece)
    alpha = -inf
    beta = inf
    return make_move(board, piece, pieces_set, Player.COMPUTER, alpha, beta, depth, depth)


def pick_best(board, piece, pieces_set, player=Player.COMPUTER):
    """
    :param board:       The current gamestate
    :param pieces_set:  A set of available pieces to play
    :param piece:       The piece to insert
    :param player:      The player to pick the best move for
    :return:            The move with the highest score
    """
    if not isinstance(player, Player) or not isinstance(piece, Piece) or not isinstance(pieces_set, set):
        raise TypeError("One of the paramters is an invalid type!")
    options = get_options(board, piece, pieces_set)
    scores = [evaluate(option.gamestate) for option in options]
    best_score = max(scores) if player == Player.COMPUTER else min(scores)
    return options[scores.index(best_score)]


def get_options(board, piece, available_pieces):
    """
    :param board:               The current gamestate
    :param piece:               The piece to insert
    :param available_pieces:    A set containing all playable moves
    :return:                    A list of all possible moves
    """
    if not isinstance(piece, Piece) or not isinstance(available_pieces, set):
        raise TypeError(":piece: needs to be a Piece object and :available_pieces: needs to be a set!")
    if piece not in available_pieces:
        raise ValueError(":piece: has to be in :available_pieces:!")
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                option = deepcopy(board)
                option[i][j] = piece
                # TODO: Optimise this section using pick_best instead of iteration over all possible pieces
                for next_piece in available_pieces:
                    if next_piece is piece:
                        continue
                    out.append(Option(option, (i, j), next_piece))
    return out


def make_move(board, player, piece, pieces_set, alpha, beta, depth, idepth):
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
    if depth == 0 or is_full(board):
        return val
    options = get_options(board, piece, pieces_set)
    rival = Player.HUMAN if player == Player.COMPUTER else Player.COMPUTER
    best_index = options[0].index
    best_score = make_move(options[0].gamestate, rival, options[0].piece,  alpha, beta, depth - 1, idepth)
    for option in options[1:]:
        score = make_move(option.gamestate, rival, option.piece,  alpha, beta, depth - 1, idepth)
        if better_move(player, score, best_score):
            best_index = option.index
            best_score = score
        if alpha < best_score and player == Player.COMPUTER:
            alpha = best_score
        elif beta > best_score and player == Player.HUMAN:
            beta = best_score
        if beta <= alpha:
            break
    best_score = -best_score if player == Player.HUMAN else best_score
    return best_score if depth != idepth else best_index


def better_move(player, score, best_score):
    """
    :param player:      Tells the computer if looking for min or max scores (str, Player.HUMAN/Player.COMPUTER)
    :param score:       The new score
    :param best_score:  The previous best score
    :return:            If :score: is better than :best_score:
    """
    return score > best_score if player == Player.COMPUTER else score < best_score
