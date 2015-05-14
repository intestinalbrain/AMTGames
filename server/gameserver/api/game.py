# coding: utf-8

import json

from flask import Blueprint

from gameserver.api import EMPTY_RESPONSE

game_blueprint = Blueprint('game_blueprint', __name__)

@game_blueprint.route('/opponent/<player_id>', methods=['GET'])
def get_opponent(player_id):
    return json.dumps({'player_id': player_id, 'value': 'get_opponent'})


@game_blueprint.route('/atack/<from_player_id>/<to_player_id>', methods=['POST'])
def atack(from_player_id, to_player_id):
    return EMPTY_RESPONSE
