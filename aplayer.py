__author__ = 'SL_RU'

###Проигрыватель музыкальных файлов

import pyglet, time

def init():
    global cur_player, song_loading
    cur_player = None
    song_loading = False
    pass

def play_file(file):
    global cur_player, song_loading
    while song_loading:
        time.sleep(0.3)
    print("PLAY: requested file " + file)
    song_loading = True
    music = pyglet.media.load(file)
    if(cur_player == None):
        pla = music.play()
        cur_player = pla
    else:
        #cur_player.pause()
        cur_player.queue(music)
        cur_player.next()
        #cur_player.play()
    song_loading = False
    print("PLAY: playing")
    return cur_player

def pause():
    global cur_player
    if(cur_player != None):
        cur_player.pause()
def play():
    global cur_player
    if(cur_player != None):
        cur_player.play()


def set_endevent(func):
    #m.music.set_endevent(func)
    pass
