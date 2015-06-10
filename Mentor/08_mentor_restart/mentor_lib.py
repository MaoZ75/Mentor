import os
from kivy.logger import Logger
import traceback

debug = True


def extract_title(complete_file_name):
    the_file = open(complete_file_name)
    first_row = the_file.readline()
    the_file.close()
    return first_row.split('\t')[1]  # ToDo sobstiture with official separator


class Sequences():

    def __init__(self):
            self.files = []
            self.titles = []
            self.origins = ["/sdcard/Mentor", "C:\\Mao\\Progetti\\Mentor\\sequenze", "composizioni"]
            self.base_folder = None

    def load_sequences(self):  # ToDo Universal Name for default parameters
        for orig in self.origins:
            if os.path.exists(orig):
                self.base_folder = orig
                Logger.debug("MentorLib.Sequences.LoadSequence: Set base dir for sequences {}".format(self.base_folder))
                break
        for files in os.listdir(self.base_folder):
            complete_file_name = os.path.join(self.base_folder, files, 'info.txt')
            if os.path.exists(complete_file_name):  # and len(self.files) < 6:  # ToDo Less specific
                self.files.append(complete_file_name)
                self.titles.append(extract_title(complete_file_name))
        while len(self.files) < 6:
            self.files.append(self.files[-1])
            self.titles.append("--")

    def file_name_for_title(self, title):
        return self.files[self.titles.index(title)]

    def get_titles(self):
        return self.titles

    def start_sequence(self, *args, **kwargs):  #sequence_name):
        try:
            if args[0] == 'timer':  # args[0] is the Title
                #print self.root.ids.tx_timer
                """
                Logger.debug("Time goes: {}".format(self.timer_value))
                self.osc_push_message(self.timer_value, "/tmr")
                """
            else:
                """
                sequence_file_name = self.sequences.file_name_for_title(args[0])  # args[0] is the Title
                #print('The flexible function has *args of', str(args), "and **kwargs of", str(kwargs))
                self.osc_push_message(sequence_file_name, "/nsq")
                """
                pass
            #self.root.ids.sm.transition = SlideTransition(direction="left")
            #self.root.ids.sm.current = 'mentorplayer'  # self.root.ids.sm.next()
        except ValueError:
            Logger.debug("ValueError on start_sequence: no worry if you see me only at beginning")