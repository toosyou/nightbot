from flask import render_template, request
import threading
import time
import numpy as np
from urllib.parse import urlparse, parse_qs

from nightbot import nightbot
from app_socket import socketio

class Queue():
    def __init__(self):
        self.queue = list()
        self.lock = threading.Lock()

    def push(self, request):
        with self.lock:
            self.queue.append(request)
    
    def pop(self):
        with self.lock:
            if not self.empty():
                self.queue.pop(0)
    
    def get(self):
        with self.lock:
            first =  self.queue[0]
        return first

    def empty(self):
        return len(self.queue) == 0


request_queue = Queue()

class Request():
    def __init__(self, youtube_url, start_time, duration):
        self.youtube_url = youtube_url
        self.start_time = start_time
        self.duration = duration

def send_request():
    request = request_queue.get()
    payload = {
        'url': request.youtube_url,
        'start_time': request.start_time,
        'duration': request.duration,
    }

    socketio.emit('new video', payload, broadcast=True)

@socketio.on('successful')
def pop_queue():
    request_queue.pop()
    nightbot.api_request('song_requests/queue/pause', method='post')

@socketio.on('next')
def send_next():
    if request_queue.empty():
        while nightbot.api_request('song_requests/queue/play', method='post') is None:
            time.sleep(3)
    else:
        send_request()

def video_request_page():
    return render_template('video_request.html')

def video_request():
    return push_queue(request.args['user_id'], request.args['query'])

def push_queue(user_id, input_string):
    args = input_string.strip().split(' ')
    url, start_time, duration = args[0], int(args[1]), max(min(30, int(args[2])), 5)
    url = 'https://www.youtube.com/embed/{}'.format(
        parse_qs(urlparse(url).query)['v'][0]
    )
    request_queue.push(Request(url, start_time, duration))
    send_request()

    return '{} 成功點播了 {}，等會就會出現在螢幕上了！'.format(user_id, args[0])