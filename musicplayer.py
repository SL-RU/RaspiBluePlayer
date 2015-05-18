__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random
import json
import aplayer

def log(s):
    print("MUSIC_PLAYER:" + s)

class MusicPlayer(object):
    aplayer = None
    songs = list()
    cur_song = ""
    path = ""

    def __init__(self, audioPlayer, path):
        self.aplayer = audioPlayer
        self.path = path
        self.find_musics()

    def find_musics(self):
        """Find and enumerate all audio files in the path"""
        self.songs = list()
        wa = os.walk(self.path)
        for couple in wa:
            for f in couple[2]:
                if(f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')):
                    self.add_file(couple[0] + "/" + f)

    def add_file(self, f):
        if (f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')) and f.startswith(self.path):
#            leng = len(self.musics_all.values())
            self.songs.append(f[len(self.path):])
            log(f[len(self.path):])

    def play_song_by_name(self, name):
        if(aplayer is not None) and os.path.isfile(self.path + name):
            b = self.aplayer.play_file(self.path + name)
            self.cur_song = name
            return b
        else:
            return False

    def play_song_by_id(self, id):
        self.play_song_by_name(self.songs[id])

    def play_next(self):
        s = random.choice(self.songs)
        self.play_song_by_name(s)
