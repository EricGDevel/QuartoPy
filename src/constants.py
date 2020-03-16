"""
Module constants.py
============

This module contains all the enums and constants used by the other modules of the project
"""

__version__ = '1.1'
__author__ = 'Eric G.D'

from enum import Enum

MAX_SCORE = 10 ** 5


class GameMode(Enum):
    single_player = 0
    multi_player = 1


class Player(Enum):
    human = 1
    computer = 2


def next_player(player: Player) -> Player:
    return Player.human if player == Player.computer else Player.computer


class Colors:
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
