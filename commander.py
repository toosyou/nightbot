import requests
from flask import Flask, request
import threading
import better_exceptions; better_exceptions.hook()

from nightbot import nightbot
import chatviewer
import states
import rank_parser
import songs
import polls
import beauty

app = Flask(__name__)

if __name__ == "__main__":
    states.initial()

    app.add_url_rule('/rank', view_func=rank_parser.parser)
    app.add_url_rule('/poll', view_func=polls.add_poll)

    # songs
    app.add_url_rule('/skip', view_func=songs.receive_skip)
    app.add_url_rule('/add_playlist', view_func=songs.add_playlist)
    app.add_url_rule('/volumeup', view_func=songs.volumeup)
    app.add_url_rule('/volumedown', view_func=songs.volumedown)
    app.add_url_rule('/add_and_skip', view_func=songs.add_and_skip)
    app.add_url_rule('/beauty', view_func=beauty.get_beauty)
    app.add_url_rule('/boobs', view_func=beauty.get_boobs)

    app.run(host='0.0.0.0', port=7001)