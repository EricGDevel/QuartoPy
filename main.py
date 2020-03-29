"""
Module main.py
==============

This module contains the source code of the main kivy app and it's runtime code
"""

__version__ = '1.2'
__author__ = 'Eric G.D'

import os

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from src.keyboard import Keyboard
from src.screens import *

kivy.require('1.11.0')


class QuartoApp(App):
    """
    Class QuartoApp(App):
    ---------------------

    This is an extension of the app class, used to start the Kivy program
    Contains the runtime code of the application
    """

    sm: ScreenManager = None
    keyboard: Keyboard = None
    instructions: Instructions = None
    pause_menu: PauseMenu = None
    paused: bool = False
    CONFIG_FILE: str = 'kivy_config.ini'

    @staticmethod
    def get_screen_manager() -> ScreenManager:
        """
        Initialises the program's ScreenManger and returns it
        :return:    A reference to QuartoApp.sm
        """
        if QuartoApp.sm is None:
            QuartoApp.sm = ScreenManager(transition=SlideTransition())
            QuartoApp.sm.add_widget(MainMenuScreen(name='menu'))
            QuartoApp.sm.add_widget(PlayMenuScreen(name='play'))
            QuartoApp.sm.add_widget(DifficultyMenuScreen(name='diff'))
            QuartoApp.sm.add_widget(GameScreen(name='sp', game_mode=GameMode.single_player))
            QuartoApp.sm.add_widget(GameScreen(name='mp', game_mode=GameMode.multi_player))
        return QuartoApp.sm

    @staticmethod
    def setup_instructions() -> Instructions:
        """
        Initialises the programs Instructions popup and returns it
        :return:    A reference to QuartoApp.instructions
        """
        if QuartoApp.instructions is None:
            QuartoApp.instructions = Instructions(os.path.join('assets', 'instructions.jpg'))
        return QuartoApp.instructions

    @staticmethod
    def setup_pause_menu() -> PauseMenu:
        """
        Initialises the programs Pause Menu Popup and returns it
        :return:    A reference to QuartoApp.pause_menu
        """
        if QuartoApp.pause_menu is None:
            QuartoApp.pause_menu = PauseMenu()
            QuartoApp.paused = False
        return QuartoApp.pause_menu

    @staticmethod
    def set_cwd() -> None:
        """
        Sets the current working directory to this file's (main.py) base folder
        :return:    None
        """
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)

    @staticmethod
    def setup_logging() -> None:
        """
        Sets up the program's logger
        :return:    None
        """
        Config.set('kivy', 'log_name', "quarto_log_%y-%m-%d_%_.txt")
        Config.set('kivy', 'log_dir', os.path.join(os.getcwd(), 'logs'))
        Config.set('kivy', 'log_maxfiles', 10)
        Config.set('kivy', 'log_level', 'info')
        Config.set('kivy', 'log_enable', 1)

    def set_config(self) -> None:
        """
        Configures the program
        :return:    None
        """
        QuartoApp.set_cwd()
        config_exists = os.path.isfile(QuartoApp.CONFIG_FILE)
        Config.read(QuartoApp.CONFIG_FILE)
        if not config_exists:
            # QuartoApp.setup_logging()
            Config.set('kivy', 'exit_on_escape', 0)
            Config.set('graphics', 'fullscreen', 0)
            # Logger.debug("Setup: Config updated.")
        Config.write()
        self.title = 'Quarto'
        self.icon = os.path.join('assets', 'icon.png')

    def build(self) -> ScreenManager:
        """
        Builds an instance of QuaroApp and starts the main program
        Called by QuartoApp.run()
        :return:    The application's ScreenManager, used as the base widget for the window
        """
        self.set_config()
        QuartoApp.setup_instructions()
        QuartoApp.setup_pause_menu()
        QuartoApp.keyboard = Keyboard(self)
        return QuartoApp.get_screen_manager()


if __name__ == '__main__':
    QuartoApp().run()
