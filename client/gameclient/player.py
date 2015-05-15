# coding: utf-8

from random import randint
import uuid
import requests
from threading import Lock
import time
import datetime

from utils import generate_player_name, generate_player_power
from settings import PLAYER_INIT_MEDALS, PLAYER_INIT_MONEY, GROUP_PLAYER_COUNT, URL_PREFIX


class Player(object):
    lock = Lock()
    
    def __init__(self, group_id=None, uuid='', name='', power=0, medals=0, money=0):
        self._uuid = uuid
        self._name = name
        self._power = power
        self._medals = medals
        self._money = money
        self._sleep = False
        self._group_id = group_id
        self._atack_dt = None
    
    def wakeup(self):
        self._sleep = False

    @property
    def group_id(self):
        return self._group_id
    
    @group_id.setter
    def group_id(self, group_id):
        self._group_id = group_id

    @property
    def uuid(self):
        return self._uuid
    
    @uuid.setter
    def uuid(self, uuid):
        self._uuid = uuid
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, power):
        self._power = int(power)
    
    @property
    def medals(self):
        return self._medals
    
    @medals.setter
    def medals(self, medals):
        self._medals = int(medals)
    
    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, money):
        self._money = int(money)
    
    @property
    def post_url_format(self):
        return '/'.join([str(val) for val in 
                         [self.name, self.power, self.medals, self.money]])
    
    def sleep(self, dt):
        with self.lock:
            return self._atack_dt and (dt-self._atack_dt).total_seconds() < 5
    
    def initialize(self, values=None):
        if values:
            for key, value in values.items():
                setattr(self, key, value)
        else:
            self._name = generate_player_name()
            self._power = generate_player_power()
            self._medals = PLAYER_INIT_MEDALS
            self._money = PLAYER_INIT_MONEY
    
    def attack(self):
        with self.lock:
            result = requests.get('/'.join([URL_PREFIX, 'opponent', self.uuid])).json()
            if not 'status' in result:
                requests.post('/'.join([URL_PREFIX, 'attack', self.uuid, result['uuid']]))
            else:
                return False
            self._atack_dt = datetime.datetime.now()
        return True

