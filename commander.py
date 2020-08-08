import requests
from flask import Flask, request
import configparser
import threading
import better_exceptions; better_exceptions.hook()

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
    }.get(comment.split(' ')[0], None)
    if command: command(comment, user_id)

def lyric_match(comment):
    comment = comment.lower().replace(' ', '')
    for key in lyric.lyrics:
        if comment.startswith(key.lower().replace(' ', '')):
            lyric.random_lyrics(key)

@chat_bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == 'Nightbot'.lower():
        return

    comment = ctx.content
    user_id = ctx.author.name

    check_vote(comment.lower().strip(), user_id)
    lyric_match(comment)
    check_command(comment, user_id)

if __name__ == "__main__":
    t = threading.Thread(target=chat_bot.run)
    t.start()

    app.add_url_rule('/rank', view_func=rank_parser.parser)
    
    app.add_url_rule('/poll', view_func=polls.add_poll)

    # songs
    app.add_url_rule('/skip', view_func=songs.receive_skip)
    app.add_url_rule('/add_playlist', view_func=songs.add_playlist)
    app.add_url_rule('/volumeup', view_func=songs.volumeup)
    app.add_url_rule('/volumedown', view_func=songs.volumedown)
    app.add_url_rule('/add_and_skip', view_func=songs.add_and_skip)

    app.run(host='0.0.0.0', port=7001)