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


class core(object):
    def __init__(self):
        self.init_hardware()
        self.init_lcd()
        self.connect_bt()
        self.init_aplayer()
        self.init_gui_events()
        self.start_threads()
        self.start_player()
        

    cur_player = None    
    aplayer = None
    
    #Button's pins, connected to GPIO.
    #physical placement:
    # 0 1   5 6
    #     4 
    # 2 3   7 8                
    button_pins = [21, 19, 23, 26, 18, 13, 11, 16, 15]
    #Led's pins.
    # Left's id - 0, right's - 1
    led_pins = [24, 22]
    buttons = None
    leds = None
    
    #Bluetooth headset MAC. Needed to connecting and listening events
    headset_MAC = "00:11:67:11:11:8C"
    blueh = None #Bluetooth headset events


    gui = None
    
    
    def init_hardware(self):
        hardware.Init()
        
        self.buttons = []
        for i in range(len(self.button_pins)):
            self.buttons.append(hardware.GPIOButton(self.button_pins[i]))

        self.leds = []
        for i in range(len(self.led_pins)):
            self.leds.append(hardware.GPIOLed(self.led_pins[i]))

        self.leds[0].set(False)
        self.leds[1].set(False)

        hardware.SetIndLed(self.leds[1])

    def connect_bt(self):
        self.blueh = bluetooth_headset.BluetoothHeadsetEvents(self.headset_MAC)
        
    def init_aplayer(self):
        self.aplayer = aplayer.Aplayer("hw")

    def init_lcd(self):
        gui = lcd_interface.LcdInterface()
        #Blah blah
    
    def init_gui_events(self):
        self.buttons[8].press = self.halt
        
        ev = [[lambda:self._on_gui_event("up"), lambda:self._on_gui_event("back")],
              [lambda:self._on_gui_event("ok"), lambda:self._on_gui_event("ok")],
              [lambda:self._on_gui_event("down"), lambda:self._on_gui_event("forw")],
              [lambda:self._on_gui_event("info"), lambda:self._on_gui_event("set")],
              
              [lambda:self._on_player_event("play"),lambda:self._on_player_event("stop")],
              
              [lambda:self._on_player_event("scroll_b"),lambda:self._on_player_event("song_back")],
              [lambda:self._on_player_event("scroll_f"),lambda:self._on_player_event("song_forw")],
              [lambda:self._on_player_event("play"),lambda:self._on_player_event("stop")]]
        for i in range(len(ev)):
            self.buttons[i].click = ev[i][0]
            self.buttons[i].press = ev[i][1]

            
    def _on_gui_event(self, ev):
        if self.gui.is_on:
            self.gui.input(ev)
        else:
            self.gui.on_off(True)
    def _on_player_event(self, ev, val=0):
        self.cur_player.input(ev, val)
        
        
    #Threads:
    thr_player = None       #aplayer thread
    thr_hardware = None     #hardware thread
    thr_blue_ev = None      #bluetooth thread
    
    def start_threads(self):
        #aplayer thread
        def aplayer_update():
            while True:
                self.aplayer.update()
                time.sleep(0.09)
        self.thr_player = Thread(target=aplayer_update)
        self.thr_player.setDaemon(True)
        self.thr_player.start()
        print("Player thread started")

        #hardware thread
        self.thr_hardware = Thread(target=hardware.Update)
        self.thr_hardware.setDaemon(True)
        self.thr_hardware.start()
        print("hardware thread started")

        #bluetooth thread
        self.thr_blue_ev = Thread(target=self.blueh.Update)
        self.thr_blue_ev.setDaemon(True)
        self.thr_blue_ev.start()
        print("Bluetooth headset event's thread started")

    def start_player(self):
        self.cur_player = musicplayer.MusicPlayer(self.aplayer, "/home/pi/music")                
        
    def connect_bluetooth(self):
        print("connect button")
        subprocess.call("sudo bt-audio -c " + self.headset_MAC, stdout=sys.stdout)
        
    def halt(self):
        print("halt button")
        if(self.player is not None):
            self.player.save()
        subprocess.call("sudo halt", stdout=sys.stdout)
 

        
cr = core()
cr.thr_blue_ev.join()
#if LOG_TO_FILE:

if(curpl is not None):
    curpl.save()

print("Halting")
hardware.Exit()
print("END: ", datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"))

if LOG_TO_FILE:
    sys.stdout.close()