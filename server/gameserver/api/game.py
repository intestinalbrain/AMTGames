# coding: utf-8

import random
import json
from datetime import datetime
import time


from flask import Blueprint

from gameserver.api import EMPTY_RESPONSE
from gameserver.db.db import get_db
from gameserver.settings import TIME_TOUR

game_blueprint = Blueprint('game_blueprint', __name__)

@game_blueprint.route('/opponent/<player_id>', methods=['GET'])
def get_opponent(player_id):
    db = get_db()
    if time.mktime(datetime.now().timetuple()) - db.timestamp > TIME_TOUR:
        return json.dumps({'status': 'finished'})
    player = db.get_random_player_for_fight(player_id, exclude=[player_id])
    return json.dumps({'uuid': player['uuid']})


@game_blueprint.route('/attack/<from_player_id>/<to_player_id>', methods=['POST'])
def atack(from_player_id, to_player_id):
    db = get_db()
    from_player, to_player = db.get(from_player_id), db.get(to_player_id)
    result = random.randint(-10, 10)
    from_player['medals'] += result
    from_player['attacked'] = True
    to_player['medals'] -= result
    to_player['in_fight'] = False
    db.update(from_player)
    db.update(to_player)
    return EMPTY_RESPONSE
