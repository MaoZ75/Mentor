__author__ = 'Maurizio'
__version__ = '0.0.1'

import kivy
kivy.require('1.9.0')
from kivy.app import App

from kivy.utils import Platform
is_android = Platform() == 'android'
is_win = Platform() == 'win'

from kivy.logger import Logger

from kivy.uix.floatlayout import FloatLayout


class LoadDialog(FloatLayout):

    def load(self, path, selection):
        Logger.debug("Ecco: {}{}".format(path, selection))
        pass

    def cancel(self):
        pass


class BaseApp(App):

    def build(self):
        if is_android:
            from android import AndroidService
            service = AndroidService('Mentor Service', 'running')
            service.start('service started')
            self.service = service
        self.root = LoadDialog()
        return self.root

    def on_pause(self):
        return True

    def on_start(self):
        return True

    def on_stop(self):
        if is_android:
            self.service.stop()

if __name__ == '__main__':
    BaseApp().run()
