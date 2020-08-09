import threading

class GeneralPoll():
    def __init__(self, name, options, option_desc=None, single_vote=True):
        self.single_vote = single_vote

        self.name = name
        self.lock = threading.Lock()
        self.options = dict()
        self.option_desc = dict()
        self.voted_user = set()
        self.init(options, option_desc)

    def init(self, options, option_desc=None):
        self.options = dict()
        for i, option in enumerate(options):
            self.options[option] = 0

            if option_desc is not None:
                self.option_desc[option] = option_desc[i]

        self.voted_user = set()

    def vote(self, user_id, which):
        with self.lock:
            if self.single_vote and user_id not in self.voted_user:
                if which in self.options:
                    self.options[which] += 1
                    self.voted_user.add(user_id)

class States():
    def __init__(self):
        self.polls = dict()
        self.anchor_option = set()
        self.strikes = dict()

    def add_poll(self, name, options, option_desc=None, single_vote=True):
        if name not in self.polls:
            self.polls[name] = GeneralPoll(name, options, option_desc=option_desc, single_vote=single_vote)
        self.reset_anchor()

    def del_poll(self, name):
        self.polls.pop(name, None)

    def reset_anchor(self):
        self.anchor_option = set()
        for name, poll in self.polls.items():
            self.anchor_option.update(poll.options.keys())

    def vote(self, user_id, which):
        for name, poll in self.polls.items():
            poll.vote(user_id, which)

def initial():
    global global_states
    global_states = States()