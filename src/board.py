"""
Module board.py
===============

This module contains the Board and PieceBar objects that are used by GameScreen
Note: Board contains all game functions that don't relate to AI
"""

__all__ = ['Board', 'PiecesBar']
__version__ = '0.0'
__author__ = 'Eric G.D'

from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from src.constants import *
from src.minimax import *
from src.piece import *


class Board(GridLayout):
    """
    Class Board(GridLayout):
    ------------------------

    The main game board, also returned by QuartoApp.build
    """

    LENGTH = 4
    DIFFICULTY = {'baby': 0, 'easy': 4, 'medium': 8,
                  'hard': 12, 'impossible': LENGTH ** 2}
    popup = None

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.rows = self.cols = Board.LENGTH
        self.first_player = self.current_player = kwargs.get('first_player', Player.HUMAN)
        self.game_mode = kwargs.get('game_mode', GameMode.SINGLE_PLAYER)
        self.depth = Board.DIFFICULTY[kwargs.get('difficulty', 'hard')]
        self.pieces_set = set([Piece(num) for num in range(Board.LENGTH ** 2)])
        self.cell_list = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.pieces_bar = None
        Logger.debug("Setup: Initialised new Board object")
        self.disabled = True    # Don't allow game to run until self.pieces_bar is not None

    def initialise_buttons(self, reset: bool = False) -> None:
        """
        Initialises/resets the button objects in self.button_list by doing the following:
        - Binding the on_click function
        - Setting the buttons text value to a blank string  (On reset)
        - Adding the button to the Board                    (On init)
        :param reset:   Whether to reset or initialise the buttons
        :return:        None
        """
        for row in self.cell_list:
            for cell in row:
                cell.bind(on_release=self.on_click)
                if reset:
                    cell.piece = None
                else:
                    self.add_widget(cell)

    def first_move(self) -> None:
        """
        Runs the first move:
        SINGLE_PLAYER:
        If Computer is the first player: Gets piece from player and runs the computer's move
        If Human is the first player: Ask the computer to pick a piece for the player to play.
        MULTI_PLAYER: Gets a piece from the first player and the second player's move
        :return:    None
        """
        if self.game_mode == GameMode.SINGLE_PLAYER:
            if self.first_player == Player.COMPUTER:
                self.computer_move()
            else:
                pick_piece(self.cell_list, self.pieces_set, self.depth)

    def computer_move(self) -> None:
        """
        Finds the best move for the computer and plays it
        :return:    None
        """
        i, j = minimax(self.cell_list, self.pieces_bar.selected, self.pieces_set, self.depth)
        self.insert(self.cell_list[i][j], self.current_player)
        Logger.debug('Application: Computer placed {} at {}'.format(self.pieces_bar, (i, j)))
        self.change_player()

    def insert(self, cell: Cell, piece: Piece) -> None:
        """
        :param cell:    The cell to insert into
        :param piece:   The piece to insert
        :return:        None
        """
        ...

    def end_message(self, message: str) -> None:
        """
        Generates the end of game popup and displays it
        :param message: The message to display in the popup
        :return:        None
        """
        self.disabled = True
        self.popup = Popup(title="Game Over!",
                           content=self.generate_popup_contents(message),
                           size_hint=(0.625, 0.625),
                           auto_dismiss=False
                           )
        self.popup.open()

    def generate_popup_contents(self) -> BoxLayout:
        """
        Generates the contents for the end game popup
        :return:    The contents of the popup
        """
        ...

    def reset(self) -> None:
        """
        Starts a new game
        :return:    None
        """
        ...

    def change_player(self) -> None:
        """
        Switches the current player
        :return:        None
        """
        self.current_player = Player.COMPUTER if self.current_player != Player.COMPUTER else Player.HUMAN

    def on_click(self, touch) -> None:
        """
        The function that runs when a cell in the board is clicked
        If no piece is selected: Do nothing
        Else: Insert's the selected piece into the cell and runs the computer's turn
        :param touch:   The cell that was clicked
        :return:        None
        """
        if self.pieces_bar.selected is not None:
            game_over = self.insert(touch, self.pieces_bar.selected)
            self.pieces_bar.remove_widget(self.pieces_bar.selected)
            self.pieces_bar.selected = None
            if not game_over:
                self.change_player()
                if self.game_mode == GameMode.SINGLE_PLAYER:
                    self.computer_move()


class PiecesBar(BoxLayout):
    """
    Class PiecesBar(BoxLayout):
    ---------------------------

    The bar containing all playable pieces. Is displayed underneath the board
    """

    def __init__(self, board: Board, **kwargs) -> None:
        super().__init__(**kwargs)
        self.board = board
        self.board.pieces_bar = self
        self.board.initialise_buttons()
        self.board.first_move()
        self.board.disabled = False
        self.selected = None
        self.widgets = []
        for piece in self.board.pieces_set:
            widget = Cell(piece)
            widget.bind(on_release=self.select)
            self.widgets.append(widget)
            self.add_widget(widget)
        self.confirm_button = Button(text='Confirm')
        self.confirm_button.bind(self.confirm)
        self.add_widget(self.confirm_button)
        Logger.debug("Initialised new PieceBar object.")

    def confirm(self, touch) -> None:
        """
        Confirm's the player's selected piece
        :param touch:   The confirm button
        :return:        None
        """
        ...

    def select(self, touch) -> None:
        """
        Selects a piece
        :param touch:   The piece to select
        :return:        None
        """
        if self.selected is not None:
            self.selected.color = Color.WHITE.value
        self.selected = touch
        touch.color = Color.TINT.value
