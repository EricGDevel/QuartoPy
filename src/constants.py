"""
Module constants.py
===================

This module contains all the enums and constants used by the other modules of the project
"""

from __future__ import annotations

from enum import Enum

__version__ = "1.4.0"
__author__ = "Eric G.D"

MAX_SCORE: int = 10**5
MAX_TIME: int = 2

NO_INDEX: int = -1
HASH_BITS: int = 64

NO_ATTRIBUTES: int = -1
BOTH_ATTRIBUTES: int = -2


class GameMode(Enum):
    """
    Class GameMode(Enum):
    ---------------------

    An enum that contains all the possible game modes.
    Used by board to determine what happens after a player makes as move
    """

    single_player = 0
    multi_player = 1


class Player(Enum):
    """
    Class Player(Enum):
    -------------------

    An enum containing the types/numbers of the current players
    Used by Board to assign minimising/maximising signs to NegaMax and to display the end of game message
    """

    human = 1
    computer = 2


class TTFlag(Enum):
    """
    Class TTFlag(Enum):
    -------------------

    An enum that represents the types of transpositions that are stored in the transposition table
    exact:          The calculated value is an exact value for the game state, and can be returned immediately
    upper_bound:    The calculated value is an upper bound for the current game state, so the alpha value can be
                    updated to reduce search time
    lower_bound:    Similar to upper_bound, the previously calculated score is a lower_bound and thus the beta
                    value of the current calculation can be updated to reduce search time
    """

    exact = 0
    lower_bound = 1
    upper_bound = 2


def next_player(player: Player) -> Player:
    """
    :param player:  The current player
    :return:        The player who is next to play
    """
    return Player.human if player == Player.computer else Player.computer


class Colors:
    """
    Class Colors:
    -------------

    A class containing rgba tuples for colors used in the UI
    """

    selected = (0.8, 0.8, 0.2, 0.8)
    confirmed = (0.2, 0.8, 0.2, 0.8)
    board = (0.5, 0.5, 0.5, 1)
    pieces_bar = (0.2, 0.2, 0.5, 1)
    white = (1, 1, 1, 1)
    cyan = (0.2, 0.8, 0.8, 1)
    green = (0.2, 0.8, 0.2, 1)
    blue = (0.2, 0.2, 0.8, 1)
    red = (0.8, 0.2, 0.2, 1)
    transparent = (1, 1, 1, 0)
