__author__ = 'SL_RU'

##главный файл. Точка входа

from queue import  Queue

from threading import Timer
import time
import aplayer as pl
import musicplayer

path = "C:\\"

pl.init()
musicplayer.init(path)

def func():
    while True:
        print("lol")
        time.sleep(2)

thr = Timer(2, func)
thr.setDaemon(True)
thr.start()

musicplayer.play_rnd()

while input() != "q":
    print("Press q to quit")

