#!/usr/bin/python3
__author__ = 'SL_RU'

##главный файл. Точка входа

##from queue import Thread

from threading import Thread
import time, os
import aplayer
import musicplayer
import booksplayer

import hardware
hardware.Init()

import bluetooth_headset

#Button's pins, connected to GPIO.
#physical placement:
# 0 1   5 6
#     4 
# 2 3   7 8
button_pins = [21, 19, 23, 26, 18, 13, 11, 16, 15]

#Led's pins.
# Left's id - 0, right's - 1
led_pins = [24, 22]

#Bluetooth headset MAC. Needed to connecting and listening events
headset_MAC = "00:11:67:11:11:8C"

buttons = []
for i in range(len(button_pins)):
    buttons.append(hardware.GPIOButton(button_pins[i]))

leds = []
for i in range(len(led_pins)):
    leds.append(hardware.GPIOLed(led_pins[i]))

blueh = bluetooth_headset.BluetoothHeadsetEvents(headset_MAC)
    
pl = aplayer.Aplayer("bt")


path = "/home/pi/music/"

#bookpl = booksplayer.BooksPlayer(pl, path)
muspl = musicplayer.MusicPlayer(pl, path)

curpl = muspl

curpl.load()
def cli():
    global path, curpl
    inp = ""
    while True:
        print("Press q to quit")
        inp = input()
        if inp is "q":
            break
        elif(inp == "pp"):
            curpl.play_rnd()
        elif inp is "s":
            pl.pause()
        if inp is "p":
            curpl.play()
        if inp is "f":
            curpl.play_forw()
        if inp is "k": #skip
            curpl.on_audio_end()
        if inp.startswith("pl "):
            curpl.play_book(inp[3:])
        if inp.startswith("pp "):
            curpl.play_pos(int(inp[3:]))
        if inp.startswith("save"):
            print("saving player")
            curpl.save()
        if inp.startswith("load"):
            print("load player")
            curpl.load()
        if inp.startswith("cr_pl"):
            print("creating playlist")
            curpl.create_playlist()

def player_update():
    while True:
        pl.update()
        time.sleep(0.06)



thr_player = Thread(target=player_update)
thr_player.setDaemon(True)
thr_player.start()

thr_hardware = Thread(target=hardware.Update)
thr_hardware.setDaemon(True)
thr_hardware.start()

thr_blue_ev = Thread(target=blueh.Update())
thr_blue_ev.setDaemon(True)
thr_blue_ev.start()

thr_cli = Thread(target=cli)
thr_cli.setDaemon(True)
thr_cli.start()
thr_cli.join()


hardware.Exit()
