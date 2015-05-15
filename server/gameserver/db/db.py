# coding: utf-8

import random
import uuid

from flask import g
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from threading import Lock

class Database(object):
    lock = Lock()
    
    def __init__(self):
        self._players = []
        self._uuid_index = {}
        self._group_index = {}
        self._timestamp = None
    
    def add(self, player):
        with self.lock:
            uuid_ = uuid.uuid4().urn
            player['uuid'] = uuid_
            self._players.append(player)
            self._group_index.setdefault(player.get('group_id'), []).append(uuid_)
            self._uuid_index[uuid_] = len(self._players)-1
            return uuid_
    
    def update(self, data):
        with self.lock:
            uuid = data['uuid']
            player = self._players[self._uuid_index[uuid]]
            old_group = player.get('group_id')
            new_group = data.get('group_id')
            if old_group != new_group:
                values = self._group_index[old_group]
                values.remove(uuid)
                self._group_index.setdefault(new_group, []).append(uuid)
            for key, value in data.items():
                player[key] = value
    
    def get_random_player_for_fight(self, uuid, exclude=[]):
        with self.lock:
            player = random.choice([player for player in self._players 
                                    if not (player['uuid'] in exclude or player.get('in_fight'))])
            player['in_fight'] = True
            return player
    
    
    def get(self, uuid):
        with self.lock:
            return self._players[self._uuid_index[uuid]]
    
    def get_group(self, group_id):
        with self.lock:
            return [self._players[self._uuid_index[uuid]] for uuid in self._group_index[group_id]]
    
    
    def get_all(self):
        with self.lock:
            return self._players[:]

    
def get_db():
    ctx = stack.top
    if ctx is not None:
        if not hasattr(ctx, 'database'):
            ctx.database = Database()
        result = ctx.database
        ctx.push()
        return result
