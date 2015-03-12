__author__ = 'SL_RU'

###Проигрыватель музыкальных файлов

from pygame import mixer as m

path = "C:\\music\\"

def init():
    m.init()

def play(file):
    m.music.load(file)
    m.music.play()

def stopAll():
    m.music.stop()

def set_endevent(func):
    m.music.set_endevent(func)
