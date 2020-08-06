import requests
from flask import Flask, request
import configparser
import threading

from twitchio.ext import commands

from token_parser import request_nightbot_token, get_and_save_token
import states
import rank_parser
import songs

import os, sys
sys.path.append(os.path.join('./', 'NightPy'))
from NightPy.nightpy import NightPy

app = Flask(__name__)

CONFIG_FILENAME = './paylin.cfg'
secret_config = configparser.ConfigParser()
secret_config.read(CONFIG_FILENAME)

chat_bot = commands.Bot(
    irc_token = secret_config['twitch']['chat_token'],
    client_id = secret_config['twitch']['client_id'],
    nick = secret_config['twitch']['nick'],
    prefix = '!',
    initial_channels=['#{}'.format(secret_config['general']['channel'])]
)

nightbot = NightPy(get_and_save_token(request_nightbot_token))
nightbot.join_channel()

states.initial()

@chat_bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == 'Nightbot'.lower():
        return

    if ctx.content.lower().strip() == '+1' or ctx.content.lower().strip() =='＋１':
        states.global_states.song.skip_vote_upvote(ctx.author.name)

    if ctx.content.lower().strip() == '-1' or ctx.content.lower().strip() =='－１':
        states.global_states.song.skip_vote_downvote(ctx.author.name)

if __name__ == "__main__":
    t = threading.Thread(target=chat_bot.run)
    t.start()

    app.add_url_rule('/rank', view_func=rank_parser.parser)
    app.add_url_rule('/skip', view_func=songs.receive_skip)

    app.run(host='0.0.0.0', port=7001)