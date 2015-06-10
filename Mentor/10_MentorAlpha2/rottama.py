__version__ = '0.0.67'

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import Platform
from mentor_widget import MentorWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.textinput import TextInput
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.logger import Logger
from kivy.properties import StringProperty
import mentor_lib

kivy.require('1.9.0')

from time import time

############################   Time mo

t0 = time()
def elapsed_seconds():
    return int(time() - t0)


class MentorBaseApp(App):

    def build(self):
        self.osc_activities = []
        self.osc_id = osc.listen(ipAddr='0.0.0.0', port=activity_port)
        self.count_requests = 0
        self.timer_value = "40.10.10.1"
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('Mentor Service', 'running')
            service.start('service started')
            self.service = service
            self.folder_music = "/storage/emulated/legacy/Music/PerAttivita"
        elif platform == 'win':
            self.folder_music = "C:\\Mao\\Progetti\\Musica\\MusicaSuNexus\\PerAttivita"
        else:
            self.folder_music = ".\\music"
        Logger.info("Folder music: {}".format(self.folder_music))
        self.root = MentorWidget()
        #if len(self.sequences.titles)%2:
        #    btn = Button(text="_     _", id='pippo')  #, size_hint_y=None, height=40)
        #    self.root.ids.grid_main.add_widget(btn)
        #self.start_sequence_ok = False
        #self.sequence_buttons = []
        #for i in self.sequences.titles:
            #self.sequence_buttons.append(Button(text=str(i)))
            #self.sequence_buttons[-1].bind(on_press=self.start_sequence(str(i)))
            #self.sequence_buttons[-1].bind(on_release=self.start_sequence(str(i)))
            #btn.bind(state=self.start_sequence(str(i)))
            #btn.bind(on_release=self.root.start_sequence(btn.text))
            #self.root.ids.grid_main.add_widget(self.sequence_buttons[-1])
            #self.root.ids.grid_main.add_widget(Button(text=str(i), on_press=self.start_sequence(str(i))))
        #self.start_sequence_ok = True
        osc.init()
        osc.bind(self.osc_id, self.msg_from_server, '/msg')
        osc.bind(self.osc_id, self.root.write_cockpit, '/osd')

        return self.root


    def on_pause(self):
        return True

    def on_start(self):
        return True

    def on_stop(self):
        #osc.sendMsg('/end', ['', ], port=service_port)
        if platform == 'android':
            self.service.stop()

    def on_text_input_text(self, instance, value):
        self.timer_value = value

    @staticmethod
    def msg_from_server(self, message, *args):
        if debug:
            print "Incoming message - \"{}\"".format(message[2])

    def send(self):
        message = "a Message"
        self.osc_push_message(message, '/msg')

    def speak_something(self, message='Test', language='EN'):
        self.count_requests += 1
        self.osc_push_message("1\tTTS_{}\t{}".format(language, message), "/spk")
        pass


if __name__ == '__main__':
    MentorBaseApp().run()
