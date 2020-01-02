"""
Module constants.py
============

This module contains all the enums and constants used by the other modules of the project
"""

__version__ = '0.0'
__author__ = 'Eric G.D'

from enum import Enum


class GameMode(Enum):
    SINGLE_PLAYER = 0
    MULTI_PLAYER = 1


class Player(Enum):
    COMPUTER = 1
    HUMAN = -1

    def __invert__(self):
        return Player.COMPUTER if self != Player.COMPUTER else Player.HUMAN


class Color(Enum):
    WHITE = (1, 1, 1, 1)
    SELECTED_TINT = (0.5, 0.5, 0.5, 0.5)
