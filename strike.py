import threading
import states
import time

from nightbot import nightbot

strike_rules = {
    '777': r'.*7{3,}.*',
    '哭啊': r'.*哭[啊|阿].*',
    '太神啦': r'.*太神[了|啦|拉|辣].*',
    '???': r'^[?|？]{3,}$',
}

class Strike():
    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
        self.repeats = 1
        self.endding_thread = threading.Timer(10, self.end)
        self.endding_thread.start()

    @staticmethod
    def handler(name, user_id):
        # check if the according strike exists in state
        if name in states.global_states.strikes:
            the_strike = states.global_states.strikes[name]
            the_strike.refresh()
            the_strike.repeats += 1

        else:
            # create a new strike
            states.global_states.strikes[name] = Strike(name)

            # nightbot.send_channel_message('{} 已經啟動了 {} 連擊，一起打 {} 來連擊吧！'.format(
            #     user_id, name, name
            # ))

        return

    def refresh(self):
        self.endding_thread.cancel()
        self.endding_thread = threading.Timer(10, self.end)
        self.endding_thread.start()

    def end(self):
        # remove strike from states
        states.global_states.strikes.pop(self.name)
        if self.repeats > 2:
            nightbot.send_channel_message('{} 連擊在 {} 秒間達成了 {} COMBO! 再接再厲吧！'.format(
                self.name, int(time.time() - self.start_time), self.repeats
            ))