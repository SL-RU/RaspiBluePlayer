import os
import json
import mutagen


class Audiobook(object):
    path = ""
    bookpl = None
    audios = list()
    name = ""
    cur_id = 0
    
    def __init__(self, bookpl, name):
        self.bookpl = bookpl
        self.path = bookpl.path + name + "/"
        self.name = name
        self.name = self.name[:len(self.name) - 1]
        print(self.name)
        self.refresh_path()

    def refresh_path(self):
        self.audios = list()
        wa = os.walk(self.path)
        for couple in wa:
            for d in couple[2]:
                if(d.endswith("mp3") or d.endswith("ogg") or d.endswith("wav")):
                    f = os.path.join(couple[0], d)
                    au = mutagen.File(f)
                    self.audios.append((f[len(self.path):], au.info.length))
        print(self.audios)

    def get_next(self):
        self.cur_id += 1
        return self.local_to_player_path(self.audios[self.cur_id - 1][0])

    def local_to_player_path(self, fl):
        return (self.path + fl)[len(self.bookpl.path):]

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
