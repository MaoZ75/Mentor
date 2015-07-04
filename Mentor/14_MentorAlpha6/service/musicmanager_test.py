
__author__ = 'Maurizio'

import os
from kivy.logger import Logger
from kivy.core.audio import SoundLoader
import random
from time import sleep


class MusicManager():

    def __init__(self):
        self.extensions = [".mp3"]
        self.playlist = []
        self.random = True
        self.idx = 0
        self.actual_song = None
        pass

    def scan_music_folder(self, folder='.', recurse=False):
        for the_root, dirs, files in os.walk(folder):
            for f in files:
                if os.path.splitext(f)[1].lower() in self.extensions:
                    self.playlist.append(os.path.join(the_root, f))
        if self.random:
            self.shuffle()
        else:
            self.sort()

    def set_random_state(self, state=True):
        self.random = state

    def play(self):
        self.actual_song.play()

    def play_next_on_stop(self):
        if self.actual_song.state == 'stop':
            self.idx = (self.idx + 1) % len(self.playlist)
            self.actual_song = SoundLoader.load(self.playlist(self.idx))
            self.play()

    def shuffle(self):
        random.shuffle(self.playlist)
        self.actual_song = SoundLoader.load(self.playlist[0])
        self.idx = 0

    def sort(self):
        self.playlist.sort()
        self.actual_song = SoundLoader.load(self.playlist[0])
        self.idx = 0

    def stop(self):
        self.actual_song.stop()



m = MusicManager()
m.scan_music_folder("C:\\Mao\\Progetti\\Musica\\MusicaSuNexus\\PerAttivita")
m.play()
sleep(5)
m.stop()
sleep(3)
m.play()
sleep(5)

