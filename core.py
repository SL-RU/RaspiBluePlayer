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

def run_web():
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

def player_update():
    while True:
        pl.update()


thr_web = Thread(target=run_web)
thr_web.setDaemon(True)
thr_web.start()

thr_player = Thread(target=player_update)
thr_player.setDaemon(True)
thr_player.start()

thr_cli = Thread(target=cli)
thr_cli.setDaemon(True)
thr_cli.start()
thr_cli.join()

mpl.turn_off()