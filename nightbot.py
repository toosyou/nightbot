import requests
import configparser

import os, sys
sys.path.append(os.path.join('./', 'NightPy'))
from NightPy.nightpy import NightPy

CONFIG_FILENAME = './paylin.cfg'
secret_config = configparser.ConfigParser()
secret_config.read(CONFIG_FILENAME)

def request_nightbot_token():
    r = requests.post('https://api.nightbot.tv/oauth2/token',
        data={
            'client_id': secret_config['secret']['client_id'],
            'grant_type': secret_config['secret']['grant_type'],
            'scope': secret_config['secret']['scope'],
            'client_secret': secret_config['secret']['client_secret'],
        }
    )
    return r.json()['access_token']

def get_and_save_token(token_func):
    if secret_config.has_option('nightbot', 'token'):
        token = secret_config['nightbot']['token']
    else:
        token = token_func()
        secret_config.set('nightbot', 'token', token)
        with open(CONFIG_FILENAME, 'w') as f:
            secret_config.write(f)
    return token

nightbot = NightPy(get_and_save_token(request_nightbot_token))
nightbot.join_channel()
