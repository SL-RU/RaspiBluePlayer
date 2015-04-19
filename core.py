__author__ = 'SL_RU'

##главный файл. Точка входа

##from queue import Thread

from threading import Thread
import time, os
import aplayer as pl
import musicplayer as muspl
#from musicplayer import MusicPlayer
#import web
import hardware

path = "/home/pi/"
IS_BLUETOOTH_ALSA=True
IS_LINUX=True
IS_GPIO=True

pl.IS_BLUETOOTH_ALSA = IS_BLUETOOTH_ALSA
pl.IS_LINUX = IS_LINUX
hardware.IS_GPIO = IS_GPIO

pl.init()
mpl = muspl.MusicPlayer(path)
hardware.Init()

mpl.pause()

#def run_web():
#    web.start(mpl)

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

def ButtonClick():
    mpl.pause()

button = hardware.GPIOButton(24)
button.on_press = ButtonClick

halt = hardware.GPIOButton(22)
def haltButton():
    mpl.turn_off()
    os.system("sudo halt")
halt.on_long_press = haltButton
def bt():
    print("lol")
    muspl.aplayer.conn()
halt.on_press = bt
halt.LONG_press_count = 400
next = hardware.GPIOButton(23)
def nextButton():
    mpl.play_rnd()
next.on_press = nextButton


#thr_web = Thread(target=run_web)
#thr_web.setDaemon(True)
#thr_web.start()

thr_player = Thread(target=player_update)
thr_player.setDaemon(True)
thr_player.start()

thr_cli = Thread(target=cli)
#thr_cli.setDaemon(True)
thr_cli.start()
thr_player.join()

mpl.turn_off()
