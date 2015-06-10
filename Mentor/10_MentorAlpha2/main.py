__author__ = 'Maurizio'
__version__ = '0.0.70'

import kivy
kivy.require('1.9.0')
from kivy.app import App
import mentor_lib
from kivy.uix.button import Button
#from kivy.clock import Clock
from functools import partial
from kivy.logger import Logger




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
        #Clock.schedule_interval(self.timed_ops, .1)
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
            type = largs[1]
            msg = largs[0]
        else: # Sending default OSC
            type = self.sequences.current_osc_message[1]
            msg = self.sequences.current_osc_message[0]
        Logger.debug("main.BaseApp.osc_send: sending message'[{}]{}' on port {}".format(type, msg, service_port))
        osc.sendMsg(type, [msg, ], port=service_port)

    #def timed_ops(self, dt):
    #    pass
        #self.osc_send()
        #osc.readQueue(self.osc_id)
        #self.speak_service()


if __name__ == '__main__':
    BaseApp().run()
