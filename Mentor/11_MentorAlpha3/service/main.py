__version__ = '0.1.0'
__author__ = 'Maurizio'
import os
import time
from kivy.lib import osc
from sequence_manager import Sequence
from kivy.logger import Logger
from kivy.utils import Platform
platform = Platform()


activity_port = 3002
service_port = 3000
debug = True


def read_message_spk(message):  # ToDo: more elegant solution
    """
    :param message: in format '{}|{}|'.format(language, text)
                        instead of | any separator can be used
    :return: [language, text, other_parts]
    """
    if debug:
        print message
    return message.split(message[-1], 2)


def elapsed_seconds():
    return time.time() - elapsed_seconds.t0
elapsed_seconds.t0 = time.time()


def msg_feeding_ok():
    if msg_feeding_ok.time < elapsed_seconds():
        msg_feeding_ok.time = elapsed_seconds() + 2
        return True
    else:
        return False
msg_feeding_ok.time = 0


def osc_send():
    if len(osc_send.activities) > 0:
        msg, reg_type = osc_send.activities.pop(0)
        #Logger.info("osc_send: {}({}) [{} messages in queue]".format(msg, reg_type, len(osc_send.activities)))
        osc.sendMsg(reg_type, [msg, ], port=activity_port)
        #Logger.debug("{}:{}".format(reg_type, msg))
osc_send.activities = []
osc_send.last_activity = []


def osc_send2():
    if len(osc_send.activities) > 0:
        msg, reg_type = osc_send.activities.pop(0)
        #Logger.info("osc_send: {}({}) [{} messages in queue]".format(msg, reg_type, len(osc_send.activities)))
        osc.sendMsg(reg_type, msg, port=activity_port)
        #Logger.debug("{}:{}".format(reg_type, msg))


def osc_push_message(message='idle', reg_type='/msg'):
    #Logger.debug("'{}', '{}'".format(message,reg_type))
    if osc_send.activities.count([message, reg_type]) == 0 and \
            [message, reg_type] != osc_send.last_activity:  # Avoids double messages and repetitions
        osc_send.last_activity = [message, reg_type]
        osc_send.activities.append([message, reg_type])


def ping(message, *args):
    msg = "{}: {}".format(elapsed_seconds(), message[2])
    if debug:
        print msg
    osc_push_message(msg, '/msg')


if __name__ == '__main__':
    # get the argument passed
    #arg = os.getenv('PYTHON_SERVICE_ARGUMENT')
    osc.init()
    oscid = osc.listen(ipAddr='0.0.0.0', port=service_port)
    sequence = Sequence()
    osc.bind(oscid, sequence.player_command, '/cmd')
    #osc.bind(oscid, ping, '/msg')
    #osc.bind(oscid, sequence.new_activity, '/act')
    osc.bind(oscid, sequence.start_a_new_sequence, '/nsq')
    osc.bind(oscid, sequence.load_tabata, '/tbt')
    osc.bind(oscid, sequence.load_timer, '/tmr')
    # osc.bind(oscid, sequence.push_an_act, '/act')
    # osc.bind(oscid, start_sequence, '/seq')
    while True:
        # this will print 'Hello From Service' continually, even when the application is switched
        # print "{} from {}".format(arg, elapsed_seconds())
        """if msg_feeding_ok():
            osc_push_message("A message", "/msg")
        else:
            pass
            #tts.speak(message='Resistance is FUTILE. Select an e-mail app.', language='EN')
        """
        osc.readQueue(oscid)
        osc_push_message(sequence.get_state_string(), '/osd')
        #Logger.debug("service/main: cycling")
        osc_send2()
        sequence.activity_click()
        time.sleep(1.1)

