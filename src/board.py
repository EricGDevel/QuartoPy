"""
Module board.py
===============

This module contains the Board and PieceBar objects that are used by GameScreen
Note: Board contains all game functions that don't relate to AI
"""

__all__ = ['Board', 'PiecesBar']
__version__ = '1.0'
__author__ = 'Eric G.D'

from copy import deepcopy
from math import inf
from typing import List, Set, Union

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from src.constants import *
from src.ai import *
from src.piece import *


class Board(GridLayout):
    """
    Class Board(GridLayout):
    ------------------------

    Represents the main game board where pieces are inserted.
    In addition, it contains most of the main program's code
    """

    LENGTH = 4
    DIFFICULTY = {'baby': 0, 'easy': 2, 'medium': 4,
                  'hard': 6, 'impossible': LENGTH ** 2}
    popup = None

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.rows = self.cols = Board.LENGTH
        self.first_player = self.current_player = kwargs.get('first_player', Player.computer)
        self.game_mode = kwargs.get('game_mode', GameMode.single_player)
        self.depth = Board.DIFFICULTY[kwargs.get('difficulty', 'hard')]
        self.cell_list = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.pieces_bar = PiecesBar(self)
        self.initialise_buttons()
        self.first_move()

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
        if self.game_mode == GameMode.single_player and self.first_player == Player.computer:
            piece = pick_starting_piece(self.pieces_bar.pieces_set)
            self.pieces_bar.confirm(piece)

    def computer_move(self) -> None:
        """
        Finds the best move for the computer and plays it
        :return:    None
        """
        option = self.minimax()
        i, j = option.index
        self.insert_confirmed(self.cell_list[i][j])
        self.pieces_bar.confirm(option.piece)
        # Logger.info('Application: Computer placed {} at {}'.format(self.pieces_bar, option.index))

    def get_turn_num(self) -> int:
        return (Piece.MAX_NUM + 1) - (len(self.pieces_bar) - 1)

    def minimax(self):
        """
        Calculates the next move by evaluating the possible moves and playing as both sides
        :return: The best move for the board
        """
        board = self.convert()
        max_player = self.current_player == Player.computer
        depth = Board.DIFFICULTY['baby'] if self.get_turn_num() < 5 else self.depth
        piece = self.pieces_bar.confirmed.piece
        pieces_set = deepcopy(self.pieces_bar.pieces_set)
        if depth <= 0:
            return pick_best(board, piece, pieces_set, max_player)
        return make_move(board, max_player, piece, pieces_set, -inf, inf, depth, depth)

    def on_click(self, touch) -> None:
        """
        The function that runs when a cell in the board is clicked
        If no piece is selected: Do nothing
        Else: Insert's the selected piece into the cell and runs the computer's turn
        :param touch:   The cell that was clicked
        :return:        None
        """
        if self.pieces_bar.confirmed is not None:
            game_over = self.insert_confirmed(touch)
            if game_over:
                self.disabled = True
                self.pieces_bar.disabled = True

    def insert(self, cell: Cell, piece: Piece) -> bool:
        """
        :param cell:    The cell to insert into
        :param piece:   The piece to insert
        :return:        If the game has ended or not
        """
        cell.piece = piece
        cell.unbind(on_release=self.on_click)
        converted = self.convert()
        is_full = self.is_full()
        winning_move = has_won(converted)
        game_over = is_full or winning_move
        if game_over:
            message = '{} wins!'.format(self.get_current_player_str()) if winning_move else "It's a tie!"
            self.end_message(message)
        return game_over

    def get_current_player_str(self) -> str:
        if self.game_mode == GameMode.single_player:
            return self.current_player.name.title()
        player_num = 1 if self.current_player == self.first_player else 2
        return f'Player {player_num}'

    def insert_confirmed(self, cell: Cell) -> bool:
        """
        Inserts the selected piece into cell
        :param cell:    The cell to insert into
        :return:        If the game has ended or not
        """
        assert self.pieces_bar.confirmed is not None
        piece = self.pieces_bar.confirmed.piece
        self.pieces_bar.remove_confirmed()
        return self.insert(cell, piece)

    def end_message(self, message: str) -> None:
        """
        Generates the end of game popup and displays it
        :param message: The message to display in the popup
        :return:        None
        """
        self.disabled = True
        if self.popup is None:
            self.popup = EndMessage()
        self.popup.ids.message.text = message
        self.popup.open()

    def reset(self) -> None:
        """
        Starts a new game
        :return:    None
        """
        if self.popup is not None:
            self.popup.dismiss()
        self.disabled = False
        self.initialise_buttons(reset=True)
        self.first_player = self.current_player = (~self.first_player)
        self.pieces_bar.reset()
        self.first_move()

    def change_player(self) -> None:
        """
        Switches the current player
        :return:        None
        """
        self.current_player = (~self.current_player)  # Method defined in Player.__invert__()

    def is_full(self) -> bool:
        """
        :return:    If the board is full
        """
        return len(self.pieces_bar) == 0

    def convert(self) -> List[List[Piece]]:
        """
        :return:                A simplified version of board
        """
        return [[cell.piece for cell in row] for row in self.cell_list]


