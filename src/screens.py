"""
Module screens.py
=================

This module contains all the Screen objects and the widgets that they use,
that are in turn used by the App's ScreenManager
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from src.board import Board

__version__ = '1.3'
__author__ = 'Eric G.D'


class GameScreen(Screen):
    """
    Class GameScreen(Screen)
    ------------------------

    Contains the main game's layout, including the board and piece selection bar
    """

    def __init__(self, **kwargs):
        super().__init__(name=kwargs['name'])
        self.layout = BoxLayout(orientation='vertical')
        self.board = Board(game_mode=kwargs.get('game_mode'),
                           first_player=kwargs.get('first_player'),
                           difficulty=kwargs.get('difficulty'))
        self.pieces_bar = self.board.pieces_bar
        self.layout.add_widget(self.board)
        self.layout.add_widget(self.pieces_bar)
        self.add_widget(self.layout)


class MainMenuScreen(Screen):
    """
    Class MainMenuScreen(Screen)
    ----------------------------

    The main menu screen that allows the user to navigate to the Play and Settings screens, and exit the program
    """
    pass


class PlayMenuScreen(Screen):
    """
    Class PlayMenuScreen(Screen)
    ----------------------------

    Used to let the player to select what GameMode they would like to play
    """
    pass


class DifficultyMenuScreen(Screen):
    """
    Class DifficultyMenuScreen(Screen)
    ------------------------------

    This menu allows the player to choose the difficulty of their AI opponent
    """
    pass


class MenuLayout(BoxLayout):
    """
    Class MenuLayout(BoxLayout)
    ---------------------------

    Used to contain the contents of the menu screens
    """
    pass


class Instructions(Popup):
    """
    Class Instructions(Popup)
    -------------------------

    A popup that contains the rules of the game
    """

    def __init__(self, src: str, **kwargs):
        super().__init__(**kwargs)
        self.img.source = src


class PauseMenu(Popup):
    """
    Class PauseMenu(Popup)
    ----------------------

    A popup that allows the player to go to the main menu or restart
    """
    pass


class BackButton(Button):
    """
    Class BackButton(Button)
    ------------------------

    Moves back one screen when pressed
    """
    pass


class DifficultyButton(Button):
    """
    Class DifficultyButton(Button)
    ------------------------------

    Selects the game's difficulty when pressed
    """
    pass
