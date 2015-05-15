# coding: utf-8

from threading import Thread
from datetime import datetime
import time
import sys

import requests

from settings import (TOUR_TIME, 
                      GROUP_COUNT, 
                      PLAYER_COUNT, 
                      URL_PREFIX, 
                      THREAD_COUNT)

from player import Player


class Worker(Thread):
    def __init__(self, players, start_position=0):
        Thread.__init__(self)
        self._players = players
        self._players_count = len(self._players)
        self._is_run = False
        self._start_position = start_position
    
    def run(self):
        self._is_run = True
        position = self._start_position
        while self._is_run:
            now = datetime.now()
            if position == self._players_count:
                position = 0
            player = self._players[position]
            if not player.sleep(now):
                if not player.attack():
                    break
            position += 1
            
    def stop(self):
        self._is_run = False


class Game(object):
    def __init__(self):
        self._players = []
        self._groups = []
        self._workers = []
    
    def start(self):
        self._register_players()
        self._start_tour()
        self._actualize_players()
        self.workers()
        self._wait_loop()
        self._show_results()
        self._exit()
    
    def workers(self):
        start_position = 0
        for thread_id in xrange(THREAD_COUNT):
            worker = Worker(self._players, start_position+thread_id*3)
            worker.start()
            self._workers.append(worker)
    
    def stop(self):
        for worker in self._workers:
            worker.stop()
            worker.join()
    
    def _wait_loop(self):
        while any([worker.is_alive() for worker in self._workers]):
            time.sleep(0.5)
        self.stop()
    
    
    def _exit(self):
        print 'Good bye'
    
    def _start_tour(self):
        requests.post('/'.join([URL_PREFIX, 
                                'tournament', 
                                str(time.mktime(datetime.now().timetuple()))]))
    
    def _show_results(self):
        for group_id in self._groups:
            results = requests.get('/'.join([URL_PREFIX, 'tournament', str(group_id)])).json()
            print self._format_results(results, group_id)
    
    def _format_results(self, results, group_id):
        lines = []
        lines.append(u'Group №%s' % group_id)
        for position, winner in enumerate(results['winners']):
            lines.append('%s. %s - %s' % (position+1, winner['name'], winner['medals']))
        lines.append('Not attacked: %s' % results['not_attacked_count'])
        lines.append('*'*40)
        return '\n'.join(lines)
    
    def _register_players(self):
        self._players = [self._init_player(Player()) for _ in xrange(PLAYER_COUNT)]
            
    def _init_player(self, player):
        player.initialize()
        result = requests.post('/'.join([URL_PREFIX, 'player', player.post_url_format])).json()
        player.uuid = result['uuid']
        return player
    
    def _actualize_players(self):
        for player in self._players:
            response = requests.get('/'.join([URL_PREFIX, 'player', player.uuid])).json()
            group_id = response['group_id']
            group_id in self._groups or self._groups.append(group_id)
            player.initialize(response)
