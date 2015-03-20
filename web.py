__author__ = 'sl_ru'

import os, time
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

import cherrypy
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
        return mytemplate.render(rows=self.muPlayer.musics,  current=self.muPlayer.current_song)
    list.exposed = True

    def player(self):
        mytemplate = lookup.get_template("music/music_player.html")
        return mytemplate.render(current=self.muPlayer.current_song)
    player.exposed = True

    def play_rnd(self):
        self.muPlayer.play_rnd()
        self.last_play_click = time.time()
        raise cherrypy.HTTPRedirect("./")
    play_rnd.exposed = True

    def play_song(self, id):
        self.muPlayer.play_song(self.muPlayer.musics[int(id)])
        self.last_play_click = time.time()
        raise cherrypy.HTTPRedirect("./list")
    play_song.exposed = True

    def pause(self):
        self.muPlayer.pause()
        raise cherrypy.HTTPRedirect("./")
    pause.exposed = True
    def play(self):
        self.muPlayer.play()
        raise cherrypy.HTTPRedirect("./")
    play.exposed = True



class WebIndex(object):
    def index(self):
        mytemplate = lookup.get_template("index.html")
        return mytemplate.render()
    index.exposed = True

    def upload(self, myFile):
        out = """<html>
        <body>
            Uploaded: %s<br />
            Thank you! =D
        </body>
        </html>"""

        fl = open("E:\\music\\"+myFile.filename, "wb")
        fl.write(myFile.file.read())

        return out % (myFile.filename, myFile.content_type)
    upload.exposed = True




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
