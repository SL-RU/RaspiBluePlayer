__author__ = 'SL_RU'

##главный файл. Точка входа

##from queue import Thread

from threading import Thread
import time
import aplayer as pl
from musicplayer import MusicPlayer
import web

path = "E:\\"

pl.init()
mpl = MusicPlayer(path)

def run_pyglet():
    web.start(mpl)

def cli():
    inp = ""
    while True:
        print("Press q to quit")
        inp = input()
        if(inp == "q"):
            break
        elif(inp == "p"):
            mpl.play_rnd()
        elif inp=="s":
            pl.pause()


thr = Thread(target=cli)
thr.setDaemon(True)
thr.start()

thr = Thread(target=run_pyglet)
thr.setDaemon(True)
thr.start()


while True:
    pl.update()
