import os
import random
import json

class Playlist:
    def __init__(self, musicpl):
        """musicpl - musicplayer"""
        pass

#song - local path to song file, used by misicplayer. Global path must be musicplayer.path + song
    
    def add_song(self, song):
        """Add songs to list wanted to play"""
        pass

    def remove_song(self, song):
        """remove song from wanted to play"""
        pass

    def get_cur_song(self, song):
        """get song, which must be playing now. If there is that song, then returns song, else - None"""
        pass

    def song_played(self, song):
        """Need to call, when song was played."""
        pass

    def get_songs_played(self):
        """Returns list of songs, which were played already"""
        pass

    def get_future_songs(self):
        """Returns list of songs, which planned be played"""
        pass

    def save(self, f):
        pass

    def load(self, f):
        pass

    def get_name(self):
        pass

    def set_name(self):
        pass

    def get_type(self):
        pass

class RandomPlaylist(Playlist):
    played_songs = list()
    cur_song = None
    musicpl = None
    name = ""
    
    def __init__(self, musicpl):
        """musicpl - musicplayer"""
        self.musicpl = musicpl

#song - local path to song file, used by misicplayer. Global path must be musicplayer.path + song

    def add_song(self, song):
        """Add songs to list wanted to play"""
        if(song in self.played_songs):
            self.played_songs.remove(song)

    def remove_song(self, song):
        """remove song from wanted to play"""
        if(song not in self.played_songs):
            self.played_songs.append(song)

    def get_cur_song(self):
        """get song, which must be playing now. If there is that song, then returns song, else - None"""
        if(self.cur_song is not None):
            return self.cur_song
        else:
            n = len(self.musicpl.songs) - len(self.played_songs)
            if n > 0:
                i = random.randint(1, n)
                for j in self.musicpl.songs:
                    if(j not in self.played_songs):
                        i -= 1
                        if i <= 0:
                            self.cur_song = j
                            return j
        return None

    def song_played(self, song):
        """Need to call, when song was played."""
        self.played_songs.append(song)
        self.cur_song = None

    def get_songs_played(self):
        """Returns list of songs, which were played already"""
        return self.played_songs

    def get_future_songs(self):
        """Returns list of songs, which planned be played"""
        if len(self.played_songs) == 0:
            return self.musicpl.songs
        else:
            l = list()
            for j in self.musicpl.songs:
                if j not in self.played_songs:
                    l.append(j)
            return l

    def load(self, f):
        with open(f, "r") as fl:
            d = json.load(fl)
            self.name = d["name"]
            self.cur_song = d["cur_song"]
            self.played_songs = d["played_songs"]

    def save(self, f):
        dt = {
            "type": self.get_type(),
            "name": self.get_name(),
            "cur_song": self.cur_song,
            "played_songs": self.played_songs
        }
        with open(f, "w") as fl:
            json.dump(dt, fl)
            fl.close()
    
    def get_name(self):
        return self.name

    def set_name(self, n):
        self.name = n

    def get_type(self):
        return "random"

def load_playlist(p, mupl):
    """Loads playlist from save.
    p - path to file
    mupl - musicplayer
    If loaded - return playlist
    else - None"""
    if(os.path.isfile(p)):
        with open(p, "r") as fl:
            tp = json.load(fl)
            fl.close()
            if tp['type'] == "random":
                pl = RandomPlaylist(mupl)
                pl.load(p)
                return pl
    return None
