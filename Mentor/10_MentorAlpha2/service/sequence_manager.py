__author__ = 'Maurizio Stagni'

from kivy.logger import Logger
import time
import tts
import os
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
        # self.thresholds = [20*60, 15*60, 10*60, 5*60, 2*60, 60] ToDo: Maybe one day!
        self.base_seq_dir = ""
        self.bg_img = "images/bk_nw.png"  # will be used by the ui!
        self.default_bg_img = "images/bk_nw.png"
        if platform == 'win':
            self.default_snd = "../sounds/02_sfs.ogg"
        else:
            self.default_snd = "../sounds/02_sfs.mp3"
        self.idx_stp = -1
        self.music_folder = '.'
        self.official_separator = "\t"
        self.ok_music = True
        self.ok_play = False
        self.pause_time = 0
        self.res_last_action = 0
        self.separators = ["\t", ";"]
        self.seq_images = []  # image location
        self.seq_modes = []  # Action (TTS_EN, TTS_IT, Play)
        self.seq_snds = []  # sound to be played at the end location
        self.seq_text_messages = []  # Text/FileName
        self.seq_timings = []  # in seconds
        self.sound = None
        self.sound_manager = MusicManager()
        self.sequence_state = 50  # Variable for state machine on playing attention sound
        self.time_duration = 0
        self.time_end_step = 0
        self.time_last_step = 0
        self.time_sound_played = 0
        self.title = 'Null Sequence'

    def _initialize_image(self, step=-1):
        if step == -1:
            step = self.idx_stp + 1
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

    def activity_click(self):
        #Logger.debug("sequence.activity_click: self.sequence_state: {} - okPLay: {}".format(
        #    self.sequence_state, self.ok_play))
        if self.ok_play:
            if self.res_last_action == 0:  # Ok for a new check
                missing = self.time_end_step - time.time()
                if missing < 0 or self.sequence_state > 10:
                    if self.sequence_state == 10:  # Load The sound File
                        if self._initialize_sound():
                            self.sequence_state = 20
                        else:
                            self.sequence_state = 30
                    elif self.sequence_state == 20:                                   # 20 Wait for time to be elapsed.
                        if missing < -5:  # ToDo avoid 5sec limit
                            Logger.debug("activity_click: sound too long for step {}: {}".format(
                                self.idx_stp,
                                self.seq_snds[self.idx_stp]))
                            self.sequence_state = 30
                        elif time.time() > self.time_sound_played:  # Ok to stop the file
                                Logger.debug("activity_click: stopping sound at {}".format(time.time()))
                                self.sound.stop()
                                self.sound.unload()  # ToDo: improve this unloading more smartly
                                self.sequence_state = 30
                        else:
                            pass  # Logger.debug("activity_click: waiting for sound play")
                    elif self.sequence_state == 30:                                     # 30 Update indexes and images.
                        if self.idx_stp < len(self.seq_timings):
                            self.idx_stp += 1
                            self._initialize_image()
                            self.sequence_state = 40  # waiting clock to let the screen to be updated
                        else:
                            self.stop_sequence()
                    elif self.sequence_state == 40:  # Excecute Next Step
                    elif self.sequence_state == 60:  # Excecute Next Step
                        self.time_last_step = int(time.time())
                        self.time_end_step = self.time_last_step + self.seq_timings[self.idx_stp]
                        self.sequence_state = 70
                    elif self.sequence_state == 70:  # Excecute Next Step
                        self.exec_actual_activity()
                        self.sequence_state = 10
            elif self.sequence_state == 10:  # Last execution failed: do it again
                self.exec_actual_activity()
            #if not tts.isSpeaking():
                #pass
                #self.sound_manager.set_volume(1) # ToDo sound_manager
                #self.sound_manager.play_next_on_stop()  # ToDo sound_manager

    def delta_pause(self):
        if self.pause_time == 0:
            return 0
        else:
            return int(time.time()) - self.pause_time

    def exec_actual_activity(self):
        if tts.isSpeaking():
            self.res_last_action = -1
            Logger.debug("exec_actual_activity: Still talking")
        elif self.seq_modes[self.idx_stp][0:4] == "TTS_":
            #self.sound_manager.set_volume(0.1)
            # ToDo sound_manager
            lng = self.seq_modes[self.idx_stp][-2:]
            msg = self.seq_text_messages[self.idx_stp]
            Logger.debug("Sequence exec_actual_activity: tts.speak({}, {})".format(msg, lng))
            self.res_last_action = tts.speak(msg, lng)
        else:
            Logger.debug("Sequence exec_actual_activity: VIRTUAL{} {})".format(
                self.seq_modes[self.idx_stp], self.seq_text_messages[self.idx_stp]))
            self.res_last_action = 0  # show must go on!

    def get_state_string(self):
        #if len(self.seq_timings) == 0 or self.idx_stp == -1:
        if self.idx_stp == -1 or self.idx_stp == len(self.seq_text_messages):
            time_left_action = '--.--'
            seq_text_message = ''
        else:
            time_left_action = self.time_left_action()
            seq_text_message = self.seq_text_messages[self.idx_stp]
        message = "{}\t{}\t{}\t{}\n\n{}\n[{}-{}]\t{}".format(
            time_left_action,
            self.time_left_total(),
            self.bg_img,
            self.title, seq_text_message.replace(".", "\n"),
            self.idx_stp + 1, len(self.seq_timings),
            "blabla")
        message = [time_left_action,
                   self.time_left_total(),
                   self.bg_img,
                   self.title, seq_text_message.replace(".", "\n"),
                   self.idx_stp + 1, len(self.seq_timings)
                    ]
        #Logger.debug(message.replace("\t", "<-  ->"))
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
            self.ok_play = True
            #self.time_end_step += int(time.time()) - self.pause_time
            self.pause_time = 0
        elif cmd == 'pause':
            self.ok_play = False
            if self.pause_time == 0:  # To avoid multiple pause presses
                self.pause_time = int(time.time())
        elif cmd == 'stop':
            self.stop_sequence()
        elif cmd == 'forward':
            self.res_last_action = 0
            #self.idx_stp = min(len(self.seq_timings), self.idx_stp + 1)
            self.time_end_step = int(time.time()) + 1
        elif cmd == 'rewind':
            self.res_last_action = 0
            self.idx_stp = max(-1, self.idx_stp - 2)
            self.time_end_step = int(time.time()) - 1
        elif cmd == 'replay':
            self.exec_actual_activity()

    def start_a_new_sequence(self, message, *args):
        self.__init__()
        max_count = 0
        for coding in ['windows-1252', 'windows-1252', 'UTF-8', 'ASCII', 'ISO-8859-1']:
            try:
                print(message)
                seq_file = open(message[2], 'r')
                content = seq_file.read()
                seq_file.close()
                self.base_seq_dir = os.path.dirname(message[2])
                Logger.info("start_a_new_sequence: base folder: {}".format(self.base_seq_dir))
                Logger.info("start_a_new_sequence: {} well decoded in {}".format(message[2], coding))
                Logger.info("start_a_new_sequence: Testo:\n{}".format(content))
                break
            except UnicodeDecodeError:
                Logger.critical(
                    "start_a_new_sequence: {} Tentata codifica {} errata".format(message[2], coding))
                pass
        for s in self.separators:
            occurrences = content.count(s)
            if occurrences > max_count:
                self.official_separator = s
                max_count = occurrences
        parameter = True
        #setattr(self, 'title', 'now works')
        for s in content.replace('\r', '').split('\n'):
            if parameter:
                val = s.split(self.official_separator)
                print val[0], val[1]
                if val[0].find("Start of the sequence") > -1:  # Inizio Sequenza ____________________________
                    parameter = False
                else:  # is a valid parameter _______________________________
                    try:
                        setattr(self, val[0], val[1])  # ToDo in python 3 remove!
                    except UnicodeEncodeError:
                        setattr(self, 'title', val[1])  # ToDo in python 3 remove!
                        Logger.debug('start_a_new_sequence: Tarokked the title: {}'.format(val[1]))
            else:  # Decoding istructions from here _______________________________________________
                if s.count(self.official_separator) > 1:  # It is a valid instruction, at least 3 operand
                    self.new_activity(["", "", s])  # ToDo Valutation about this mess
        self._initialize_image(0)
        Logger.info("New Sequence Loaded: Title: {} ({} seconds, {} elements)".format(
            self.title, format_seconds(self.time_duration), len(self.seq_timings)))
        tts.speak("Sequence Loaded: {}".format(self.title))

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

    def stop_sequence(self):
        Logger.debug("stop_sequence: OK 1")
        # self.sound_manager.stop()  # ToDo: check if ok
        # ToDo sound_manager
        self.ok_play = False
        #Logger.debug("stop_sequence: OK 2")
        self.res_last_action = 0
        #Logger.debug("stop_sequence: OK 3")
        self.idx_stp = -1
        #Logger.debug("stop_sequence: OK 4")
        self.time_end_step = 0
        #Logger.debug("stop_sequence: OK 5")
        self.sequence_state = 10

    def time_left_action(self):
        sec = 0
        if self.time_end_step == 0:
            pass  # return "00.00"
        else:
            sec = max(0,
                      int(self.time_end_step - time.time())) #  + self.delta_pause()
        return format_seconds(sec)

    def time_left_total(self):
        left = self.time_duration
        if self.time_end_step == 0:
            pass  # return format_seconds()
        else:
            sum_remaining = 0
            for i in range(max(self.idx_stp+1, 0), len(self.seq_timings)):
                sum_remaining += self.seq_timings[i]
            left = max(0,
                       int(self.time_end_step - time.time()) + sum_remaining + self.delta_pause())
        return format_seconds(left)


