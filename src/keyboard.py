"""
Module keyboard.py
==================

Contains the implementation of the keyboard object that gets the user's input
"""

import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from src.board import PiecesBar
from src.screens import GameScreen

__version__ = '1.1'
__author__ = 'Eric G.D'


class Keyboard(Widget):
    """
    Class Keyboard(Widget)
    ----------------------

    A keyboard object that allows the user to control some of the game with the keyboard
    """

    def __init__(self, app: App, **kwargs) -> None:
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._disable_keyboard, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._app = app

    def _on_key_down(self, keyboard, keycode, text, modifiers) -> None:
        key = keycode[1]
        if key == 'escape':
            sys.exit(0)
        pieces_bar = self._app.sm.current_screen.pieces_bar \
            if isinstance(self._app.sm.current_screen, GameScreen) else None
        if isinstance(pieces_bar, PiecesBar) and pieces_bar.confirmed is None:
            Keyboard.__keyboard_select(pieces_bar, key)

    @staticmethod
    def __keyboard_select(pieces_bar: PiecesBar, key: str) -> None:
        """
        Selects or confirms the selected piece based on the key that the player pressed
        :param pieces_bar:  The PiecesBar object of the current game
        :param key:         The key that was pressed
        :return:            None
        """
        if key in ('left', 'right'):
            selected_index = pieces_bar.widgets.index(pieces_bar.selected) \
                if pieces_bar.selected is not None else 0
            relative_widget_index = 1 if key == 'right' else -1
            relative_widget_index = 0 if pieces_bar.selected is None and key == 'right' else relative_widget_index
            index = (selected_index + relative_widget_index) % len(pieces_bar.widgets)
            pieces_bar.select(pieces_bar.widgets[index])
        elif key == 'enter' and pieces_bar.selected is not None:
            pieces_bar.confirm()

    def _disable_keyboard(self) -> None:
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
