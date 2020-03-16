"""
Module option.py
================

Contains the Option class
"""

__version__ = '1.1'
__author__ = 'Eric G.D'

from typing import List, Tuple

import numpy as np

from src.piece import Piece


class Option:
    """
    Class Option:
    -------------

    Contains all the data of a single option (move) the computer can make
    """

    def __init__(self, game_state: List[List[Piece]], i: int, j: int, piece: Piece) -> None:
        self.__game_state = np.array(game_state)
        self.__index = i, j
        self.__piece = piece

    def __repr__(self) -> str:
        return f'Option(\n\tGameState: {self.__game_state}\n\tIndex: {self.__index}\n\tPiece: {self.__piece}\n)\n'

    @property
    def game_state(self) -> np.array:
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
