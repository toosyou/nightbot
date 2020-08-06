from flask import Flask, request
from commander import nightbot
import states
import threading

def skip_poll_result():
    up, down = states.global_states.song.skip_poll_up, states.global_states.song.skip_poll_down

    nightbot.send_channel_message('卡歌投票結束，結果為同意：不同意 = {} : {}，{}'.format(
        up, down,
        '卡歌成功！' if up > down else '卡歌失敗！'
    ))

    if up > down:
        nightbot.skip_current_queue_item()

def receive_skip():
    states.global_states.song.skip_poll_init()
    threading.Timer(10, skip_poll_result).start()
    return '卡歌投票開始，倒數十秒鐘，我話講完，誰贊成誰反對（同意 +1 不同意 -1）'