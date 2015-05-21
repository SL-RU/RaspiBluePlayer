__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random
import json
import aplayer
import musicplaylist

def log(s):
    print("MUSIC_PLAYER:" + s)

class MusicPlayer(object):
    aplayer = None
    songs = list()
    cur_song = ""
    path = ""
    cur_playlist = None
    
    def __init__(self, audioPlayer, path):
        self.set_aplayer(audioPlayer)
        self.path = path
        self.create_playlist()
        self.turn_on()

    def refresh_path(self):
        """Find and enumerate all audio files in the path"""
        self.songs = list()
        wa = os.walk(self.path)
        for couple in wa:
            for f in couple[2]:
                if(f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')):
                    self.add_file(couple[0] + "/" + f)

    def add_file(self, f):
        if (f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.ogg')) and f.startswith(self.path):
#            leng = len(self.musics_all.values())
            self.songs.append(f[len(self.path):])
            log(f[len(self.path):])

    def play_audio_by_name(self, name):
        if(aplayer is not None) and os.path.isfile(self.path + name):
            b = self.aplayer.play_file(self.path + name)
            self.cur_song = name
            return b
        else:
            return False

    def set_aplayer(self, apl):
        if(self.aplayer is not None):
            self.aplayer.turn_off()
        self.aplayer = apl

    def get_aplayer(self):
        return aplayer

    def play(self):
        if(self.aplayer is not None):
            self.aplayer.play()

    def pause(self):
        if(self.aplayer is not None):
            self.aplayer.pause()

    def play_forw(self):
        if self.cur_playlist is not None:
            s = self.cur_playlist.get_cur_song()
            if s is not None:
                self.play_song_by_name(s)

    def play_back(self):
        pass

    def load(self):
        self.load_playlist()
        if(os.path.isfile(self.path + "booksplayer.json")):
            with open(self.path + "booksplayer.json", "r") as fl:
                dt = json.load(fl)
                fl.close()

    def save(self):
        dt = {
            }
        self.save_playlist()
        with open(self.path + "booksplayer.json", "w") as fl:
            json.dump(dt, fl)
            fl.close()

    def turn_on(self):
        self.refresh_path()
        self.aplayer.add_endevent(self.on_song_end)

    def turn_off(self):
        if(self.aplayer is not None):
            self.aplayer.turn_off()

    def get_type(self):
        return "book_player"

    def on_audio_end(self):
        self.play_forw()
