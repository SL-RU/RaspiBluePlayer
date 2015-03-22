__author__ = 'sl_ru'

import os, time
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

import cherrypy, json
from mako.template import Template
from mako.lookup import TemplateLookup

lookup = TemplateLookup(directories=['html'])

class MusicPlayerWeb(object):
    def __init__(self, musicPlayer):
        self.muPlayer = musicPlayer
        self.last_play_click = time.time()

    def index(self):
        mytemplate = lookup.get_template("music/index.html")
        return mytemplate.render()
    index.exposed = True

    def list(self):
        mytemplate = lookup.get_template("music/music_list.html")
        return mytemplate.render()
    list.exposed = True

    def player(self):
        mytemplate = lookup.get_template("music/music_player.html")
        return mytemplate.render(current=self.muPlayer.current_song)
    player.exposed = True

    def play_rnd(self):
        self.muPlayer.play_rnd()
        self.last_play_click = time.time()
    play_rnd.exposed = True

    def play_song(self, id):
        self.muPlayer.play_song(self.muPlayer.musics_all[int(id)])
        self.last_play_click = time.time()
    play_song.exposed = True

    def pause(self):
        self.muPlayer.pause()
    pause.exposed = True
    def play(self):
        self.muPlayer.play()
    play.exposed = True

    @cherrypy.tools.json_out()
    def get_player_data(self):
        return {'current_track': self.muPlayer.current_song,
                'cur_time': self.muPlayer.get_pos()}
    get_player_data.exposed = True

    @cherrypy.tools.json_out()
    def get_music_list_data(self):
        return {'all': self.muPlayer.musics_all,
                'current': self.muPlayer.current_song,
                'excluded': self.muPlayer.musics_excluded}

    get_music_list_data.exposed = True

    def upload_music(self):
        mytemplate = lookup.get_template("music/upload_music.html")
        return mytemplate.render()
    upload_music.exposed = True
    #@cherrypy.tools.json_in()
    def upload_file(self,file):
        all_data = bytearray()
        while True:
            data = file.file.read(8192)
            all_data += data
            if not data:
                break
        print(file.filename)
        if(not os.path.isdir(self.muPlayer.path + "/uploads")):
            os.mkdir(self.muPlayer.path + "/uploads")
        path = self.muPlayer.path + "/uploads/" + file.filename
        if(os.path.isfile(path)):
            ind = 0
            while(os.path.isfile(path)):
                path = self.muPlayer.path + "/uploads/" + str(ind) + file.filename
                ind += 1
        fl = open(path, "wb")
        fl.write(all_data)
        fl.close()
        self.muPlayer.add_file(path)
        return 'File ' + path + "uploaded!"
    upload_file.exposed = True


class WebIndex(object):
    def index(self):
        mytemplate = lookup.get_template("index.html")
        return mytemplate.render()
    index.exposed = True





def start(musicPlayer):
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    tutconf = os.path.join(os.path.dirname(__file__), 'web.conf')
    root = WebIndex()
    root.music = MusicPlayerWeb(musicPlayer)
    root.music.exposed = True
    cherrypy.quickstart(root, config=tutconf)
    cherrypy.engine.start()
