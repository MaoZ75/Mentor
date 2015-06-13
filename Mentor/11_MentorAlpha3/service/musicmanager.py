
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
        try:
            self.actual_song.unload()
        except AttributeError:
            self.actual_song = None

    def scan_music_folder(self, folder='.', recurse=False):
        self.__init__()
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
        if self.actual_song is not None:
            self.actual_song.play()

    def pause(self):
        if self.actual_song is not None:
            self.actual_song.volume = 0.1

    def resume(self):
        if self.actual_song is not None:
            self.actual_song.volume = 1.0

    def play_next_on_stop(self):
        if self.actual_song.state == 'stop':
            self.idx = (self.idx + 1) % len(self.playlist)
            self.actual_song.unload()
            self.actual_song = SoundLoader.load(self.playlist[self.idx])
            self.play()

    def set_volume(self, value=0.5):
        if self.actual_song is not None:
            if self.actual_song.volume != value:
                self.actual_song.volume = value

    def get_status(self):
        if self.actual_song is None:
            return 'stop'
        else:
            return self.actual_song.state

    def shuffle(self):
        random.shuffle(self.playlist)
        self.actual_song = SoundLoader.load(self.playlist[0])
        self.idx = 0

    def sort(self):
        self.playlist.sort()
        self.actual_song = SoundLoader.load(self.playlist[0])
        self.idx = 0

    def stop(self):
        Logger.debug("MManager Stop: stopping step 1")
        if self.actual_song is not None:
            if self.actual_song.state == 'play':
                Logger.debug("MManager stop: starting")
                #self.actual_song.stop()
                Logger.debug("MManager stop: unloading")
                self.actual_song.unload()
            else:
                Logger.debug("MManager Stop: mysterious state {}".format(self.actual_song.state))


if __name__ == '__main__':
    pass
    m = MusicManager()
    m.scan_music_folder("C:\\Mao\\Progetti\\Musica\\MusicaSuNexus\\PerAttivita")
    m.play()
    sleep(2)
    m.pause()
    sleep(2)
    m.resume()
    sleep(2)
    m.stop()
