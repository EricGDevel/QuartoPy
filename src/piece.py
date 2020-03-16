"""
Module piece.py
===============

Contains the declarations of the Piece and Cell classes.
"""

__all__ = ['Piece', 'Cell']
__version__ = '1.1'
__author__ = 'Eric G.D'

import os
from functools import partial
from typing import Any, Tuple, Union

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage


class Piece:
    """
    Class Piece
    -----------

    Contains the data of every piece, including it's id number, attributes tuple and image representation
    """
    NUM_OF_BITS = 4
    MAX_NUM = (2 ** NUM_OF_BITS) - 1

    def __init__(self, num: int) -> None:
        self.__id = num
        self.__attributes = Piece.get_attributes(num)
        self.__image = os.path.join('assets', f'piece_{str(num).zfill(2)}.png')

    @staticmethod
    def get_attributes(num: int) -> Tuple[bool, ...]:
        """
        :param num:     The piece's ID
        :return:        The attributes of the piece with the id :num: (Based on the :num:'s binary representation)
        """
        if not isinstance(num, int):
            raise TypeError(f':num: needs to be an int, not {type(num)}!')
        if not 0 <= num <= Piece.MAX_NUM:
            raise ValueError(f':num: needs to be between 0 and {Piece.MAX_NUM}')
        binary_str = format(num, 'b').zfill(Piece.NUM_OF_BITS)
        attributes = [bit == '1' for bit in binary_str]
        return tuple(attributes)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Piece) and other.__id == self.__id

    def __hash__(self) -> int:
        return hash(self.__id)

    def __str__(self) -> str:
        attribute_strings = (('Small', 'Large'), ('Square', 'Round'), ('Solid', 'Hollow'), ('Black', 'White'))
        atts = [1 if att else 0 for att in self.__attributes]
        return '{%s}' % ', '.join([attribute_strings[i][att] for i, att in enumerate(atts)])

    @property
    def attributes(self) -> Tuple[bool, ...]:
        return self.__attributes

    @property
    def is_large(self) -> bool:
        return self.__attributes[0]

    @property
    def is_round(self) -> bool:
        return self.__attributes[1]

    @property
    def is_hollow(self) -> bool:
        return self.__attributes[2]

    @property
    def is_white(self) -> bool:
        return self.__attributes[3]

    @property
    def image(self) -> str:
        return self.__image

    @property
    def id(self) -> int:
        return self.__id


class Cell(ButtonBehavior, AsyncImage):
    """
    class Cell(ButtonBehavior, AsyncImage)
    --------------------------------------

    Represents a cell in the game board and a button in PiecesBar
    This class is essentially a graphic wrapper for Piece
    """
    BLANK_IMAGE = os.path.join('assets', 'blank.png')

    def __init__(self, piece: Union[None, int, Piece] = None):
        ButtonBehavior.__init__(self)
        AsyncImage.__init__(self)
        if isinstance(piece, int):
            piece = Piece(piece)
        if not isinstance(piece, Piece) and piece is not None:
            raise TypeError(f'{type(piece)} is not a valid type for :piece:!')
        self.__piece = piece
        self.source = piece.image if piece is not None else Cell.BLANK_IMAGE

    @property
    def piece(self) -> Piece:
        return self.__piece

    @piece.setter
    def piece(self, p: Union[None, int, Piece]) -> None:
        if p is None:
            self.__piece = p
            self.source = Cell.BLANK_IMAGE
        elif isinstance(p, int):
            if not 0 <= p <= Piece.MAX_NUM:
                raise ValueError(f':p: needs to be between 0 and {Piece.MAX_NUM}')
            self.__piece = Piece(p)
            self.source = self.__piece.image
        elif isinstance(p, Piece):
            self.__piece = p
            self.source = self.__piece.image
        else:
            raise TypeError(f'{type(p)} is not a valid type for :p:!')

    def set_background_color(self, color: Tuple[int, int, int, int]) -> None:
        self.canvas.before.clear()
        Clock.schedule_once(partial(self.__set_bg_color, color))

    def __set_bg_color(self, color: Tuple[int, int, int, int], *largs) -> None:
        with self.canvas.before:
            Color(rgba=color)
            Rectangle(pos=self.pos, size=self.size)
