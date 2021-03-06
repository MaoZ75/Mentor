import os
import os.path
from kivy.logger import Logger
import traceback

debug = True


class Sequences():

    def __init__(self, platform):
            """
            :param platform: ['android', 'win', 'linux']
            :return:
            """
            self.files = []
            self.titles = []
            self.origins = [os.path.abspath(os.path.join(os.curdir, 'composizioni')),
                            "/sdcard/Mentor",
                            "C:\\Mao\\Progetti\\Mentor\\sequenze"]
            if platform == 'android':
                from android import AndroidService
                service = AndroidService('Mentor Service', 'running')
                service.start('service started')
                self.service = service
            #    self.folder_music = "/storage/emulated/legacy/Music/PerAttivita"
            #elif platform == 'win':
            #    self.folder_music = "C:\\Mao\\Progetti\\Musica\\MusicaSuNexus\\PerAttivita"
            #else:
            #    self.folder_music = ".\\music"
            # ToDo            Logger.info("Folder music: {}".format(self.folder_music))
            self.base_folder = None # ToDo more General
            for orig in self.origins:
                Logger.debug(
                    "MentorLib.Sequences.LoadSequence: {} exists? {}".format(
                        orig, os.path.exists(orig)))
                if os.path.exists(orig):
                    self.base_folder = orig
                    break
            Logger.info("Origins: {}".format(self.origins))
            Logger.debug("MentorLib.Sequences.LoadSequence: Set base dir for sequences {}".format(self.base_folder))
            # self.current_osc_message = ["60:0:5:5", "/tmr"] # ToDo: DelThis

    def extract_title(self, complete_file_name):
        the_file = open(complete_file_name)
        first_row = the_file.readline().replace('\r','').replace('\n','')
        the_file.close()
        return first_row.split(first_row[-1])[1]  # ToDo sobstiture with official separator

    def file_name_for_title(self, title):
        file_name = self.files[self.titles.index(title)]
        return file_name, file_name.replace('.txt', '.rst')

    def get_titles(self):
        return self.titles

    def load_sequences(self):  # ToDo Universal Name for default parameters
        for files in os.listdir(self.base_folder):
            complete_file_name = os.path.join(self.base_folder, files, 'info.txt')
            if os.path.exists(complete_file_name):
                self.files.append(complete_file_name)
                self.titles.append(self.extract_title(complete_file_name))

    def get_osc_message_from_title(self, title, rst_id, *largs):
        try:
            sequence_file_name, rst_file = self.file_name_for_title(title)  # args[0] is the Title
            if os.path.exists(rst_file):
                rst_id.preload(rst_file, encoding='utf-8', errors='ignore')
            self.current_osc_message = [sequence_file_name, "/nsq"]
            Logger.debug("mentor_lib.get_osc_message_from_title: Loaded {} as default sequence".format(self.current_osc_message))
        except ValueError:
            Logger.debug("ValueError on start_sequence: no worry if you see me only at beginning")
