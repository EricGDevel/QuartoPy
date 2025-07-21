"""
Module option.py
================

Contains the Option class
"""

from __future__ import annotations

__version__ = "1.4.0"
__author__ = "Eric G.D"

from collections.abc import Iterable
from random import getrandbits
from typing import Any

import numpy as np

from src.constants import HASH_BITS, NO_INDEX, TTFlag
from src.piece import Piece


class Option:
    """
    Class Option:
    -------------

    Contains all the data of a single option (move) the computer can make
    """

    def __init__(
        self,
        game_state: GameState | np.ndarray,
        piece: Piece,
        i: int = NO_INDEX,
        j: int = NO_INDEX,
    ):
        self.__game_state: GameState = (
            game_state if isinstance(game_state, GameState) else GameState(game_state)
        )
        self.__piece: Piece = piece
        self.__index: tuple[int, int] = (i, j)

    def __repr__(self) -> str:
        return f"Option({self.__game_state!r}, {self.__piece!r}, {self.__index[0]}, {self.__index[1]})"

    def __hash__(self) -> int:
        return hash(self.__game_state) ^ GameState.selected_table[self.__piece.id]

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Option)
            and self.__game_state == other.__game_state
            and self.__piece == other.piece
        )

    def is_valid(self) -> bool:
        """
        :return:    If the option has a valid insertion index
        """
        return 0 <= self.i < GameState.LENGTH and 0 <= self.j < GameState.LENGTH

    @property
    def game_state(self) -> GameState:
        return self.__game_state

    @property
    def index(self) -> tuple[int, int]:
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


class Transposition:
    def __init__(self, move: Option, value: int, flag: TTFlag, depth: int):
        self.__move: Option = move
        self.__value: int = value
        self.__flag: TTFlag = flag
        self.__depth: int = depth

    def __repr__(self) -> str:
        return f"Transposition({self.__value}, {str(self.__flag)}, {self.__depth})"

    @staticmethod
    def get_flag(value: int, alpha: float, beta: float) -> TTFlag:
        """
        :param value:   The value of the current node being calculated
        :param alpha:   The original alpha value before the search began
        :param beta:    The latest beta value of the search
        :return:        The transposition flag for the current search
        """
        if alpha > beta:
            raise ValueError(":alpha: cannot be greater than :beta:!")
        if value <= alpha:
            return TTFlag.upper_bound
        if value >= beta:
            return TTFlag.lower_bound
        return TTFlag.exact

    @property
    def move(self) -> Option:
        return self.__move

    @property
    def value(self) -> int:
        return self.__value

    @property
    def flag(self) -> TTFlag:
        return self.__flag

    @property
    def depth(self) -> int:
        return self.__depth


class GameState:
    LENGTH: int = 4
    zobrist_table: list[list[list[int]]] = []
    selected_table: list[int] = []
    transposition_table: dict[Option, Transposition] = {}

    def __init__(self, state: np.ndarray | list[list[Piece]]):
        if not len(state) == len(state[0]) == GameState.LENGTH:
            raise ValueError(
                f"Invalid dimensions for :state:, should be a {GameState.LENGTH}x{GameState.LENGTH} array!"
            )
        self.__board: np.ndarray = np.array(state)
        if not GameState.zobrist_table:
            GameState.__zobrist_init()

    @property
    def board(self) -> np.ndarray:
        return self.__board

    def __getitem__(self, key: Any) -> np.ndarray:
        return self.__board[key]

    def __iter__(self) -> Iterable[np.ndarray]:
        return iter(self.board)

    def __hash__(self) -> int:
        """
        Uses the Zobrist hashing algorithm to provide a unique hash for the current game state
        :return:        A unique hash value for the current game state

        .. seealso:     https://en.wikipedia.org/wiki/Zobrist_hashing
                        https://www.chessprogramming.org/Zobrist_Hashing
        """
        hash_ = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is None:
                    continue
                hash_ ^= GameState.zobrist_table[i][j][self.board[i][j].id]
        return hash_

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, GameState) and np.array_equal(self.board, other.board)

    def __len__(self) -> int:
        return len(self.board)

    def __repr__(self) -> str:
        return f"Gamestate({self.__board.tolist()!r})"

    @staticmethod
    def __zobrist_init() -> None:
        """
        Initialises the zobrist table with random 64 bit numbers
        :return:    None
        """
        table = [
            [
                [
                    getrandbits(HASH_BITS) for _ in range(Piece.MAX_NUM + 1)
                ]  # For pieces in the board
                for _ in range(GameState.LENGTH)
            ]
            for _ in range(GameState.LENGTH)
        ]
        GameState.zobrist_table[:] = table
        GameState.selected_table[:] = [
            getrandbits(HASH_BITS) for _ in range(Piece.MAX_NUM + 1)
        ]  # For selected piece
