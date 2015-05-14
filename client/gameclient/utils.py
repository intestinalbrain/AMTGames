# coding: utf-8

import string
import random

def get_player_name(name_length=6):
    return ''.join([random.choice(string.ascii_letters) for x in xrange(name_length)])
    
