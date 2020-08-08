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

def add_and_skip():
    try:
        if len(request.args['query'].strip()) == 0:
            return '用法：!插歌 [搜尋字串 | 歌曲 youtube 連結]'
        queue = nightbot.add_new_queue_item(request.args['query'])
        nightbot.promote_queue_item(queue.id)
        nightbot.skip_current_queue_item()
        return '歌曲： {} 插播！'.format(queue.track.title)
    except:
        return '插播失敗！要求 {} 可能已經在歌單中，或是歌曲太長了喔！'.format(request.args['query'])

def get_volume():
    return nightbot.get_song_request_settings()[5]

def volumeup():
    setting = nightbot.get_song_request_settings()

    new_volume = min(100, setting.volume + 5)

    payload = {
        'volume': new_volume
    }

    nightbot.api_request('song_requests', method='put', payload=payload)
    return '音量已被調為：{}'.format(new_volume)

def volumedown():
    setting = nightbot.get_song_request_settings()

    new_volume = max(0, setting.volume - 5)

    payload = {
        'volume': new_volume
    }

    nightbot.api_request('song_requests', method='put', payload=payload)
    return '音量已被調為：{}'.format(new_volume)

def add_playlist():
    try:
        if len(request.args['query'].strip()) == 0:
            return '用法：!加歌 [搜尋字串 | 歌曲 youtube 連結]'

        song = nightbot.add_playlist_item(request.args['query'])
        return '新歌： {} 已經被永久的加入到播放清單囉'.format(song.track.title)
    except:
        return '要求 {} 可能已經在歌單中，或是歌曲太長了喔！'.format(request.args['query'])