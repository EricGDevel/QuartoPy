from src.piece import *
from src.enums import *
from src.minimax import minimax, pick_piece

from kivy.uix.gridlayout import GridLayout


class Board(GridLayout):
    """
    Class Board(GridLayout):
    The main game board, also returned by QuartoApp.build
    """

    LENGTH = 4
    DIFFICULTY = {'baby': 0, 'easy': 4, 'medium': 8,
                  'hard': 12, 'impossible': LENGTH ** 2}
    popup = None

    def __init__(self, **kwargs):
        super().__init__()
        self.rows = self.cols = Board.LENGTH
        self.first_player = self.current_player = kwargs.get('first_player', Player.MINIMISING)
        self.game_mode = kwargs.get('game_mode', GameMode.SINGLE_PLAYER)
        self.depth = Board.DIFFICULTY[kwargs.get('difficulty', 'hard')]
        self.pieces_set = set([Piece(num) for num in range(Board.LENGTH ** 2)])
        self.selected = None
        self.button_list = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.init_buttons()
        self.first_move()   

    def init_buttons(self, reset=False):
        """
        Initialises/resets the button objects in self.button_list by doing the following:
        - Binding the on_click function
        - Setting the buttons text value to a blank string  (On reset)
        - Adding the button to the Board                    (On init)
        :param reset:   Whether to reset or initialise the buttons
        :return:        None
        """
        for row in self.button_list:
            for cell in row:
                cell.bind(on_release=self.on_click)
                if reset:
                    cell.piece = None
                else:
                    self.add_widget(cell)

    def first_move(self):
        if self.game_mode == GameMode.SINGLE_PLAYER and self.first_player == Player.COMPUTER:
            self.computer_move()

    def computer_move(self):
        if self.selected is None:
            pick_piece(self.button_list, self.pieces_set, self.depth)
        i, j = minimax(self.button_list, self.selected, self.pieces_set,  self.depth)
        self.insert(self.button_list[i][j], self.current_player)
        self.change_player()

    def change_player(self):
        """
        Sets the current player
        :return:        None
        """
        self.current_player = Player.COMPUTER if self.current_player != Player.COMPUTER else Player.HUMAN

    def on_click(self, touch):
        pass

