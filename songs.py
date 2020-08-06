from flask import Flask, request
from nightbot import nightbot
import states
import threading

def skip_poll_result():
    votes = states.global_states.polls['skip_song'].options
    up = votes['+1'] + votes['＋１']
    down = votes['-1'] + votes['－１']

    nightbot.send_channel_message('卡歌投票結束，結果為同意：不同意 = {} : {}，{}'.format(
        up, down,
        '卡歌成功！' if up > down else '卡歌失敗！'
    ))

    if up > down:
        nightbot.skip_current_queue_item()

    states.global_states.del_poll('skip_song')

def receive_skip():
    states.global_states.add_poll('skip_song', ['+1', '＋１', '-1', '－１'])
    threading.Timer(10, skip_poll_result).start()
    return '卡歌投票開始，倒數十秒鐘，我話講完，誰贊成誰反對（同意 +1 不同意 -1）'