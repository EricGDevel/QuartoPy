"""
Module piece.py
===============

Contains the declarations of the Piece and Cell classes.
"""

__all__ = ['Piece', 'Cell']
__version__ = '0.0'
__author__ = 'Eric G.D'

import os
from typing import Any, Optional, Union

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class Piece:

    BLANK_IMAGE = ''
    NUM_OF_BITS = 4
    MAX_NUM = (2 ** NUM_OF_BITS) - 1

    def __init__(self, num: int) -> None:
        if not isinstance(num, int):
            raise TypeError(':num: needs to be an integer!')
        if not 0 <= num <= Piece.MAX_NUM:
            raise ValueError(f':num: needs to be between 0 and {Piece.MAX_NUM}')
        self.__id = num
        self.__attributes = tuple([bool(int(bit)) for bit in ('{0:0=%db}' % Piece.NUM_OF_BITS).format(num)])
        self.__image = os.path.join('..', 'assets', f'piece_{str(num).zfill(2)}.png')

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Piece) and other.__id == self.__id

    def __hash__(self) -> int:
        return hash(self.__id)

    @property
    def isLarge(self) -> bool:
        return self.__attributes[0]

    @property
    def isRound(self) -> bool:
        return self.__attributes[1]

    @property
    def isHollow(self) -> bool:
        return self.__attributes[2]

    @property
    def isWhite(self) -> bool:
        return self.__attributes[3]

    @property
    def image(self) -> str:
        return self.__image

    @property
    def id(self) -> int:
        return self.__id


class Cell(ButtonBehavior, Image):

    def __init__(self, piece: Optional[int, Piece] = None):
        ButtonBehavior.__init__(self)
        Image.__init__(self)
        if isinstance(piece, int):
            piece = Piece(piece)
        self.__piece = piece
        try:
            self.source = piece.image if piece is not None else Piece.BLANK_IMAGE
        except AttributeError:
            raise TypeError(":piece: can only be None, int, or Piece!")

    @property
    def piece(self) -> Piece:
        return self.__piece

    @piece.setter
    def piece(self, p: Union[None, int, Piece]) -> None:
        if p is None:
            self.__piece = p
            self.source = Piece.BLANK_IMAGE
        elif isinstance(p, int):
            if not 0 <= p <= Piece.MAX_NUM:
                raise ValueError(f':piece: needs to be between 0 and {Piece.MAX_NUM}')
            self.__piece = Piece(p)
            self.source = self.__piece.image
        elif isinstance(p, Piece):
            self.__piece = p
            self.source = self.__piece.image
        else:
            raise TypeError('Invalid type for :piece:!')
