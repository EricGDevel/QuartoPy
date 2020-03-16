"""
Module main.py
==============

This module contains the main application and it's configuration
"""

__version__ = '1.1'
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
    """

    sm = None
    keyboard = None
    instructions = None
    CONFIG_FILE = 'kivy_config.ini'

    @staticmethod
    def get_screen_manager() -> ScreenManager:
        """
        Initialises the program's ScreenManger and returns it
        :return:    QuartoApp.sm
        """
        if QuartoApp.sm is None:
            QuartoApp.sm = ScreenManager(transition=SlideTransition())
            QuartoApp.sm.add_widget(MainMenuScreen(name='menu'))
            QuartoApp.sm.add_widget(PlayMenuScreen(name='play'))
            QuartoApp.sm.add_widget(DifficultyMenuScreen(name='diff'))
            # TODO: Remove redundant extra screen and have the screen get the game mode when the mode button is pressed
            QuartoApp.sm.add_widget(GameScreen(name='sp', game_mode=GameMode.single_player))
            QuartoApp.sm.add_widget(GameScreen(name='mp', game_mode=GameMode.multi_player))
        return QuartoApp.sm

    @staticmethod
    def setup_instructions() -> Instructions:
        if QuartoApp.instructions is None:
            QuartoApp.instructions = Instructions()
            QuartoApp.instructions.ids['img'].source = os.path.join('assets', 'instructions.jpg')
        return QuartoApp.instructions

    @staticmethod
    def set_cwd() -> None:
        """
        Sets the current working directory to this file's directory
        In addition, it set's this window's icon
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
        # TODO: Fix logging bugs (Multiple log files per run, not saving to logs/ folder)
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
        Starts the program
        :return:    The application's ScreenManager
        """
        self.set_config()
        QuartoApp.setup_instructions()
        QuartoApp.keyboard = Keyboard(self)
        return QuartoApp.get_screen_manager()


if __name__ == '__main__':
    QuartoApp().run()
