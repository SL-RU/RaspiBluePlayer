__author__ = 'SL_RU'

### Логика музыкального плеера

import os
import aplayer
import random
import json
import aplayer
import musicplaylist
import audiobook


def log(s):
    print("BOOKS_PLAYER:" + s)


class BooksPlayer(object):
    aplayer = None
    books = list()
    cur_book = None
    path = ""

    def __init__(self, audioPlayer, path):
        self.set_aplayer(audioPlayer)
        self.path = path
        #self.create_playlist()
        self.turn_on()

    def refresh_path(self):
        """Find and enumerate all audio files in the path"""
        self.books = list()
        wa = list(os.walk(self.path))[0]
        for i in wa[1]:
            self.books.append(i)

    def play_audio_by_name(self, name, offset=0):
        if(self.aplayer is not None) and os.path.isfile(self.path + name):
            b = self.aplayer.play_file(self.path + name)
            self.aplayer.set_pos(offset)
            self.cur_song = name
            log("playing" + name)
            return b
        else:
            return False

    def set_aplayer(self, apl):
        if(self.aplayer is not None):
            self.aplayer.turn_off()
        self.aplayer = apl

    def get_aplayer(self):
        return aplayer

    def play_book(self, name):
        """Starting or continueing playing book. If other book playing in this time, it will be saved and stopped"""
        if(self.cur_book is not None):
            self.cur_book.save()
        self.cur_book = audiobook.Audiobook(self, name)
        log("Cur book is " + name)

    def play(self):
        if(self.aplayer is not None):
            self.aplayer.play()

    def pause(self):
        if(self.aplayer is not None):
            self.aplayer.pause()

    def play_forw(self):
        #if(self.cur_book is not None):
        log("lfdfghjk")
        a = self.cur_book.get_next()
        log(a)
        self.play_audio_by_name(a)

    def play_back(self):
        pass

    def load(self):
        #self.load_playlist()
        if(os.path.isfile(self.path + "booksplayer.json")):
            with open(self.path + "booksplayer.json", "r") as fl:
                dt = json.load(fl)
                fl.close()

    def save(self):
        dt = {
            
            }
        #self.save_playlist()
        with open(self.path + "booksplayer.json", "w") as fl:
            json.dump(dt, fl)
            fl.close()

    def turn_on(self):
        self.refresh_path()
        self.aplayer.add_endevent(self.on_audio_end)

    def turn_off(self):
        if(self.aplayer is not None):
            self.aplayer.turn_off()

    def get_type(self):
        return "book_player"

    def on_audio_end(self):
        self.play_forw()

    def play_pos(self, p):
        b = self.cur_book.get_audio_and_time_by_pos(p)
        self.play_audio_by_name(b[0], offset=b[1])
