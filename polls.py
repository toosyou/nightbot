from flask import Flask, request
from nightbot import nightbot
import states
import threading
from urllib.parse import unquote

def poll_result(name):
    votes = states.global_states.polls[name].options
    descs = states.global_states.polls[name].option_desc

    result_string = '{} 投票結果：| '.format(name)

    max_vote, max_symbol = -1, None
    for symbol, times in votes.items():
        result_string += '{}: {} 票 | '.format(descs[symbol], times)
        if max_vote < times:
            max_vote, max_symbol = times, symbol

    result_string += '最高票： {}'.format(descs[max_symbol])

    nightbot.send_channel_message(result_string)
    states.global_states.del_poll(name)

def add_poll():
    args = unquote(request.args['args'])
    try:    
        title = args.split('|')[0]
        time = int(args.split('|')[1])

        poll_start_string = '{} 投票開始，倒數 {} 秒:| '.format(title, time)

        options = list()
        option_desc = list()
        for option_string in args.split('|')[2:]:
            option_string = option_string.strip()

            option, desc = option_string.split(' ')[0].strip(), option_string.split(' ')[1].strip()
            options.append(option)
            option_desc.append(desc)

            poll_start_string += '{} 打 {} | '.format(desc, option)

        states.global_states.add_poll(title, options, option_desc, single_vote=True)
        threading.Timer(time+1, poll_result, [title, ]).start()

        nightbot.send_channel_message(poll_start_string)
        return '  '

    except:
        return '用法：!投票 標題 ｜ 持續時間(秒) | 選項1符號 選項1描述 | 選項2符號 選項2描述 | ...'