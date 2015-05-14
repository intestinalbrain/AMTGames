# coding: utf-8

from flask import Flask

from settings import HOST, PORT

from api.admin import admin_blueprint
from api.game import game_blueprint

def main():
    app = Flask(__name__)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(game_blueprint)
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
