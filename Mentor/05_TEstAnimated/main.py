__author__ = 'Maurizio'
__version__ = '0.0.1'

import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import os.path
import os
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class BaseWidget(GridLayout):
    pass


class BaseApp(App):

    def build(self):
        self.root = BaseWidget()
        self.sources = [f for f in os.listdir(os.curdir) if f[-3:]=='zip']
        self.sources.extend([f for f in os.listdir(os.curdir) if f[-3:]=='png'])
        print(self.sources)
        #img = Image(id='jmp', source='jumping_jacks.zip',
        #    anim_delay=.4, size_hint_y=5)
        #self.root.add_widget(img)
        self.i = 0
        return self.root

    def new_image(self):
        self.i = (self.i + 1) % len(self.sources)
        self.root.ids.jmp.source = self.sources[self.i]

if __name__ == '__main__':
    BaseApp().run()
