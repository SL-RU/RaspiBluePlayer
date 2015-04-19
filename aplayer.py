__author__ = 'SL_RU'

###Проигрыватель музыкальных файлов

import vlc, time, sys
from queue import Queue

def log(msg):
    if not (msg.startswith('APLTASK')):
        print(msg)

IS_BLUETOOTH_ALSA=False
IS_LINUX=True

def init():
    global cur_player, song_loading, vlc_instance, tasks, IS_BLUETOOTH_ALSA, cur_media
    vlc_instance = vlc.Instance()
    cur_player = vlc_instance.media_player_new()
    if(IS_BLUETOOTH_ALSA):
        cur_player.audio_output_device_set('alsa', 'bluetooth')
    tasks = Queue()
    song_loading = False
    cur_media = None
    pass

def conn():
    _add_task("conn", None)
def connect_bluetooth(a):
    global cur_player
    cur_player.audio_output_device_set('alsa', 'bluetooth')

def _play_file(file):
    global cur_player, song_loading, vlc_instance, cur_media
    print("PLAY: requested file " + file)
    #try:
    song_loading = True
    if(not IS_LINUX):
        file = str(file.encode('utf-8').decode('cp1251'))
    cur_media = vlc_instance.media_new(file)
    #cur_player.stop()
    cur_player.set_media(cur_media)
    cur_player.set_position(0)
    cur_player.play()
    #except:
    #    print("PLAY: error " + str(sys.exc_info()[0]))
    #else:
    #    print("PLAY: playing")
    song_loading = False
def play_file(file):
    _add_task('play_file', file)

def _pause(a):
    global cur_player
    if(cur_player != None):
        cur_player.pause()
def pause():
    _add_task('pause', None)

def _play(a):
    global cur_player
    if(cur_player != None):
        cur_player.play()
def play():
    _add_task('play', None)

def _set_endevent(func):
    global cur_player
    if(cur_player != None):
        cur_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, func)
def set_endevent(func):
    _add_task('set_endevent', func)

def _set_pos(pos):
    global cur_player
    if(cur_player != None and pos >= 0 and pos <= 1):
        cur_player.set_position(pos)
def set_pos(pos):
    _add_task('set_pos', pos)

def _set_pos(pos):
    global cur_player
    if(cur_player != None and pos >= 0 and pos <= 1):
        cur_player.set_position(pos)
def set_pos(pos):
    _add_task('set_pos', pos)

def get_pos():
    global cur_player
    return cur_player.get_position()
def get_duration():
    global cur_player, cur_media
    if(cur_media != None):
        return cur_media.get_duration() / 1000


def _add_task(func, arg):
    global tasks
    tasks.put((func, arg))
    log('APLTASK: added ' + func)

functions = {
    'play_file' : _play_file,
    'pause' :_pause,
    'set_endevent' :_set_endevent,
    'play' : _play,
    'set_pos' : set_pos,
    'conn' : connect_bluetooth,
}

def update():
    global tasks, functions
    f = tasks.get()
    log('APLTASK: doing ' + f[0])
    functions[f[0]](f[1])
    log('APLTASK: done')
    tasks.task_done()
