"""
Module main.py
==============

This module contains the main application and it's configuration
"""

__version__ = '0.0'
__author__ = 'Eric G.D'

import os

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from src.screens import *

kivy.require('1.11.0')


class QuartoApp(App):
    """
    Class QuartoApp(App):
    ---------------------

    This is an extension of the app class, used to start the Kivy program
    """

    __sm = None
    CONFIG_FILE = 'kivy_config.ini'

    @staticmethod
    def get_screen_manager() -> ScreenManager:
        """
        Initialises the program's ScreenManger and returns it
        :return:    QuartoApp.__sm
        """
        if QuartoApp.__sm is None:
            QuartoApp.__sm = ScreenManager(transition=SlideTransition())
            QuartoApp.__sm.add_widget(MainMenuScreen(name='menu'))
            QuartoApp.__sm.add_widget(PlayMenuScreen(name='play'))
            QuartoApp.__sm.add_widget(SettingsMenuScreen(name='settings'))
            QuartoApp.__sm.add_widget(GameScreen(name='sp', game_mode=GameMode.SINGLE_PLAYER))
            QuartoApp.__sm.add_widget(GameScreen(name='mp', game_mode=GameMode.MULTI_PLAYER))
            Logger.debug("Setup: QuartoApp.__sm generated.")
        return QuartoApp.__sm

    @staticmethod
    def set_cwd() -> None:
        """
        Sets the current working directory to this file's directory
        In addition, it set's this window's icon
        :return:    None
        """
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        Config.set('kivy', 'window_icon', os.path.join('assets', 'icon.png'))

    @staticmethod
    def setup_logging() -> None:
        """
        Sets up the program's logger
        :return:    None
        """
        Config.set('kivy', 'log_maxfiles', 10)
        Config.set('kivy', 'log_name', "quarto_log_%y-%m-%d_%_.txt")
        Config.set('kivy', 'log_dir', os.getcwd())
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
        QuartoApp.setup_logging()
        if not config_exists:
            Config.set('kivy', 'exit_on_escape', 1)
            Config.set('graphics', 'full_screen', 'auto')
        Config.write()
        Logger.debug("Setup: Config generated.")
        self.title = 'Quarto'

    def build(self) -> ScreenManager:
        """
        Starts the program
        :return:    None
        """
        self.set_config()
        return QuartoApp.get_screen_manager()


if __name__ == '__main__':
    QuartoApp().run()
