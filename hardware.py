__author__ = 'SL_RU'

import RPi.GPIO as GPIO
import time
from threading import Thread

##Взаимодействие с gpio, блютус и прочим хардваре
IS_GPIO = False

def Init():
    global thread
    if(IS_GPIO):
        GPIO.setmode(GPIO.BCM)
    thread = Thread(target=Update)
    thread.setDaemon(True)
    thread.start()
def Exit():
    if(IS_GPIO):
        GPIO.cleanup()
elements = []
def Update():
    global elements
    while True:
        for e in elements:
            e.Update()
        time.sleep(0.01)
def AddElement(el):
    global elements
    elements.append(el)
def RemoveElemment(el):
    global elements
    elements.remove(el)

class GPIOButton(object):
    def __init__(self, pin):
        if(IS_GPIO):
            GPIO.setup(pin, GPIO.IN)
        self.pin = pin
        AddElement(self)
    pin = 0
    last_state = 0
    press_count = 0
    SHORT_press_count = 20
    LONG_press_count = 100
    def Update(self):
        st = False
        if(IS_GPIO):
            st = GPIO.input(self.pin)
            #print(st)
        if(st):
            self.press_count += 1
        else:
            if(self.press_count > self.SHORT_press_count):
                if(self.press_count > self.LONG_press_count):
                    if(self.on_long_press != None):
                        self.on_long_press()
                else:
                    if(self.on_press != None):
                        self.on_press()
            self.press_count = 0
    on_press = None
    on_long_press = None
