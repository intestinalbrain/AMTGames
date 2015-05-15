# coding: utf-8

import json

from flask import Blueprint

from gameserver.api import EMPTY_RESPONSE
from gameserver.db.db import get_db

from gameserver.settings import GROUP_PLAYER_COUNT

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route('/player/<name>/<int:power>/<int:medals>/<int:money>', methods=['POST'])
def add_player(name, power, medals, money):
    db = get_db()
    player = {'name': name, 'power': power, 'medals': medals, 'money': money}
    uuid = db.add(player)
    return json.dumps({'uuid': uuid})


@admin_blueprint.route('/player/<uuid>', methods=['GET'])
def get_player(uuid):
    db = get_db()
    return json.dumps(db.get(uuid))


@admin_blueprint.route('/tournament/<float:timestamp>', methods=['POST'])
def start_tournament(timestamp):
    db = get_db()
    db.timestamp = float(timestamp)
    players = db.get_all()
    players = sorted(players, key=lambda item: item['power'])
    for group_id, group in enumerate(zip(*[iter(players)]*GROUP_PLAYER_COUNT), 1):
        for player in group:
            player = dict(player)
            player['group_id'] = group_id
            db.update(player)
    return EMPTY_RESPONSE


@admin_blueprint.route('/tournament/<int:group_id>', methods=['GET'])
def tournament_data(group_id):
    db = get_db()
    winners = sorted(db.get_group(int(group_id)), 
                     key=lambda player: player['medals'], 
                     reverse=True)[:3]
    not_attacked_count = len([player for player in db.get_group(int(group_id)) if not player['attacked']])
    result = {'winners': winners, 'not_attacked_count': not_attacked_count}
    return json.dumps(result)
