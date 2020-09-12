from flask import render_template
from twitchio.ext import commands
import configparser
import re
import json
import time
import requests
import threading
import numpy as np
import requests

from nightbot import nightbot
import strike
import lyric
import states
import beauty
import video_request
from app_socket import socketio

CONFIG_FILENAME = './config.cfg'
secret_config = configparser.ConfigParser()
secret_config.read(CONFIG_FILENAME)

def request_channel_id():
    headers = {
        'client-id': secret_config['twitch']['client_id'],
        'Authorization': 'Bearer {}'.format(secret_config['twitch']['oauth_token'])
    }
    params = {
        'query': secret_config['general']['channel']
    }
    r = requests.get('https://api.twitch.tv/helix/users', params=params, headers=headers)
    return r.json()['data'][0]['id']

def comment_screen():
    return render_template('comment_screen.html')

def send_comment(comment, user_id):
    socketio.emit('new comment', {
        'comment': '{}: {}'.format(user_id, comment)
    })

def fake_comments(user_id, comment):
    for _ in range(100):
        send_comment(comment, user_id)
    return '彈幕刷起來'

def check_vote(comment, user_id):
    if comment in states.global_states.anchor_option:
        states.global_states.vote(user_id, comment)

def check_strike(comment, user_id):
    for name, rule in strike.strike_rules.items():
        if re.match(rule, comment):
            strike.Strike.handler(name, user_id)
            return # only match the firest rule for not

def check_command(comment, user_id):
    rule_and_handler = {
    }

    for rule, handler in rule_and_handler.items():
        if re.match(rule, comment):
            handler(comment, user_id)
            return # only match the firest rule for not

def lyric_match(comment):
    comment = comment.lower().replace(' ', '')
    for key in lyric.lyrics:
        if comment.startswith(key.lower().replace(' ', '')):
            lyric.random_lyrics(key)

def redemption(title, user_id, user_input):
    title_and_funcs = {
        '隨機表特': lambda user_id, user_input: '@{} 恭喜獲得{}'.format(user_id, beauty.get_beauty()),
        '隨機奶特': lambda user_id, user_input: '小色鬼 @{} 恭喜獲得{}'.format(user_id, beauty.get_boobs()),
        '全服廣播': lambda user_id, user_input: '!speak {} 說 {}'.format(user_id, user_input),
        '播放 youtube 影片': lambda user_id, user_input: video_request.push_queue(user_id, user_input),
        '彈幕刷起來': lambda user_id, user_input: fake_comments(user_id, user_input)
    }

    if title in title_and_funcs:
        message = title_and_funcs[title](user_id, user_input)[:380]
        while True:
            if nightbot.send_channel_message(message) is None:
                time.sleep(1 + np.random.rand()*2)
            else:
                return

avaliable_controls = [s.strip() for s in secret_config['game_control']['controls'].split(',')] if secret_config.has_section('game_control') else None
poll_controls = [s.strip() for s in secret_config['game_control']['poll_controls'].split(',')] if secret_config.has_section('game_control') else None
def game_control_poll_result(control):
    votes = states.global_states.polls[control].options
    agree = sum([votes[s] for s in ['yes', 'y', 'Yes', 'Y']])
    disagree = sum([votes[s] for s in ['no', 'n', 'No', 'N']])

    if agree > disagree: # succeed, send control
        r = requests.get(secret_config['game_control']['base_url'], params={'control': control})

    nightbot.send_channel_message('{} result: agree : disagree = {} : {}, {} {}!'.format(
        control, agree, disagree, control,
        'sent' if agree > disagree else 'not sent'
    ))

    states.global_states.del_poll(control)

def game_control(comment, user_id):
    global avaliable_controls
    global poll_controls

    def no_other_poll_controls():
        for control in poll_controls:
            if control in states.global_states.polls:
                return False
        return True

    if secret_config.has_section('game_control'):
        control = comment.lower().strip()

        if control in avaliable_controls:
            r = requests.get(secret_config['game_control']['base_url'], params={'control': control})

        elif control in poll_controls:
            if no_other_poll_controls():
                states.global_states.add_poll(control, ['yes', 'y', 'Yes', 'Y', 'no', 'n', 'No', 'N'])
                threading.Timer(11, game_control_poll_result, [control]).start()
                nightbot.send_channel_message('{} poll initiated! Type (y)es/(n)o to agree/disagree! 10s remaining.'.format(control))
            else:
                nightbot.send_channel_message('Another poll has been initiated. Wait 10s for another one.')

class Bot(commands.Bot):
    async def event_ready(self):
        await self.pubsub_subscribe(secret_config['twitch']['oauth_token'],
                'channel-points-channel-v1.{}'.format(request_channel_id()))

    async def event_raw_pubsub(self,  data):
        #data is given to us as a dictionary
        if data['type'] == 'MESSAGE':
            payload = data['data']['message']
            #but this payload is a json string
            payload = json.loads(payload)
            #now the payload is a dictionary, but it's nested as hell, so getting to the name of the reward is clunky

            user_id = payload['data']['redemption']['user']['display_name']
            title = payload['data']['redemption']['reward']['title']

            try:
                user_input = payload['data']['redemption']['user_input']
            except:
                user_input = ''

            redemption(title, user_id, user_input)

    async def event_message(self, ctx):
        comment = ctx.content
        user_id = ctx.author.name

        # make sure the bot ignores itself and the streamer
        if user_id.lower() == 'Nightbot'.lower():
            return

        game_control(comment, user_id)
        check_vote(comment.lower().strip(), user_id)
        lyric_match(comment)
        check_strike(comment, user_id)
        check_command(comment, user_id)
        send_comment(comment, user_id)

chatviewer = Bot(
    irc_token = secret_config['twitch']['chat_token'],
    client_id = secret_config['twitch']['client_id'],
    nick = secret_config['twitch']['nick'],
    prefix = '!',
    initial_channels=['#{}'.format(secret_config['general']['channel'])]
)

threading.Thread(target=chatviewer.run).start()