class PiecesBar(BoxLayout):
    """
    Class PiecesBar(BoxLayout):
    ---------------------------

    The bar containing all playable pieces. Is displayed underneath the board
    """

    @staticmethod
    def generate_pieces_set() -> Set[Piece]:
        """
        Generates a set of all playable pieces
        :return:    The generated set
        """
        return {Piece(num) for num in range(Board.LENGTH ** 2)}

    def __init__(self, board: Board, **kwargs) -> None:
        super().__init__(**kwargs)
        if not isinstance(board, Board):
            raise ValueError(f':board: needs to be a Board object, not {type(board)}!')
        self.board = board
        self.selected = None
        self.confirmed = None
        self.pieces_set = PiecesBar.generate_pieces_set()
        self.widgets = []
        self.add_pieces()
        self.confirm_button = Button(text='Confirm', size_hint_x=None)
        self.confirm_button.bind(on_release=self.confirm)
        self.add_widget(self.confirm_button)

    def add_pieces(self):
        for piece in self.pieces_set:
            widget = Cell(piece)
            widget.bind(on_release=self.select)
            self.widgets.append(widget)
            self.add_widget(widget)

    def confirm(self, touch: Union[Piece, Cell]) -> None:
        """
        Confirm's the player's selected piece
        :param touch:   The confirm button
        :return:        None
        """
        confirmed = False
        if isinstance(touch, Piece):
            assert self.confirmed is None and self.selected is None
            self.confirmed = next((cell for cell in self.widgets if cell.piece == touch), None)
            if self.confirmed is None:
                raise ValueError('Invalid piece to confirm.')
            confirmed = True
        else:
            if self.selected is not None and self.confirmed is None:
                self.confirmed = self.selected
                self.selected = None
                confirmed = True
        if confirmed:
            self.pieces_set.remove(self.confirmed.piece)
            self.confirmed.color = Color.CONFIRMED_TINT.value
            self.board.change_player()
            if self.board.game_mode == GameMode.single_player and self.board.current_player == Player.computer:
                self.board.computer_move()

    def remove_confirmed(self):
        assert self.confirmed is not None
        self.widgets.remove(self.confirmed)
        self.remove_widget(self.confirmed)
        self.confirmed = None

    def select(self, touch) -> None:
        """
        Selects a piece
        :param touch:   The piece to select
        :return:        None
        """
        if self.confirmed is None:
            if self.selected is not None:
                self.selected.color = Color.WHITE.value
            self.selected = touch
            touch.color = Color.SELECTED_TINT.value

    def clear_all(self):
        while len(self.widgets) > 0:
            self.remove_widget(self.widgets[0])
            del self.widgets[0]
        self.confirmed = None
        self.selected = None

    def reset(self) -> None:
        self.remove_widget(self.confirm_button)
        self.clear_all()
        self.pieces_set = PiecesBar.generate_pieces_set()
        self.add_pieces()
        self.add_widget(self.confirm_button)
        self.disabled = False

    def __len__(self):
        return len(self.widgets)


class EndMessage(Popup):
    pass
