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

    def play_song_by_name(self, name):
        if(aplayer is not None) and os.path.isfile(self.path + name):
            b = self.aplayer.play_file(self.path + name)
            self.cur_song = name
            return b
        else:
            return False

    def play_song_by_id(self, id):
        self.play_song_by_name(self.songs[id])

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
        if(os.path.isfile(self.path + "musicplayer.json")):
            with open(self.path + "musicplayer.json", "r") as fl:
                dt = json.load(fl)
                self.play_song_by_name(dt["cur_song"])
                fl.close()

    def save(self):
        dt ={
            "cur_song": self.cur_song,
            }
        self.save_playlist()
        with open(self.path + "musicplayer.json", "w") as fl:
            json.dump(dt, fl)
            fl.close()

    def turn_on(self):
        self.refresh_path()
        self.aplayer.add_endevent(self.on_audio_end)

    def turn_off(self):
        if(self.aplayer is not None):
            self.aplayer.turn_off()

    def get_type(self):
        return "music_player"

    def create_playlist(self):
        self.cur_playlist = musicplaylist.RandomPlaylist(self)

    def load_playlist(self, fl=None):
        if(fl is None):
            fl = self.path + "last_playlist.json"
        log("Loading cur playlist from file " + fl)
        self.set_cur_playlist(musicplaylist.load_playlist(fl, self))

    def set_cur_playlist(self, playlist):
        self.cur_playlist = playlist

    def save_playlist(self, fl=None):
        if(fl is None):
            fl = self.path + "last_playlist.json"
        log("Saving cur playlist in file " + fl)
        if(self.cur_playlist is not None):
            self.cur_playlist.save(fl)

    def on_audio_end(self):
        if(self.cur_playlist is not None):
            self.cur_playlist.song_played(self.cur_song)
            self.play_forw()
