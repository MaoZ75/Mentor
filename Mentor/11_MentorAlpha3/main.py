__author__ = 'Maurizio'
__version__ = '0.0.70'

import kivy
kivy.require('1.9.0')
from kivy.app import App
import mentor_lib
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
from kivy.logger import Logger

# Determine PLatform
from kivy.utils import Platform
is_android = Platform() == 'android'
is_win = Platform() == 'win'

from kivy.lib import osc
activity_port = 3002
service_port = 3000


class BaseApp(App):

    def build(self):
        self.osc_id = osc.listen(ipAddr='0.0.0.0', port=activity_port)
        osc.init()
        osc.bind(self.osc_id, self.msg_from_server, '/msg')
        osc.bind(self.osc_id, self.write_cockpit, '/osd')
        #osc.bind(self.osc_id, self.root.write_cockpit, '/osd')
        self.icon = 'images/ic_launcher.png'
        if is_android:
            from android import AndroidService
            service = AndroidService('Mentor Service', 'running')
            service.start('service started')
            self.service = service()
        self.sequences = mentor_lib.Sequences(Platform())
        self.sequences.load_sequences()
        for title in self.sequences.titles:
            btn = Button(text=title, shorten=True, text_size=(200, None))  #, size_hint_y=None, height=40)
            btn.bind(on_press=partial(self.sequences.get_osc_message_from_title, title))
            self.root.ids.grid_main.add_widget(btn)
        Clock.schedule_interval(self.timed_ops, .1)


        return self.root

    @staticmethod
    def msg_from_server(self, message, *args):
       Logger.debug("main.BaseApp.msg_from_server: Incoming message: '{}'".format(message[2]))

    def on_pause(self):
        return True

    def on_start(self):
        return True

    def on_stop(self):
        if is_android:
            self.sequences.service.stop()

    def osc_send(self, *largs):
        if len(largs) == 2:
            msg_type = largs[1]
            msg = largs[0]
        else:  # Sending default OSC
            msg_type = self.sequences.current_osc_message[1]
            msg = [self.sequences.current_osc_message[0]]
        Logger.debug("main.BaseApp.osc_send: sending message'[{}]{}' on port {}".format(msg_type, msg, service_port))
        osc.sendMsg(msg_type, msg, port=service_port)

    def write_cockpit(self, message, *args):
        if False:
            Logger.debug("Here the message -{}-".format(message))
        else:
            #for i in range:
                #if message[i] != old[i]:
                    #message[i] = old[i]
                    #update_the_cockpit_value
            #Logger.debug("write_cockpit: {}\nArgs{}".format(message[2], args))
            Logger.debug("Here the message -{}-".format(message))
            partial, total, img, label, text, actual_step, total_steps = message[2:]
            self.root.ids.partial_left.text = partial
            self.root.ids.total_left.text = total
            if self.root.ids.img_bk.source != img:
                self.root.ids.img_bk.source = img
            self.root.ids.log.text = label

    def write_timer(self, message, *args):
        self.root.ids.current_minute, self.root.ids.current_second, self.root.ids.current_exercise, current_repetition \
            = message[2].split('\t', 4)

    def timed_ops(self, dt):
        osc.readQueue(self.osc_id)

if __name__ == '__main__':
    BaseApp().run()
