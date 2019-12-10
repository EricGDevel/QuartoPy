class Option:

    def __init__(self, gamestate, index, piece):
        self.__gamestate = gamestate
        self.__index = index
        self.__piece = piece

    @property
    def gamestate(self):
        return self.__gamestate

    @property
    def index(self):
        return self.__index

    @property
    def i(self):
        return self.__index[0]

    @property
    def j(self):
        return self.__index[1]

    @property
    def piece(self):
        return self.__piece