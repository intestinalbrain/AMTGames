# coding: utf-8

from random import randint
import uuid

from utils import generate_player_name, generate_player_power
from settings import PLAYER_INIT_MEDALS

class Player(object):
    def __init__(self, uuid='', name='', power=0, medals=0, money=0):
        self._uuid = uuid
        self._name = name
        self._power = power
        self._medals = medals
        self._money = money

    @property
    def uuid(self):
        return self._uuid
    
    @uuid.setter
    def uuid(self, value):
        self._uuid = uuid
    
    @property
    def name(self):
        return self._name
    
    
    
    @property
    def power(self):
        return self._power
    
    @property
    def medals(self):
        return self._medals
    
    @property
    def money(self):
        return self._money
    
    @property
    def post_url_format(self):
        return '/'.join([str(val) for val in [self.uuid, self.name, self.power, self.medals, self.money]])
    
    def initialize(self, values=None):
        if values:
            for key, value in values.items():
                setattr(self, key, value)
        else:
            self._uuid = uuid4()
            self._name = generate_player_name()
            self._power = generate_player_power()
            self._medals = PLAYER_INIT_MEDALS
            self._money = PLAYER_INIT_MONEY


class Group(Thread):
    ISPLAYING = 1
    ISPAUSED = 2
    def __init__(self, group_id):
        Thread.__init__(self)
        self._group_id = group_id
        self._players = []
        self._status = self.ISPAUSED
    
    def get_player(self, player_pointer=0):
        while True:
            if player_pointer == len(self._players):
                player_pointer = 0
            yield self._players[player_pointer]
            player_pointer += 1
    
    def append_player(self, player):
        self._players.append(player)
    
    def start(self):
        self._status |= self.ISPLAYING
        while self.is_playing:
            if not self.is_paused:
                self.get_player().atack()
    
    @property
    def is_playing(self):
        return (self._status & self.ISPLAYING) == self.ISPLAYING
    
    @property
    def is_paused(self):
        return (self._status & self.PAUSED) == self.PAUSED
    
    def stop(self):
        if self.is_playing:
            self._status ^= self.ISPLAYING
    
    def pause(self, value):
        if value:
            self._status |= self.PAUSED
        else:
            if self.is_paused:
                self._status ^= self.PAUSED
