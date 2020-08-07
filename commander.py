import requests
from flask import Flask, request
import configparser
import threading

from twitchio.ext import commands

from nightbot import nightbot
import states
import rank_parser
import songs
import polls
import lyric

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

states.initial()

def check_vote(comment, user_id):
    if comment in states.global_states.anchor_option:
        states.global_states.vote(user_id, comment)

def check_command(comment, user_id):
    command = {
        '我難過的是': lyric.random_lyrics
    }.get(comment.split(' ')[0], None)
    if command: command(comment, user_id)

@chat_bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == 'Nightbot'.lower():
        return

    comment = ctx.content
    user_id = ctx.author.name

    check_vote(comment.lower().strip(), user_id)
    check_command(comment, user_id)

if __name__ == "__main__":
    t = threading.Thread(target=chat_bot.run)
    t.start()

    app.add_url_rule('/rank', view_func=rank_parser.parser)
    app.add_url_rule('/skip', view_func=songs.receive_skip)
    app.add_url_rule('/poll', view_func=polls.add_poll)
    app.add_url_rule('/volumeup', view_func=songs.volumeup)
    app.add_url_rule('/volumedown', view_func=songs.volumedown)

    app.run(host='0.0.0.0', port=7001)