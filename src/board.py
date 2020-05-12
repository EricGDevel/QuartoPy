"""
Module board.py
===============

This module contains the Board and PieceBar objects that are used by GameScreen
Note: Board contains all game functions that don't relate to AI
"""

__version__ = '1.3'
__author__ = 'Eric G.D'

import threading
from copy import deepcopy
from math import inf
from typing import Dict, List, Set, Union

from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from src.ai import *
from src.constants import *
from src.option import GameState, Option
from src.piece import *


class Message(Popup):
    pass


class Board(GridLayout):
    """
    Class Board(GridLayout):
    ------------------------

    The main game board where pieces are inserted.
    This class contains most of the main program's code.
    """

    LENGTH: int = 4
    DIFFICULTY: Dict[str, int] = {'baby': 0, 'easy': 1, 'medium': 3, 'hard': 5,
                                  'very hard': 7, 'expert': 9, 'impossible': 11,
                                  'max': LENGTH ** 2}  # Bottom rows for debugging
    end_message: Message = None

    def __init__(self, **kwargs):
        super().__init__()
        self.rows = self.cols = Board.LENGTH
        self.first_player: Player = kwargs.get('first_player', Player.computer)
        self.current_player: Player = self.first_player
        self.game_mode: GameMode = kwargs.get('game_mode', GameMode.single_player)
        difficulty = kwargs.get('difficulty')
        self.depth: int = Board.DIFFICULTY.get(difficulty, 'medium')
        self.turn_num: int = 1
        self.cell_list: List[List[Cell]] = self.generate_cell_list()
        self.pieces_bar: PiecesBar = PiecesBar(self)
        self.initialise_buttons()

    def generate_cell_list(self) -> List[List[Cell]]:
        """
        :return:    A 2D List containing the board's cells
        """
        return [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    def set_difficulty(self, key: str) -> None:
        """
        Changes the depth limit used by the AI
        :param key:     The key used to get the depth level
        :return:        None
        """
        self.depth = Board.DIFFICULTY.get(key, self.depth)

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
        If Human is the first player: Ask the computer to pick a piece for the player to play.
        If Computer is the first player: Does nothing and waits for player to select piece (Through PiecesBar.confirm)
        MULTI_PLAYER: Does nothing and waits for the first player to take their turn (Through on_click)
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
        self.disabled = True
        option = self.negamax()
        i, j = option.index
        self.insert_confirmed(self.cell_list[i][j])
        self.pieces_bar.confirm(option.piece)
        self.disabled = False
        # Logger.info('Application: Computer placed {} at {}'.format(self.pieces_bar, option.index))

    def negamax(self) -> Option:
        """
        Calculates the next move by evaluating the possible moves and playing as both sides

        :return:        The best move for the board

        .. seealso::    https://www.chessprogramming.org/Minimax\n
                        https://en.wikipedia.org/wiki/Minimax\n
                        https://www.chessprogramming.org/Negamax\n
                        https://en.wikipedia.org/wiki/Negamax
        """
        board = self.convert()
        piece = self.pieces_bar.confirmed.piece
        pieces_set = self.pieces_bar.pieces_set
        depth = Board.DIFFICULTY['baby'] if self.turn_num < 5 else self.depth
        if depth <= 0:
            return pick_best(board, piece, deepcopy(pieces_set))
        sign = 1 if self.current_player == Player.computer else -1
        return iterative_deepening(board, piece, pieces_set, sign, -inf, inf, depth)

    def on_click(self, touch) -> None:
        """
        The function that runs when a cell in the board is clicked
        If a piece hasn't been confirmed: Do nothing
        Otherwise: Inserts the confirmed piece into the cell and runs the computer's turn
        :param touch:   The cell that was clicked
        :return:        None
        """
        if self.pieces_bar.confirmed is not None:
            self.insert_confirmed(touch)

    def insert(self, cell: Cell, piece: Piece) -> bool:
        """
        :param cell:    The cell to insert into
        :param piece:   The piece to insert
        :return:        If the game has ended or not
        """
        cell.piece = piece
        cell.unbind(on_release=self.on_click)
        self.turn_num += 1
        winning_move = has_won(self.convert())
        game_over = self.is_full() or winning_move
        if game_over:
            message = f'{self.get_current_player_str()} wins!' if winning_move else "It's a tie!"
            self.game_over(message)
        return game_over

    def get_current_player_str(self) -> str:
        """
        If SinglePlayer: Returns the name of the enum value
        If MultiPlayer: Returns the player's number
        :return:    A string representation of the current player
        """
        if self.game_mode == GameMode.single_player:
            return self.current_player.name.title()
        player_num = 1 if self.current_player == self.first_player else 2
        return f'Player {player_num}'

    @mainthread
    def insert_confirmed(self, cell: Cell) -> bool:
        """
        Inserts the selected piece into cell
        :param cell:    The cell to insert into
        :return:        If the game has ended or not
        """
        if self.pieces_bar.confirmed is None:
            raise TypeError('Please confirm a piece before inserting!')
        piece = self.pieces_bar.confirmed.piece
        self.pieces_bar.remove_confirmed()
        return self.insert(cell, piece)

    def game_over(self, message: str) -> None:
        """
        Generates the end of game popup and displays it
        :param message: The message to display in the popup
        :return:        None
        """
        if self.end_message is None:
            self.end_message = Message()
        self.end_message.message.text = message
        self.end_message.open()

    def reset(self) -> None:
        """
        Starts a new game
        :return:    None
        """
        if self.end_message is not None:
            self.end_message.dismiss()
        self.initialise_buttons(reset=True)
        self.current_player = self.first_player
        self.turn_num = 1
        self.pieces_bar.reset()
        GameState.transposition_table.clear()
        self.first_move()

    def is_full(self) -> bool:
        """
        :return:    If the board is full
        """
        return len(self.pieces_bar) == 0

    def convert(self) -> GameState:
        """
        :return:                A simplified version of board
        """
        return GameState([[cell.piece for cell in row] for row in self.cell_list])


class PiecesBar(BoxLayout):
    """
    Class PiecesBar(BoxLayout):
    ---------------------------

    The bar containing all playable pieces. Is displayed underneath the board
    """

    def __init__(self, board: Board, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(board, Board):
            raise ValueError(f':board: needs to be a Board object, not {type(board)}!')
        self.board: Board = board
        self.selected: Union[None, Cell] = None
        self.confirmed: Union[None, Cell] = None
        self.pieces_set: Set[Piece] = PiecesBar.generate_pieces_set()
        self.widgets: List[Cell] = []
        self.add_pieces()
        self.confirm_button: Button = Button(text='Confirm', size_hint_x=None)
        self.confirm_button.bind(on_release=lambda *args: self.confirm())
        self.add_widget(self.confirm_button)
        Window.bind(on_resize=lambda *args: self.reselect())

    def __len__(self) -> int:
        return len(self.widgets)

    @staticmethod
    def generate_pieces_set() -> Set[Piece]:
        """
        Generates a set of all playable pieces
        :return:    The generated set
        """
        return {Piece(num) for num in range(Piece.MAX_NUM + 1)}

    def add_pieces(self) -> None:
        """
        Adds all the pieces in :self.pieces_set: to the layout
        :return:    None
        """
        for piece in self.pieces_set:
            widget = Cell(piece)
            widget.bind(on_release=self.select)
            self.add_widget(widget, -piece.id)  # Inserts the widget based on id number in ascending order
            self.widgets.append(widget)

    @mainthread
    def confirm(self, piece: Piece = None) -> None:
        """
        Confirm's the player's selected piece
        :param piece:   The confirm button
        :return:        None
        """
        if self.confirmed is not None:
            return
        if piece is None:  # Player selected a piece using keyboard or confirm button
            if self.selected is None:
                raise ValueError('Cannot confirm piece as a piece has not been selected.')
            self.confirmed = self.selected
        else:  # Touch is a piece (function was called from insert)
            self.confirmed = self.get_cell_from_piece(piece)
        self.confirmed.set_background_color(Colors.confirmed)
        self.board.current_player = next_player(self.board.current_player)
        self.selected = None
        if self.board.game_mode == GameMode.single_player and self.board.current_player == Player.computer:
            threading.Thread(target=self.board.computer_move).start()
            # Runs AI on separate thread to prevent the application from freezing

    def get_cell_from_piece(self, piece: Piece) -> Cell:
        """
        :param piece:   A piece object
        :return:        The cell object that represents it from self.widgets
        """
        try:
            return next(cell for cell in self.widgets if cell.piece == piece)
        except StopIteration:
            raise ValueError(':piece: is not selectable!.')

    def remove_confirmed(self) -> None:
        """
        Remove the confirmed piece from :self.widgets: and :self.pieces_set:
        :return:    None
        """
        if self.confirmed is None:
            raise TypeError('A piece needs to be confirmed in order to remove it!')
        self.confirmed.canvas.before.clear()
        self.widgets.remove(self.confirmed)
        self.pieces_set.remove(self.confirmed.piece)
        self.remove_widget(self.confirmed)
        self.confirmed = None

    def select(self, touch: Cell) -> None:
        """
        Selects a piece
        :param touch:   The piece to select
        :return:        None
        """
        if self.confirmed is not None:
            return
        if self.selected is not None:
            self.selected.canvas.before.clear()
        self.selected = touch
        touch.set_background_color(Colors.selected)

    def reset(self) -> None:
        """
        Resets the PiecesBar to it's initial state
        :return:    None
        """
        self.clear_widgets()
        self.widgets.clear()
        self.confirmed = None
        self.selected = None
        self.pieces_set = PiecesBar.generate_pieces_set()
        self.add_pieces()
        self.add_widget(self.confirm_button)

    def reselect(self) -> None:
        """
        Redraws the background of selected and confirmed pieces on window resize
        :return:    None
        """
        if self.selected is not None:
            self.selected.set_background_color(Colors.selected)
        elif self.confirmed is not None:
            self.confirmed.set_background_color(Colors.confirmed)
