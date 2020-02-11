"""
Module constants.py
============

This module contains all the enums and constants used by the other modules of the project
"""

__version__ = '0.3'
__author__ = 'Eric G.D'

from enum import Enum


class GameMode(Enum):
    single_player = 0
    multi_player = 1


class Player(Enum):
    human = 1
    computer = 2

    def __invert__(self):
        return Player.computer if self != Player.computer else Player.human


class Color(Enum):
    WHITE = (1, 1, 1, 1)
    SELECTED_TINT = (0.5, 0.5, 0, 0.75)
    CONFIRMED_TINT = (0, 0.5, 0, 0.75)
