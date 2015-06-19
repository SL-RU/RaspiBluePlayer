#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'SL_RU'

##главный файл. Точка входа

import time, os, sys, getopt

def set_output_to_file(path):
    fl = open(path, "a", 1)
    sys.stdout = sys.stderr = fl

try:
    opts, args = getopt.getopt(sys.argv[1:],"hl:")
except:
    print("Invalid args\nRaspiBluePlayer by SL_RU.\n-l <logfile>")
    sys.exit(2)

LOG_TO_FILE = False
LOG_FILE = ""

for opt, arg in opts:
    if opt == '-h':
        print("-l <logfile>")
        sys.exit()
    elif opt == "-l":
        LOG_TO_FILE = True
        LOG_FILE = arg

if LOG_TO_FILE:
    try:
        set_output_to_file(LOG_FILE)
    except:
        print("ERROR: couldn't set log to requested file")
        LOG_TO_FILE = False

from threading import Thread
import subprocess
from datetime import datetime
import aplayer
import musicplayer
import booksplayer
import hardware
import bluetooth_headset
import lcd_interface


print("\n\n\nST: ", datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"))
print("RaspiBluePlayer starting")
print("Author: SL_RU <sl_ru@live.com>")


hardware.Init()
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


lcd = lcd_interface.LcdInterface()

path = "/home/pi/music/"
lcd.text(0, 0, "Music path:")
lcd.text(0, 10, path)


#bookpl = booksplayer.BooksPlayer(pl, path)
muspl = musicplayer.MusicPlayer(pl, path)

leds[0].set(False)
leds[1].set(False)

hardware.SetIndLed(leds[1])

curpl = muspl

curpl.load()
#muspl.create_playlist()
def cli():
    global path, curpl, leds
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
        if inp.startswith("cr"):
            curpl.create_playlist()
        leds[0].blink(0.2)

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
        self.blue.events[2] = self.play_pause_b
        self.blue.events[3] = self.play_pause_b
        
        self.buttons[6].click = self.skip_b
        self.blue.events[4] = self.skip_b

        self.buttons[8].press = self.halt_p

        self.buttons[7].click = self.conn_b
        self.buttons[5].click = self.forw_b
        
    def play_pause_b(self):
        print("play_pause button")
        hardware.PressIndicate()
        if (self.aplayer is not None and self.player is not None):
            if self.aplayer.playing:
                self.player.pause()
            else:
                self.player.play()

    def skip_b(self):
        hardware.PressIndicate()
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
        subprocess.call("sudo bt-audio -c " + headset_MAC, stdout=sys.stdout)

    def halt_p(self):
        print("halt button")
        if(self.player is not None):
            self.player.save()
        subprocess.call("sudo halt", stdout=sys.stdout)
        
        
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


if not LOG_TO_FILE:
    thr_cli = Thread(target=cli)
    thr_cli.setDaemon(True)
    thr_cli.start()
    thr_cli.join()
else:
    thr_blue_ev.join()

if(curpl is not None):
    curpl.save()

print("Halting")
hardware.Exit()
print("END: ", datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"))

if LOG_TO_FILE:
    sys.stdout.close()