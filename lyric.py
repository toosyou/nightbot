import numpy as np
from nightbot import nightbot

lyrics = {
    '我難過的是':[
        '''放棄你 放棄愛\
        放棄的夢被打碎 忍住悲哀\
        我以為 是成全\
        你卻說你更不愉快''',

        '''忘了你 忘了愛\
        盡全力忘記我們 真心相愛\
        也忘了告訴你 失去的不能重來'''
    ]
}

def random_lyrics(song, user_id):
    nightbot.send_channel_message(np.random.choice(lyrics[song]))