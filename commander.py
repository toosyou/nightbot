import requests
from flask import Flask, request
from NightPy.nightpy import NightPy
import configparser

app = Flask(__name__)

CONFIG_FILENAME = './config.cfg'
secret_config = configparser.ConfigParser()
secret_config.read(CONFIG_FILENAME)

TOKEN = None

@app.route("/")
def hello():
    print(request.args)
    print(request.args.get('code'))
    return "Hello World!"

def request_token():
    r = requests.post('https://api.nightbot.tv/oauth2/token',
        data={
            'client_id': secret_config['secret']['client_id'],
            'grant_type': secret_config['secret']['grant_type'],
            'scope': secret_config['secret']['scope'],
            'client_secret': secret_config['secret']['client_secret'],
        }
    )
    return r.json()['access_token']

if __name__ == "__main__":
    if secret_config.has_option('secret', 'token'):
        TOKEN = secret_config['secret']['token']
    else:
        TOKEN = request_token()
        secret_config.set('secret', 'token', TOKEN)
        with open(CONFIG_FILENAME, 'w') as f:
            secret_config.write(f)

    nightbot = NightPy(TOKEN)
    print(nightbot.get_channel())
    nightbot.join_channel()
    nightbot.send_channel_message('testing')
    # print(TOKEN)
    # app.run(host='0.0.0.0', port=7001, ssl_context='adhoc')