__version__ = '0.0.67'

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lib import osc
from kivy.utils import Platform
from time import time
from mentor_widget import MentorWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.logger import Logger
from kivy.properties import StringProperty
import mentor_lib

kivy.require('1.9.0')

activity_port = 3002
service_port = 3000

t0 = time()
platform = Platform()  # ToDo aggiustare riconoscimento piattaforma
debug = True


def elapsed_seconds():
    return int(time() - t0)


class MentorBaseApp(App):

    def build(self):
        """config = ConfigParser()
        config.read('conf.ini')
        self.config = Settings()
        # s.add_json_panel('My custom panel', config, 'settings_custom.json')"""
        self.icon = 'images/ic_launcher.png'
        self.osc_activities = []
        self.speechs = []
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
        self.sequences = mentor_lib.Sequences()
        self.sequences.load_sequences()
        self.root = MentorWidget()
        text_input = TextInput(text=self.timer_value, font_size=40, multiline=False)  #, size_hint=(None, None))  # font_size=20,
        text_input.foreground_color = [1, 1, 1, 1]
        text_input.background_color = [0, 0, 0, 0]
        text_input.shorten_from = 'center'
        #text_input.center_x = True
        #text_input.center_y = True
        text_input.bind(text=self.on_text_input_text)
        self.root.ids.grid_main.add_widget(text_input)
        btn = Button(text="Custom Timer")  #, size_hint_y=None, height=40)
        #btn.height = text_input.content_height
        btn.bind(on_press=partial(self.start_sequence, "timer"))
        self.root.ids.grid_main.add_widget(btn)
        for title in self.sequences.titles:
            btn = Button(text=title)#, size_hint_y=None, height=40)
            btn.bind(on_press=partial(self.start_sequence, title))
            self.root.ids.grid_main.add_widget(btn)
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
        Clock.schedule_interval(self.timed_ops, .1)
        return self.root

    def timed_ops(self, dt):
        self.osc_send()
        osc.readQueue(self.osc_id)
        #self.speak_service()

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

    def osc_send(self):
        if len(self.osc_activities) > 0:
            msg, reg_type = self.osc_activities.pop(0)
            if debug:
                print "sending {}({}) [{} messages in queue]".format(msg, reg_type, len(self.osc_activities))
            osc.sendMsg(reg_type, [msg, ], port=service_port)

    def osc_push_message(self, message='idle', reg_type='/msg', Doubles=False):
        if Doubles:
            self.osc_activities.append([message, reg_type])
        elif self.osc_activities.count([message, reg_type]) == 0:
                self.osc_activities.append([message, reg_type])

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

    def start_sequence(self, *args, **kwargs):  #sequence_name):
        try:
            if args[0] == 'timer':  # args[0] is the Title
                #print self.root.ids.tx_timer
                Logger.debug("Time goes: {}".format(self.timer_value))
                self.osc_push_message(self.timer_value, "/tmr")
            else:
                sequence_file_name = self.sequences.file_name_for_title(args[0])  # args[0] is the Title
                #print('The flexible function has *args of', str(args), "and **kwargs of", str(kwargs))
                self.osc_push_message(sequence_file_name, "/nsq")
            self.root.ids.sm.transition = SlideTransition(direction="left")
            self.root.ids.sm.current = 'mentorplayer'  # self.root.ids.sm.next()
        except ValueError:
            Logger.debug("ValueError on start_sequence: no worry if you see me only at beginning")

if __name__ == '__main__':
    MentorBaseApp().run()
