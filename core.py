#!/usr/bin/python3
__author__ = 'SL_RU'

##главный файл. Точка входа

##from queue import Thread

from threading import Thread
import time, os
import aplayer
import musicplayer
pl = aplayer.Aplayer("hw")

path = "/mnt/doc/music/"

muspl = musicplayer.MusicPlayer(pl, path)
muspl.load()
def cli():
    global path, muspl
    inp = ""
    while True:
        print("Press q to quit")
        inp = input()
        if inp is "q":
            break
#        elif(inp == "p"):
#            mpl.play_rnd()
        elif inp is "s":
            pl.pause()
        if inp is "p":
            muspl.play()
        if inp is "f":
            muspl.play_forw()
        if inp is "k": #skip
            muspl.on_song_end()
        if inp.startswith("pl "):
            muspl.play_song_by_name(inp[3:])
        if inp.startswith("save"):
            print("saving player")
            muspl.save()
        if inp.startswith("load"):
            print("load player")
            muspl.load()

def player_update():
    while True:
        pl.update()


thr_player = Thread(target=player_update)
thr_player.setDaemon(True)
thr_player.start()

thr_cli = Thread(target=cli)
thr_cli.setDaemon(True)
thr_cli.start()
thr_cli.join()
