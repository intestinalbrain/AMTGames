# coding: utf-8

import json

from flask import Blueprint

from gameserver.api import EMPTY_RESPONSE

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route('/player/<name>/<int:power>/<int:medals>/<int:money>', methods=['POST'])
def add_player(name, power, medals, money):
    print ' | '.join([str(val) for val in [name, power, medals, money]])
    return EMPTY_RESPONSE


@admin_blueprint.route('/player/<id>', methods=['GET'])
def get_player(id):
    print id
    return json.dumps({'id': id, 'value': 'get_player'})


@admin_blueprint.route('/tournament/<int:timestamp>', methods=['POST'])
def start_tournament(timestamp):
    return EMPTY_RESPONSE


@admin_blueprint.route('/tournament/<int:id>', methods=['GET'])
def stop_tournament(id):
    return json.dumps({'id': id, 'value': 'stop_tournament'})
