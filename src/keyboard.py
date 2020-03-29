"""
Module keyboard.py
==================

Contains the implementation of the keyboard object that gets the user's input
"""

from typing import Callable

from kivy.core.window import Window
from kivy.uix.widget import Widget

from src.board import PiecesBar
from src.screens import GameScreen

__version__ = '1.2.1'
__author__ = 'Eric G.D'


class Keyboard(Widget):  # Is a subclass of widget to provide window resizing support
    """
    Class Keyboard(Widget)
    ----------------------

    A wrapper for the kivy keyboard object that provides keyboard controls
    """

    def __init__(self, app: 'QuartoApp', **kwargs) -> None:
        super().__init__(**kwargs)
        self._keyboard: 'Kivy Keyboard' = Window.request_keyboard(self._disable_keyboard, self)
        self._app: 'QuartoApp' = app
        self.callback: Callable[..., None] = lambda *args: self._on_key_down(args[1][1])  # Get pressed key from args
        self._keyboard.bind(on_key_down=self.callback)

    def _on_key_down(self, key: str) -> None:
        """
        This function is called whenever a key is pressed
        :param key:     The key that was pressed
        :return:        None
        """
        if key == 'escape':
            self.toggle_pause_menu()
        pieces_bar = self._app.sm.current_screen.pieces_bar \
            if isinstance(self._app.sm.current_screen, GameScreen) else None
        if isinstance(pieces_bar, PiecesBar) and pieces_bar.confirmed is None:
            Keyboard.__keyboard_select(pieces_bar, key)

    def toggle_pause_menu(self) -> None:
        if self._app.sm.current not in ('sp', 'mp'):
            return
        if not self._app.paused:
            self._app.pause_menu.open()
        else:
            self._app.pause_menu.dismiss()
        self._app.paused = not self._app.paused

    @staticmethod
    def __keyboard_select(pieces_bar: PiecesBar, key: str) -> None:
        """
        Selects or confirms the selected piece based on the key that the player pressed
        :param pieces_bar:  The Piece selection bar of the current screen
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
        self._keyboard.unbind(on_key_down=self.callback)
        self._keyboard = None
