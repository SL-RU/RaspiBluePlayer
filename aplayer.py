__author__ = 'SL_RU'
# -*- coding: utf-8 -*-
#Проигрыватель музыкальных файлов

import vlc
#import time
#import sys
from queue import Queue


def log(msg):
    print(msg)


class Aplayer(object):
    def __init__(self, output_device):
        """Initializing Aplayer.
            output_device can be:
               'bt' - blutooth,
               'hw' - audio jack,
               'hdmi'
            """
        self.init_functions()
        self.vlc_instance = vlc.Instance()
        self.cur_player = self.vlc_instance.media_player_new()
#        if(output_device == "bt"):
#            self.cur_player.audio_output_device_set('alsa', 'bluetooth')
        self.tasks = Queue()
        self.song_loading = False
        self.cur_media = None

    def connect_bluetooth(self, a):
        self.cur_player.audio_output_device_set('alsa', 'bluetooth')

    def _play_file(self, fl):
        print("PLAY: requested file " + fl)
        self.song_loading = True
        self.cur_media = self.vlc_instance.media_new(fl)
        self.cur_player.set_media(self.cur_media)
        self.cur_player.set_position(0)
        self.cur_player.play()
        self.song_loading = False

    def play_file(self, fl):
        """Load and play requested media file"""
        self._add_task('play_file', fl)

    def _pause(self, a=0):
        if(self.cur_player is not None):
            self.cur_player.pause()

    def pause(self):
        """Pause playing media"""
        self._add_task('pause', 0)

    def _play(self, a=0):
        if(self.cur_player is not None):
            self.cur_player.play()

    def play(self):
        """Continue playing after pause()"""
        self._add_task('play', None)

    def _add_endevent(self, func):
        if(self.cur_player is not None):
            self.cur_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, func)

    def add_endevent(self, func):
        """Set function, which will be executed after audio file's end.
            func - function, which will be executed"""
        self._add_task('add_endevent', func)

    def _rem_endevent(self, func):
#implement!
        pass

    def rem_endevent(self, func):
        self._add_task("rem_endevent")

    def _set_pos(self, pos):
        #global self.cur_player
        if(self.cur_player != None and pos >= 0 and pos <= 1):
            self.cur_player.set_position(pos)
    def set_pos(self, pos):
       self._add_task('set_pos', pos)
    
    def _set_pos(self, pos):
        #global self.cur_player
        if(self.cur_player != None and pos >= 0 and pos <= 1):
            self.cur_player.set_position(pos)
    def set_pos(self, pos):
       self._add_task('set_pos', pos)
    
    def get_pos(self):
        #global self.cur_player
        return self.cur_player.get_position()
    def get_duration(self):
        #global self.cur_player, self.cur_media
        if(self.cur_media != None):
            return self.cur_media.get_duration() / 1000

    def _add_task(self, func, arg):
        self.tasks.put((func, arg))
        log('APLTASK: added ' + func)

    def init_functions(self):
        self.functions = {
            'play_file': self._play_file,
            'pause': self._pause,
            'add_endevent': self._add_endevent,
            'play': self._play,
            'set_pos': self.set_pos,
            'rem_endevent': self._rem_endevent,       
        }

    def update(self):
        #global self.tasks, functions
        f = self.tasks.get()
        print(self.functions)
        print(f)
        print('APLTASK: doing ' + f[0])
        self.functions[f[0]](f[1])
        print('APLTASK: done')
        self.tasks.task_done()
