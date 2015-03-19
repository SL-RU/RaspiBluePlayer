__author__ = 'SL_RU'

###Проигрыватель музыкальных файлов

import pyglet, time, sys

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
    try:
        song_loading = True
        music = pyglet.media.load(file)
        if(cur_player == None):
            pla = music.play()
            cur_player = pla
        else:
            cur_player.pause()
            cur_player.queue(music)
            cur_player.next()
            cur_player.play()
        song_loading = False
    except:
        print("PLAY: error " + str(sys.exc_info()[0]))
    else:
        print("PLAY: playing")


def pause():
    global cur_player
    if(cur_player != None):
        cur_player.pause()
def play():
    global cur_player
    if(cur_player != None):
        cur_player.play()


def set_endevent(func):
    global cur_player, end_event
    if(cur_player != None):
        end_event = func

end_check_time = 0.5
def update():
    global cur_player, end_event, end_check_time
    if(cur_player != None):
        if(cur_player.time + end_check_time >= cur_player.source.duration):
            if(end_event != None):
                end_event()
