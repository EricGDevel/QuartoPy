"""
Module screens.py
=================

This module contains all the Screen objects that are used by the ScreenManager in main.py
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from src.board import Board
from src.constants import *

__version__ = '1.0'
__author__ = 'Eric G.D'


class GameScreen(Screen):
    """
    Class GameScreen(Screen)
    ------------------------

    Contains the main game's layout and connects all of the different widgets to each other.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(name=kwargs['name'])
        self.layout = BoxLayout(orientation='vertical')
        self.board = Board(game_mode=kwargs.get('game_mode', GameMode.single_player),
                           first_player=kwargs.get('first_player', Player.computer),
                           difficulty=kwargs.get('difficulty', 'easy'))
        self.pieces_bar = self.board.pieces_bar
        self.layout.add_widget(self.board)
        self.layout.add_widget(self.pieces_bar)
        self.add_widget(self.layout)


class MainMenuScreen(Screen):
    """
    Class MainMenuScreen(Screen)
    ----------------------------

    The main menu screen that allows the user tp navigate to the Play and Settings screens
    """
    pass


class PlayMenuScreen(Screen):
    """
    Class PlayMenuScreen(Screen)
    ----------------------------

    This menu allows the player to select what gamemode they would like to play
    """
    pass
