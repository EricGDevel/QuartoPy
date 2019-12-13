"""
Module screens.py
=================

This module contains all the Screen objects that are used by the ScreenManager in main.py
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from src.board import Board, PiecesBar
from src.constants import *


class GameScreen(Screen):
    """
    Class GameScreen(Screen)
    ------------------------

    Contains the main game's layout and connects all of the different widgets to each other.
    """
    def __init__(self, **kwargs):
        super().init(name=kwargs['name'])
        self.layout = BoxLayout(orientation='horizontal')
        self.board = Board(game_mode=kwargs.get('game_mode', GameMode.SINGLE_PLAYER),
                           first_player=kwargs.get('first_player', Player.HUMAN),
                           difficulty=kwargs.get('difficulty', 'hard'))
        self.pieces_bar = PiecesBar(self.board, size_hint=(1, 0.1))
        self.layout.add_widget(self.board)
        self.layout.add_widget(self.pieces_bar)
        self.add_widget(self.layout)


class MainMenuScreen(Screen):
    """
    Class MainMenuScreen(Screen)
    ----------------------------

    """
    pass


class PlayMenuScreen(Screen):
    pass


class SettingsMenuScreen(Screen):
    pass
