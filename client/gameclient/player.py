# coding: utf-8

from random import randint

from utils import get_player_name

class Player(object):
    def __init__(self, name, power, medals, money):
        self._name = name
        self._power = power
        self._medals = medals
        self._money = money

    
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

