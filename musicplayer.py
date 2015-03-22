__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random
import json


class MusicPlayer(object):
    path = "music"
    path_settings = ".rbp.music.json"
    musics_all = dict()
    musics_excluded = list()
    musics = list()
    current_song = ""
    song_duration = -1
    was = 0
    #вызывается при старте
    def __init__(self, pth):
        self.musics = list()
        self.musics_all = dict()
        self.musics_excluded = list()
        self.path = pth + self.path
        self.path_settings = pth + self.path_settings
        wa = os.walk(self.path)
        for couple in wa:
            for f in couple[2]:
                if(f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')):
                    self.add_file(couple[0] + "/" + f)
        self.load()
        if(self.current_song != ""):
            if(self.current_song in self.musics_all.values()):
                self.play_song(self.current_song)
        print(self.musics)
    #вызывается, когда нужно переключится в режим музыки
    def turn_on(self):
        if self.was == 0:
            aplayer.set_endevent(self.on_eos)
            self.was = 1
    def add_file(self, f):
        if(f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')):
            leng = len(self.musics_all.values())
            self.musics_all.update({leng: f})
            self.musics.append(f)
    def load(self):
        if os.path.isfile(self.path_settings):
            f = open(self.path_settings, "r")
            data = json.load(f)
            self.musics_excluded = data["excluded"]
            if(data["current_song"] in self.musics_all.values()):
                self.current_song = data["current_song"]
            self.musics = list()
            for d in self.musics_all.values():
                if(not d in data["excluded"]):
                    self.musics.append(d)
            if(len(self.musics) <= 0):
                self.musics = list(self.musics_all.values()).copy()
            f.close()
    def save(self):
        f = open(self.path_settings, "w")
        json.dump(
            {
                "excluded" : self.musics_excluded,
                "current_song" : self.current_song
            },
            f)
        f.close()
    #вызывается, когда нужно переключится из режима музыки
    def turn_off(self):
        was = 0
        self.save()
        aplayer.pause()


    def play_song(self, song):
        self.current_song = song
        aplayer.play_file(song)
        aplayer.play()
        self.song_duration = -1
        self.turn_on()


    def play_rnd(self):
        if len(self.musics) > 0:
            rnd = random.randint(0, len(self.musics) - 1)
            self.play_song(self.musics[rnd])

    def pause(self):
        aplayer.pause()
    def play(self):
        if(self.current_song == ""):
            self.play_rnd()
        else:
            aplayer.play()

    def on_eos(self, a, *args, **kwds):
        if(self.current_song in self.musics_all.values()):
            self.musics.remove(self.current_song)
            self.musics_excluded.append(self.current_song)
        if(len(self.musics) <= 0):
            self.musics = list(self.musics_all.values()).copy()
            self.musics_excluded = list()
        self.current_song = ""
        self.play_rnd()

    def get_pos(self):
        if(self.song_duration <= 0):
            d = aplayer.get_duration()
            if(d != None):
                self.song_duration = d
                return aplayer.get_pos() * d
            else:
                return 0
        else:
            return aplayer.get_pos() * self.song_duration