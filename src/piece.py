"""
Module piece.py
===============

Contains the declarations of the Piece and Cell classes.
"""

from __future__ import annotations

__all__ = ["Piece", "Cell"]
__version__ = "1.3"
__author__ = "Eric G.D"

from pathlib import Path
from typing import Any

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage


class Piece:
    """
    Class Piece
    -----------

    Contains the data of a piece, including it's id number, attributes tuple and image path
    """

    NUM_OF_ATTRIBUTES: int = 4
    MAX_NUM: int = (2**NUM_OF_ATTRIBUTES) - 1

    def __init__(self, num: int):
        self.__id: int = num
        self.__attributes: tuple[bool, ...] = Piece.get_attributes(num)
        self.__image: Path = Path("assets", f"piece_{str(num).zfill(2)}.png")

    @staticmethod
    def get_attributes(num: int) -> tuple[bool, ...]:
        """
        :param num:     The piece's ID
        :return:        The attributes of the piece with the id :num: (Based on the :num:'s binary representation)
        """
        if not isinstance(num, int):
            raise TypeError(f":num: needs to be an int, not {type(num)}!")
        if not 0 <= num <= Piece.MAX_NUM:
            raise ValueError(f":num: needs to be between 0 and {Piece.MAX_NUM}.")
        binary_str = format(num, "b").zfill(Piece.NUM_OF_ATTRIBUTES)
        return tuple(bit != "0" for bit in binary_str)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Piece) and other.__id == self.__id

    def __hash__(self) -> int:
        return self.__id

    def __repr__(self) -> str:
        return f"Piece({self.__id})"

    def __str__(self) -> str:
        """
        :return: A string containing the piece's attributes
        """
        attribute_strings = (
            ("Small", "Large"),
            ("Square", "Round"),
            ("Solid", "Hollow"),
            ("Black", "White"),
        )
        attributes = [1 if att else 0 for att in self.__attributes]
        return f"({', '.join(attribute_strings[i][att] for i, att in enumerate(attributes))})"

    @property
    def attributes(self) -> tuple[bool, ...]:
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
    def image(self) -> Path:
        return self.__image

    @property
    def id(self) -> int:
        return self.__id


class Cell(ButtonBehavior, AsyncImage):
    """
    class Cell(ButtonBehavior, AsyncImage)
    --------------------------------------

    Represents a cell in the game board and a button in PiecesBar
    This class is a graphic wrapper for Piece
    """

    BLANK_IMAGE = Path("assets", "blank.png")

    def __init__(self, piece: None | int | Piece = None):
        ButtonBehavior.__init__(self)
        AsyncImage.__init__(self)
        self.piece = piece

    @property
    def piece(self) -> Piece:
        return self.__piece

    @piece.setter
    def piece(self, p: None | int | Piece):
        if isinstance(p, int):
            self.__piece = Piece(p)
        elif not (p is None or isinstance(p, Piece)):
            raise TypeError(f"{type(p)} is not a valid type for :p:!")
        self.__piece: Piece = p
        self.source = str(p.image if p is not None else Cell.BLANK_IMAGE)

    def set_background_color(self, color: tuple[int, int, int, int]) -> None:
        """
        Change the background color of the cell
        This function is a wrapper for __set_bg_color, which is called by kivy.Clock
        :param color:   A tuple containing the rgba value of the color
        :return:        None
        """
        self.canvas.before.clear()
        Clock.schedule_once(lambda *_: self.__set_bg_color(color))

    def __set_bg_color(self, color: tuple[int, int, int, int]) -> None:
        """
        Places a colored rectangle behind the canvas of the cell
        :param color:   The color of the rectangle to place
        :return:        None
        """
        with self.canvas.before:
            Color(rgba=color)
            Rectangle(pos=self.pos, size=self.size)
