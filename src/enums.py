from enum import Enum


class GameMode(Enum):
    SINGLE_PLAYER = 0
    MULTI_PLAYER = 1


class Player(Enum):
    COMPUTER = 1
    HUMAN = -1

