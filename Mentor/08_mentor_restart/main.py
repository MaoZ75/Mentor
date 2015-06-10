__author__ = 'Maurizio'
__version__ = '0.0.70'

import kivy
kivy.require('1.9.0')
from kivy.app import App
import mentor_lib
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial



from kivy.utils import Platform
is_android = Platform() == 'android'
is_win = Platform() == 'win'

activity_port = 3002
service_port = 3000


class BaseApp(App):

    def build(self):
        self.icon = 'images/ic_launcher.png'
        if is_android:
            from android import AndroidService
            service = AndroidService('Mentor Service', 'running')
            service.start('service started')
            self.service = service
        self.sequences = mentor_lib.Sequences()
        self.sequences.load_sequences()
        for title in self.sequences.titles:
            btn = Button(text=title, shorten=True, text_size=(200,None))#, size_hint_y=None, height=40)
            btn.bind(on_press=partial(self.sequences.start_sequence, title))
            self.root.ids.grid_main.add_widget(btn)
        Clock.schedule_interval(self.timed_ops, .1)

        return self.root

    def on_pause(self):
        return True

    def on_start(self):
        return True

    def on_stop(self):
        if is_android:
            self.service.stop()

    def timed_ops(self, dt):
        pass
        #self.osc_send()
        #osc.readQueue(self.osc_id)
        #self.speak_service()


if __name__ == '__main__':
    BaseApp().run()
