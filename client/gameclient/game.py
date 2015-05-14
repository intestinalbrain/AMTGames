# coding: utf-8

from threading import Thread

import time

class Group(Thread):
    ISPLAYING = 1
    ISPAUSED = 3
    def __init__(self, group_id):
        Thread.__init__(self)
        self._group_id = group_id
        self._players = []
        self._status = 0
    
    
    def append_player(self, player):
        self._player = player
    
    
    def start(self):
        self._status |= self.ISPLAYING
        while self.is_playing:
            if not self.is_paused:
                pass
    
    
    @property
    def is_playing(self):
        return (self._status & self.ISPLAYING) == self.ISPLAYING
    
    @property
    def is_paused(self):
        return (self._status & self.PAUSED) == self.PAUSED
        

class Game(object):
    def __init__(self):
        self._round = 0
        self._timer = None
        self._is_playing = False
    
    def start(self):
        self._register_player()
        self._group_players()
        self._is_playing = True
        while self._is_playing:
            self._start_tour()
            time.sleep(120)
            self._show_results()
            self._next_tour()
        self._exit()
    
    def pause(self):
        self._is_playing = False
        for group in self._groups:
            group.pause()
    
    def stop(self):
        for group in self._groups:
            group.stop()
            
