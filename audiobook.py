import os
import json
import mutagen


class Audiobook(object):
    path = ""
    bookpl = None
    audios = list()
    name = ""
    cur_audio = ""
    cur_audio_id = 0
    cur_audio_time = 0
    cur_pos = 0
    
    def __init__(self, bookpl, name):
        self.bookpl = bookpl
        self.path = bookpl.path + name + "/"
        self.name = name
        self.name = self.name[:len(self.name) - 1]
        print(self.name)
        if(not self.load()):
            self.refresh_path()
            self.save()
        print(self.audios)

    def refresh_path(self):
        self.audios = list()
        wa = os.walk(self.path)
        for couple in wa:
            for d in couple[2]:
                if(d.endswith("mp3") or d.endswith("ogg") or d.endswith("wav")):
                    f = os.path.join(couple[0], d)
                    au = mutagen.File(f)
                    self.audios.append((f[len(self.path):], au.info.length))

    def load(self):
        if(os.path.isfile(self.path + "audio_book.json")):
            with open(self.path + "audio_book.json", "r") as fl:
                d = json.load(fl)
                fl.close()
                self.name = d["name"]
                self.audios = d["audios"]
                self.cur_pos = d["pos"]
                return True
        else:
            return False

    def save(self):
        dt = {
            "name": self.name,
            "audios": self.audios,
            "pos": self.cur_pos
        }
        with open(self.path + "audio_book.json", "w") as fl:
            json.dump(dt, fl)
            fl.close()

    def get_cur_file_and_time(self):
        self.cur_audio_id += 1
        return self.local_to_player_path(self.audios[self.cur_audio_id - 1][0])

    def set_cur_state(self, audio="", time=0):
        if(self.cur_audio is audio or self.cur_audio is ""):
            self.cur_pos += time
            self.cur_audio_time = time

    def local_to_player_path(self, fl):
        return (self.path + fl)[len(self.bookpl.path):]

    def player_to_local_path(self, fl):
        return fl[len(self.path) - len(self.bookpl.path):]

    def get_audio_and_time_by_pos(self, pos):
        """Returns list, where zero element is - audio name, and second - requared time.
        If pos is invalid, then None
        pos - time in seconds from beginning of book"""
        i = 0
        p = pos
        while p - self.audios[i][1] > 0:
            p -= self.audios[i][1]
            if(i + 1 < len(self.audios)):
                i += 1
            else:
                return None
        return (self.local_to_player_path(self.audios[i][0]), p)
