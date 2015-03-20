__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random



class MusicPlayer(object):
    path = "music"
    musics = list()
    current_song = ""
    excluded_music = list()
    was = 0
    #вызывается при старте
    def __init__(self, pth):
        self.musics = list()
        self.path = pth + self.path
        wa = os.walk(self.path)
        for couple in wa:
            for f in couple[2]:
                self.musics.append(couple[0] + "\\" + f)
        print(self.musics)
    #вызывается, когда нужно переключится в режим музыки
    def turn_on(self):
        if self.was == 0:
            aplayer.set_endevent(self.on_eos)
            self.was = 1

    #вызывается, когда нужно переключится из режима музыки
    def turn_off(self):
        aplayer.stopAll()
        self.current_song = ""


    def play_song(self, song):
        self.current_song = song
        aplayer.play_file(song)
        aplayer.play()
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
        #if(self.current_song in self.musics):
        #    self.musics.remove(self.current_song)
        #    self.excluded_music.append(self.current_song)
        #pass
        if self.current_song != "":
            self.current_song = ""
            self.play_rnd()
