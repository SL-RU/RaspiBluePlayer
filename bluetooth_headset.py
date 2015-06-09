from evdev import InputDevice, list_devices
from threading import Thread
import time

class BluetoothHeadsetEvents(object):
    def __init__(self, name):
        self.name = name
        
    name = "" #evdev name of headset. Usually - MAC address
    is_connected = False
    dev = None

    #events:
    #0 - connected
    #1 - disconnected
    #2 - Play
    #3 - Pause
    #4 - next
    #5 - back
    events = [None, None, None, None, None, None]

    event_codes = ["conn", "disconn", 200, 201, 165, 163]
    
    def check_connection(self):
        devices = [InputDevice(fn) for fn in list_devices()]
        for dev in devices:
            self.is_connected = (self.name in dev.name)
            if self.is_connected:
                self.dev = dev
                break
            else:
                self.dev = None
        return self.is_connected
    
    def rise_event(self, ev_code):
        e = self.events[self.event_codes.index(ev_code)]
        print("Event code: ", ev_code)
        if e is not None:
            e()
            
    def Update(self):
        last_code = -1
        last_event_time = -100
        last_connection_check_time = -100
        while True:
            if (last_connection_check_time + 3 < time.time()):
                l = self.is_connected
                if l is not self.check_connection():
                    if l:
                        self.rise_event("disconn")
                    else:
                        self.rise_event("conn")
                        self.dev.grab()
                last_connection_check_time = time.time()
            try:
                if(self.is_connected):
                    for i in self.dev.active_keys():
                        if i in self.event_codes and (time.time() > last_event_time + 0.6 or last_code is not i):
                            last_event_time = time.time()
                            last_code = i
                            self.rise_event(i)
            except:
                last_connection_check_time = -100
            time.sleep(0.01)

b = BluetoothHeadsetEvents("00:11:67:11:11:8C")
th = Thread(target=b.Update)
th.start()
th.join()
dev.ungrab()
