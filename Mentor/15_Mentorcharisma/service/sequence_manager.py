__author__ = 'Maurizio Stagni'

from kivy.logger import Logger
import time
import tts
import os
import os.path
from kivy.core.audio import SoundLoader
from musicmanager import MusicManager
from kivy.utils import Platform
from kivy.logger import Logger
from time import sleep  # ToDo: Eliminare
#import codecs
platform = Platform()

import sys
reload(sys)
#sys.setdefaultencoding("windows-1252" )
sys.setdefaultencoding("UTF-8")

debug = True  # ToDo: eliminare debug


def format_seconds(seconds):
    return "{:02}.{:02}".format(int(seconds / 60), int(seconds % 60))


class Sequence():

    def __init__(self):
        self.base_seq_dir = ""
        # initializing sequences
        self.starting_step = 1
        self.idx_stp = -1
        self.official_separator = "\t"
        self.separators = ["\t", ";"]
        self.seq_images = []  # image location
        self.seq_modes = []  # Action (TTS_EN, TTS_IT, Play)
        self.seq_snds = []  # sound to be played at the end location
        self.seq_text_messages = []  # Text/FileName
        self.seq_timings = []  # in seconds
        self.seq_time_thresholds = [0.0]  # time in which the step must start
        self.sound = None
        self.sound_manager = MusicManager()
        # initializing state machine for seq manager
        self.sequence_state = 90  # Variable for state machine of activity_click
        # initializing messages
        self.messages = []
        self.last_message = ''
        self.title = 'Null Sequence'
        self.bg_img = "images/bk_nw.png"  # will be used by the ui!
        self.default_bg_img = "images/bk_nw.png"
        # initializing sounds
        self.time_duration = 0
        self.time_sound_played = 0
        if platform == 'win':
            self.default_snd = "../sounds/02_sfs.ogg"
        else:
            self.default_snd = "../sounds/02_sfs.mp3"
        self.music_folder = '.'
        self.ok_music = True

    def _initialize_image(self, step=-1):
        if step == -1:
            step = self.idx_stp
        try:
            if self.seq_images[step] == "":
                #Logger.debug("_initialize_image: same image for background:{}".format(self.bg_img))
                pass
            else:
                Logger.debug("{}-{}".format(self.base_seq_dir, self.seq_images[step]))
                file_name = ""
                if os.path.exists(os.path.join("..", self.seq_images[step])):
                    file_name = self.seq_images[step]
                elif os.path.exists(os.path.join(self.base_seq_dir, self.seq_images[step])):
                    file_name = os.path.join(self.base_seq_dir, self.seq_images[step])
                Logger.debug("_initialize_image: Initializing {}".format(file_name))
                if not file_name == "":
                    self.bg_img = file_name
                    Logger.debug("_initialize_image: new image for background:{}".format(file_name))
                else:
                    self.bg_img = self.default_bg_img
                    Logger.debug("_initialize_image: error ({}) and then default for bg:{}".format(
                        file_name, self.default_bg_img))
        except IndexError:
            self.bg_img = self.default_bg_img
            Logger.debug("_initialize_image: IndexError. Default for bg:{}".format(
                self.default_bg_img))

    def _initialize_sound(self):
        """
        initializes and eventually starts the sound for the current step
        :return:
            True if everything is ok
            False if the sound shouldn't / coundn't be started
        """
        #Logger.debug("[{}]".format(self.seq_snds[self.idx_stp]))
        if self.seq_snds[self.idx_stp] == "":
            Logger.debug('_initialize_sound no sound played for step {}'.format(
                self.idx_stp))
            return False
        else:
            if self.seq_snds[self.idx_stp] == "default":
                Logger.debug('_initialize_sound default sound for step {}\
                             ({})'.format(self.idx_stp, self.default_snd))
                self.sound = SoundLoader.load(self.default_snd)
            else:
                Logger.debug('_initialize_sound loading sound for step {}\
                             ({})'.format(self.idx_stp, self.seq_snds[self.idx_stp]))
                if os.path.exists(self.seq_snds[self.idx_stp]):
                    self.sound = self.seq_snds[self.idx_stp]
                else:
                    self.sound = SoundLoader.load(os.path.join(self.base_seq_dir, self.seq_snds[self.idx_stp]))
            if self.sound is None:
                Logger.debug("_initialize_sound: not a valid sound for step {}: {}".format(
                    self.idx_stp, self.seq_snds[self.idx_stp]))
                return False
            elif self.sound.state == 'stop':
                self.sound.play()
                if platform == "android":
                    self.music_folder = "/sdcard/Music/PerAttivita"  # ToDo: not good at all
                    self.time_sound_played = time.time() + int(os.path.basename(self.default_snd).split("_")[0])
                    # ToDo: eliminate this ugly condition
                elif platform == "win":
                    self.music_folder = "C:\Mao\Progetti\Musica\MusicaSuNexus\PerAttivita"  # ToDo: not good at all
                    self.time_sound_played = time.time() + self.sound.length
                else:
                    self.music_folder = "."  # ToDo: not good at all
                    self.time_sound_played = time.time()
                #Logger.info("New sequence: Loading the mucis folder: {}".format(self.music_folder))
                # self.sound_manager.scan_music_folder(self.music_folder)
                # ToDo sound_manager
                Logger.debug('activity_click: Sound {} end playing sound on{}. Sound\
                    length is {}. Now is{}'.format(self.sound.filename, self.time_sound_played,
                    self.sound.length, time.time()))
                return True
            else:
                Logger.debug("activity_click: Sound in not expected state {} for step {}: {}".format(
                    self.sound.state,
                    self.idx_stp,
                    self.seq_snds[self.idx_stp]))
                return False

    def activity_click(self, request=None):
        """request values
        None        let it run
        'replay'    redo the last activity
        'stop'      stops the sequence
        'start'     starts the sequence
        'pause'     not implemented


        :return: actual_state
        """
        #Logger.debug("sequence_manager Activity Click: state {}, step {}".format(self.sequence_state, self.idx_stp))
        if request == 'stop':
            self.sequence_state = 80
        if self.sequence_state == 10:                                            # 10 Waiting for the next trigger
            if request == 'replay':
                self.sequence_state = 60
            else:
                if self.actual_idx() != self.idx_stp:
                    self.sequence_state = 20
        elif self.sequence_state == 20:                                          # 20 Load sound and update indexes
            # Load The sound File
            if self._initialize_sound():
                self.sequence_state = 30
            else:
                self.sequence_state = 60
            # Update indexes
            if self.actual_idx() < len(self.seq_timings):
                self.idx_stp = self.actual_idx()
                self._initialize_image()
            else:
                self.sequence_state = 80
        elif self.sequence_state == 30:                                        # 30 Wait for the sound to be played
            missing = time.time() - self.seq_time_thresholds[self.idx_stp]
            if missing < -5:  # ToDo sound has to be played in max 5sec, generalize
                Logger.debug("activity_click: sound too long for step {}: {}".format(
                    self.idx_stp,
                    self.seq_snds[self.idx_stp]))
                self.sequence_state = 60
            elif time.time() > self.time_sound_played:  # Ok to stop the file
                    Logger.debug("activity_click: stopping sound at {}".format(time.time()))
                    self.sound.stop()
                    self.sound.unload()  # ToDo: improve this unloading more smartly
                    self.sequence_state = 60
        elif self.sequence_state == 60:                              # 60 Launch the next step asap
            res = self.exec_actual_activity()
            Logger.debug("Seq mana, activity click, exec_actual_activity gives {}, {}".format(res, res == 0))
            #if res == 0:
            self.sequence_state = 10
        elif self.sequence_state == 80:                              # 80 Stop the sequence
            # self.sound_manager.stop()  # ToDo: check if ok
            # ToDo sound_manager
            self.seq_time_thresholds = [0.0]  # time in which the step must start
            self.idx_stp = -1
            self.sequence_state = 90
        elif self.sequence_state == 90:                              # Sequence loaded: waiting for start
            if request == 'start':
                self.sequence_state = 99
        elif self.sequence_state == 99:  # Start the sequence
            basetime = time.time()
            self.seq_time_thresholds = [] #Must be one element more than seq_timings
            for i in range(self.starting_step -1):
                self.seq_time_thresholds.append(basetime-100)
            self.seq_time_thresholds.append(basetime)
            for timing in self.seq_timings[self.starting_step-1:]:
                basetime += timing
                self.seq_time_thresholds.append(basetime)
            self.idx_stp = -1
            self.sequence_state = 10
        if self.sequence_state in [10, 20, 60]:
            self.push_message(self.get_cockpit_info(), '/osd')

        #if not tts.isSpeaking():
            #pass
            #self.sound_manager.set_volume(1) # ToDo sound_manager
            #self.sound_manager.play_next_on_stop()  # ToDo sound_manager

    def actual_idx(self):
        for i in range(len(self.seq_time_thresholds)):
            #Logger.debug("Sequence - actual_idx: {} - {} - {}".format(
            #    self.seq_time_thresholds[i],
            #    time.time(),
            #    self.seq_time_thresholds[i] >= time.time()))
            if self.seq_time_thresholds[i] >= time.time():
                return i-1
        return len(self.seq_time_thresholds) - 1

    def delta_pause(self):
        if self.pause_time == 0:
            return 0
        else:
            return int(time.time()) - self.pause_time

    def exec_actual_activity(self):
        """

        :return: -1 if system not ready and need to be called later
                 0 if OK
        """
        if tts.isSpeaking(): #adding last sound played
            return -1
            Logger.debug("exec_actual_activity: Still talking")
        elif self.seq_modes[self.idx_stp][0:4] == "TTS_":
            #self.sound_manager.set_volume(0.1)
            # ToDo sound_manager
            lng = self.seq_modes[self.idx_stp][-2:]
            msg = self.seq_text_messages[self.idx_stp]
            Logger.debug("Sequence exec_actual_activity: tts.speak({}, {})".format(msg, lng))
            return tts.speak(msg, lng)
        else:
            Logger.debug("Sequence exec_actual_activity: VIRTUAL{} {})".format(
                self.seq_modes[self.idx_stp], self.seq_text_messages[self.idx_stp]))
            return 0  # show must go on!

    def get_cockpit_info(self):
        #if len(self.seq_timings) == 0 or self.idx_stp == -1:
        if self.idx_stp == -1 or self.idx_stp == len(self.seq_text_messages):
            time_left_action = '--.--'
            seq_text_message = ''
        else:
            seq_text_message = self.seq_text_messages[self.idx_stp]
        message = [self.time_left_action(),
                   self.time_left_total(),
                   self.bg_img,
                   self.title,
                   seq_text_message,
                   self.idx_stp + 1,
                   len(self.seq_timings)
                   ]
        return message

    def load_music_folder(self, folder, recurse=True):
        pass
        # self.sound_manager.scan_music_folder(folder, recurse)
        # ToDo sound_manager

    def new_activity(self, message, *args):
        val = message[2].split(self.official_separator)
        self.seq_timings.append(int(val[0]))
        self.time_duration += int(val[0])
        self.seq_modes.append(val[1])
        self.seq_images.append(val[2])
        self.seq_snds.append(val[3])
        self.seq_text_messages.append(val[4])

    def player_command(self, message, *args):
        cmd = message[2]
        Logger.info("Sequence Player Command: New command: {}".format(cmd))
        if cmd == 'play':
            self.activity_click('start')
        elif cmd == 'pause':
            pass # Not Yet Implemented
        elif cmd == 'stop':
            self.starting_step = 1
            self.activity_click('stop')
        elif cmd == 'forward':
            pass  # Not Yet Implemented
        elif cmd == 'rewind':
            pass  # Not Yet Implemented
        elif cmd == 'replay':
            self.activity_click('replay')
        elif cmd[:-2] == 'jump to step ':
            step = int(cmd[-2:])
            self.starting_step = step
            self.activity_click('stop')
            s = self.get_cockpit_info()
            s[-2] = step
            self.push_message(s, '/osd')

    def start_a_new_sequence(self, message, *args):
        self.__init__()
        #  ------------------------------------------------------------------------------- Read The File
        for coding in ['windows-1252', 'windows-1252', 'UTF-8', 'ASCII', 'ISO-8859-1']:
            try:
                seq_file = open(message[2], 'r')
                content = seq_file.read()
                seq_file.close()
                self.base_seq_dir = os.path.dirname(message[2])
                Logger.info("start_a_new_sequence: base folder: {}".format(self.base_seq_dir))
                Logger.info("start_a_new_sequence: {} well decoded in {}".format(message[2], coding))
                #Logger.info("start_a_new_sequence: Testo:\n{}".format(content))
                break
            except UnicodeDecodeError:
                Logger.critical(
                    "start_a_new_sequence: {} Tentata codifica {} errata".format(message[2], coding))
                pass
        #  ------------------------------------------------------------------------------- First Parsing: find separator
        max_count = 0
        for s in self.separators:
            occurrences = content.count(s)
            if occurrences > max_count:
                self.official_separator = s
                max_count = occurrences
        parameter = True
        page_rst = "{}\n===========\n{}".format(self.title, content)
        page_line_count = 0
        for s in content.replace('\r', '').split('\n'):
        #  ----------------------------------------------------------------------------- Parsing High part, Title, etc.
            if parameter:
                val = s.split(self.official_separator)
                if val[0].find("Start of the sequence") > -1:  # Inizio Sequenza ____________________________
                    parameter = False
                else:  # is a valid parameter _______________________________
                    try:
                        setattr(self, val[0], val[1])  # ToDo in python 3 remove!
                        page_rst = "{}\n===========\n\nSelf Generated sequence:\n\n".format(self.title)
                    except UnicodeEncodeError:
                        setattr(self, 'title', val[1])  # ToDo in python 3 remove!
                        Logger.debug('start_a_new_sequence: Tarokked the title: {}'.format(val[1]))
        #  ----------------------------------------------------------------------------- Parsing Excercises
            else:  # Decoding istructions from here _______________________________________________
                if s.count(self.official_separator) >= 2:  # It is a valid instruction, at least 3 operand
                    self.new_activity(["", "", s])  # ToDo Valutation about this mess
                    page_line_count += 1
                    page_rst += "{:02d}. {}\n\n".format(page_line_count, s)
        self._initialize_image(0)
        rst_file = os.path.join(self.base_seq_dir, 'info.rst')
        if not os.path.exists(rst_file):
            page_file = open(rst_file, 'w')
            page_file.write(page_rst)
            page_file.close()
        self.push_message([rst_file], '/sld')
        Logger.info("New Sequence Loaded: Title: {} ({} seconds, {} elements)".format(
            self.title, format_seconds(self.time_duration), len(self.seq_timings)))
        tts.speak("Sequence Loaded")


    def load_tabata(self, message, *args):
        self.__init__()
        seconds_go, seconds_rest, excercises, rounds = message[2:]
        self.title = 'Timer: {} Round {} exercises.{} sec wkout, {} rest.'.format(
            rounds, excercises, seconds_go, seconds_rest)
        description = 'Starting the following sequence:.{} Round of {} exercises.Practice for {} seconds, rest for {} seconds.Prepare to sweat!'.format(
            rounds, excercises, seconds_go, seconds_rest)
        self.seq_timings.append(10)
        self.time_duration += 10
        self.seq_modes.append('TTS_EN')
        self.seq_images.append('images/love_burpees.png')
        self.seq_text_messages.append(description)
        self.seq_snds.append('default')
        for j in range(int(rounds)):
            for i in range(int(excercises)):
                # Init start sequence
                self.seq_timings.append(int(seconds_go))
                self.time_duration += int(seconds_go)
                self.seq_modes.append('TTS_EN')
                self.seq_images.append('images/love_burpees.png')
                if i < 1:
                    self.seq_text_messages.append('Start Round {}.Exercise {}.'.format(j+1, i+1))
                else:
                    self.seq_text_messages.append('Start exercise {}.'.format(i+1))
                self.seq_snds.append('default')
                # Init Rest Sequence
                if int(seconds_rest) > 0:
                    self.seq_timings.append(int(seconds_rest))
                    self.time_duration += int(seconds_rest)
                    self.seq_modes.append('TTS_EN')
                    self.seq_images.append('images/now_rest.png')
                    self.seq_text_messages.append('Now rest')
                    self.seq_snds.append('default')
        self._initialize_image(0)
        Logger.info("New Sequence Loaded: Title: {} ({} seconds, {} elements)".format(
            self.title, format_seconds(self.time_duration), len(self.seq_timings)))
        tts.speak("Sequence Loaded")

    def load_timer(self, message, *args):
        duration_all = int(message[0])*60 + int(message[1])
        timer = [[30, "30 seconds"],
                 [30, "1 minute"],
                 [60, "2 minutes"],
                 [180, "5 minutes"],
                 [300, "10 minutes"],
                 [300, "15 minutes"],
                 [900, "30 minutes"],
                 [900, "45 minutes"],
                 [900, "1 hour"],
                 [900, "1 hour and 15 minutes"],
                 [900, "1 hour and 30 minutes"],
                 [900, "1 hour and 45 minutes"],
                 [900, "2 hours"],
                 ]
        actual = 0
        index = -1
        while actual+timer[index+1][0] < duration_all:
                index += 1
                actual += timer[index][0]
                Logger.debug("{} - {}".format(duration_all, actual))
        Logger.debug("{} - {} = {}".format(duration_all, actual, duration_all - actual))
        self.seq_timings.append(duration_all - actual)
        self.time_duration += self.seq_timings[-1]
        self.seq_modes.append('TTS_EN')
        self.seq_images.append('images/bk_nw.png')
        self.seq_text_messages.append('{} minute and {} seconds left.'.format(mm, sec))
        self.title = 'Timer of {} minute and {} seconds.'.format(mm, sec)
        self.seq_snds.append('default')
        while index >= 0:
                self.seq_timings.append(timer[index][0])
                Logger.debug(str(timer[index][0]))
                self.time_duration += timer[index][0]
                self.seq_modes.append('TTS_EN')
                self.seq_images.append('images/bk_nw.png')
                self.seq_text_messages.append('{} left.'.format(timer[index][1]))
                self.seq_snds.append('default')
                index -= 1

    def push_message(self, message='idle', reg_type='/msg'):
        #Logger.debug("'{}', '{}'".format(message,reg_type))
        if self.messages.count([message, reg_type]) == 0 and \
                [message, reg_type] != self.last_message:  # Avoids double messages and repetitions
            self.last_message = [message, reg_type]
            self.messages.append([message, reg_type])

    def time_left_action(self):
        return format_seconds(
            max(self.seq_time_thresholds[self.idx_stp + 1] - time.time(), 0))

    def time_left_total(self):
        return format_seconds(
            max(self.seq_time_thresholds[-1] - time.time(), 0))


