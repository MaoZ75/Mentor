#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Maurizio'
import time
import tts
from kivy.lib import osc
from kivy.utils import Platform
from kivy.logger import Logger

platform = Platform()
activity_port = 3002
service_port = 3000


def say_something(message, *args):
    msg = message[2]
    #Logger.debug("say_something: TTS is talking: {}. Status is: {}-{}".format(
    #    tts.isSpeaking(), say_something.time_end_step, time.time()))
    #   if msg != say_something.last_message:
    if tts.isSpeaking():  # or say_something.time_end_step > time.time():
        pass
    #    Logger.debug("say_something: Still talking, doing nothing until {}. Now is".format(
    #        say_something.time_end_step < time.time()))
    else:
        #say_something.last_message = msg
        #Logger.debug("say_something: tts.speak({}, {})".format(msg, 'IT'))
        #say_something.status =
        tts.speak(msg, 'IT')
        #say_something.time_end_step = time.time() + 0.5
#say_something.status = True
#say_something.time_end_step = 0
#say_something.last_message = ""

if __name__ == '__main__':
    # get the argument passed
    #arg = os.getenv('PYTHON_SERVICE_ARGUMENT')
    osc.init()
    oscid = osc.listen(ipAddr='0.0.0.0', port=service_port)
    #sequence = Sequence()
    osc.bind(oscid, say_something, '/say')
    while True:
        osc.readQueue(oscid)
        time.sleep(.5)

