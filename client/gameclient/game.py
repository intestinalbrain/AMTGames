# coding: utf-8

from threading import Thread
import time

import requests

from settings import TOUR_TIME, GROUP_COUNT, PLAYER_COUNT, URL_PREFIX
from player import Player
        

class Game(object):
    def __init__(self):
        self._round = 0
        self._timer = None
        self._is_playing = False
        self._groups = []
    
    def start(self):
        self._register_players()
        self._is_playing = True
        while self._is_playing:
            self._start_tour()
            time.sleep(TOUR_TIME)
            self._show_results()
            self._next_tour()
        self._exit()
    
    def pause(self, value):
        for group in self._groups:
            group.pause(value)
    
    def stop(self):
        self._is_playing = False
        for group in self._groups:
            group.stop()
    
    def _start_tour(self):
        self.pause(False)
    
    def _show_results(self):
        for group in self._groups:
            print group.get_results()
    
    def _register_players(self):
        player_list = []
        for x in xrange(PLAYER_COUNT):
            player = self.init_player(Player())
    
    def init_player(self, player):
        response = requests.get('/'.join([URL_PREFIX, player.uuid])).json()
        if 'new' in response:
            player.initialize()
            requests.post('/'.join([URL_PREFIX, player.post_url_format]))
        else:
            player.initialize(response)
