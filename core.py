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

leds[0].set(True)
leds[1].set(False)

hardware.SetIndLed(leds[1])

curpl = muspl

curpl.load()
muspl.create_playlist()
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
        if inp.startswith("save"):
            print("saving player")
            curpl.save()
        if inp.startswith("load"):
            print("load player")
            curpl.load()

def player_update():
    while True:
        pl.update()
        time.sleep(0.09)

class HardwareControl(object):
    def __init__(self, buttons, leds, blue):
        self.buttons = buttons
        self.leds = leds
        self.blue = blue
        self.init_keys()

    aplayer = None
    playing = False
    player = None

    def init_keys(self):
        self.buttons[4].click = self.play_pause_b
        self.blue.events[2] = self.play_b
        self.blue.events[3] = self.pause_b
        
        self.buttons[6].click = self.skip_b
        self.blue.events[4] = self.skip_b

        self.buttons[8].press = self.halt_p

        self.buttons[7].click = self.conn_b
        self.buttons[5].click = self.forw_b
        
    def play_pause_b(self):
        print("play_pause button")
        if (self.aplayer is not None and self.player is not None):
            if self.aplayer.playing:
                self.player.pause()
            else:
                self.player.play()

    def play_b(self):
        print("Play button")
        if (self.aplayer is not None and self.player is not None):
            self.player.play()

    def pause_b(self):
        if (self.aplayer is not None and self.player is not None):
            self.player.pause()

    def skip_b(self):
        if (self.aplayer is not None and self.player is not None):
            self.player.on_audio_end()

    def forw_b(self):
        print("forw button")
        if (self.aplayer is not None and self.player is not None):
            self.player.play_forw()

    def back_b(self):
        if (self.aplayer is not None and self.player is not None):
            pass

    def conn_b(self):
        print("connect button")
        os.system("sudo bt-audio -c " + headset_MAC)

    def halt_p(self):
        print("halt button")
        os.system("sudo halt")
        
cc = HardwareControl(buttons, leds, blueh)
cc.aplayer = pl
cc.player = curpl
        
thr_player = Thread(target=player_update)
thr_player.setDaemon(True)
thr_player.start()
print("Player thread started")

thr_hardware = Thread(target=hardware.Update)
thr_hardware.setDaemon(True)
thr_hardware.start()
print("hardware thread started")

thr_blue_ev = Thread(target=blueh.Update)
thr_blue_ev.setDaemon(True)
thr_blue_ev.start()
print("Bluetooth headset event's thread started")
thr_blue_ev.join()

#thr_cli = Thread(target=cli)
#thr_cli.setDaemon(True)
#thr_cli.start()
#thr_cli.join()

print("Halting")
hardware.Exit()
