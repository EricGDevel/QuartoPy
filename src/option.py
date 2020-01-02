"""
Module option.py
================

Contains the Option class
"""

__version__ = '0.0'
__author__ = 'Eric G.D'

from typing import List, Tuple

from src.piece import Piece


class Option:
    """
    Class Option:
    -------------

    Contains all the data of a single option (move) the computer can make
    """

    def __init__(self, game_state: List[List[Piece]], index: Tuple[int, int], piece: Piece) -> None:
        self.__game_state = game_state
        self.__index = index
        self.__piece = piece

    def __str__(self) -> str:
        return 'Option({})'.format(', '.join([f"{k}: {v}" for k, v in self.__dict__.items()]))

    @property
    def game_state(self) -> List[List[Piece]]:
        return self.__game_state

    @property
    def index(self) -> Tuple[int, int]:
        return self.__index

    @property
    def i(self) -> int:
        return self.__index[0]

    @property
    def j(self) -> int:
        return self.__index[1]

    @property
    def piece(self) -> Piece:
        return self.__piece
