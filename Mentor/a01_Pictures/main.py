__version__ = '0.0.27'
#!/usr/bin/kivy

import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint, shuffle
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
#from time import time
from kivy.lib import osc
#from kivy.clock import Clock
from kivy.utils import Platform

kivy.require('1.8.0')
activity_port = 3002
service_port = 3000
platform = Platform()  # ToDo aggiustare riconoscimento piattaforma


class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''
    source = StringProperty(None)


class PicturesApp(App):

    def build(self):
        # the root is created in pictures.kv
        self.root
        self.osc_id = osc.listen(ipAddr='0.0.0.0', port=activity_port)
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('Mentor Service', 'running')
            service.start('service started')
            self.service = service
        # get any files into images directory
        curdir = dirname(__file__)
        list = glob(join(curdir, 'images', '*'))
        Logger.debug("{}".format(list))
        shuffle(list)
        Logger.debug("{}".format(list))
        for filename in list:
            try:
                # load the image
                picture = Picture(source=filename, id=filename, rotation=randint(-30, 30))
                # add to the main field
                self.root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
        osc.init()
        self.last_name = ""
        osc.sendMsg('/say', ["La ap di Michele e' pronta", ], port=service_port)
        return self.root

    def on_pause(self):
        return True

    def on_start(self):
        return True

    def on_stop(self):
        if platform == 'android':
            self.service.stop()

    def tell_picture_name(self, text='Qualcosa'):  # Todo os.path.basename(fileName)
        if self.last_name != text:
            self.last_name = text
            txt = text.split("/")[-1].split('\\')[-1].split('.')[0]
            osc.sendMsg('/say', [txt, ], port=service_port)
            Logger.debug('sent a msg ({}):{}'.format('saysomething', txt))


if __name__ == '__main__':
    PicturesApp().run()

