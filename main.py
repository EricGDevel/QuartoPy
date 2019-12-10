import os
from src.board import Board

import kivy

from kivy.app import App
kivy.require('1.11.0')


class QuartoApp(App):
    """
    Class QuartoApp(App):
    This is an extension of the app class, used to start the kivy program
    """

    @staticmethod
    def set_cwd():
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)

    def set_config(self):
        QuartoApp.set_cwd()
        self.title = 'Quarto'
        self.icon = os.path.join('assets', 'icon.png')

    def build(self):
        self.set_config()
        return Board()


if __name__ == '__main__':
    QuartoApp().run()
