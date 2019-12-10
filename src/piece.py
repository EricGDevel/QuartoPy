import os

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class Piece:

    BLANK_IMAGE = ''
    NUM_OF_BITS = 4
    MAX_NUM = (2 ** NUM_OF_BITS) - 1

    def __init__(self, num):
        if not isinstance(num, int):
            raise TypeError(':num: needs to be an integer!')
        if not 0 <= num <= Piece.MAX_NUM:
            raise ValueError(f':num: needs to be between 0 and {Piece.MAX_NUM}')
        self.__id = num
        self.__attributes = tuple([bool(int(bit)) for bit in ('{0:0=%db}' % Piece.NUM_OF_BITS).format(num)])
        self.__image = os.path.join('..', 'assets', f'piece_{str(num).zfill(2)}.png')

    def __eq__(self, other):
        return isinstance(other, Piece) and other.__id == self.__id

    @property
    def isLarge(self):
        return self.__attributes[0]

    @property
    def isRound(self):
        return self.__attributes[1]

    @property
    def isHollow(self):
        return self.__attributes[2]

    @property
    def isWhite(self):
        return self.__attributes[3]

    @property
    def image(self):
        return self.__image

    @property
    def id(self):
        return self.__id


class Cell(ButtonBehavior, Image):

    def __init__(self):
        ButtonBehavior.__init__(self)
        Image.__init__(self)
        self.__piece = None
        self.source = Piece.BLANK_IMAGE

    @property
    def piece(self):
        return self.__piece

    @piece.setter
    def piece(self, p):
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

