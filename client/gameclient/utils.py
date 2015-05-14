# coding: utf-8

import string
import random

def generate_player_name(name_length=6):
    return ''.join([random.choice(string.ascii_letters) for x in xrange(name_length)])


def generate_player_power():
    return random.randint(1, 1000)
