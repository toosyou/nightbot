from flask import Flask, request
from nightbot import nightbot
import states
import threading
import argparse

def poll_result(name):
    pass

def add_poll(comment, user_id):
    # remove commend
    comment = comment[len('!投票'):]

    parser = argparse.ArgumentParser()
    parser.add_argument('title')
    parser.add_argument('options', nargs='+')

    parser.parse_args(comment.split(' '))