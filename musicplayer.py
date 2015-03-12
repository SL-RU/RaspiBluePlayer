__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random

path = "music"
musics = list()
current_song = ""
excluded_music = list()

#вызывается при старте
def init(pth):
    global musics
    musics = list()
    wa = os.walk(pth + path)
    for couple in wa:
        for f in couple[2]:
            musics.append(couple[0] + "\\" + f)
    print(musics)

#вызывается, когда нужно переключится в режим музыки
def turn_on():
    aplayer.set_endevent(on_music_ends)

#вызывается, когда нужно переключится из режима музыки
def turn_off():
    global current_song
    aplayer.stopAll()
    current_song = ""


def play_song(song):
    global current_song
    current_song = song
    aplayer.play(song)

def play_rnd():
    global musics
    if len(musics) > 0:
        rnd = random.randint(0, len(musics) - 1)
        play_song(musics[rnd])

def on_music_ends():
    global musics, current_song, excluded_music
    if(current_song in musics):
        musics.remove(current_song)
        excluded_music.append(current_song)
    play_rnd()