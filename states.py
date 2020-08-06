import threading

class States():
    class Song():
        def __init__(self):
            self.poll_lock = threading.Lock()
            self.skip_poll_up = 0
            self.skip_poll_down = 0
            self.voted_user = set()

        def skip_poll_init(self):
            with self.poll_lock:
                self.skip_poll_up = self.skip_poll_down = 0
                self.voted_user = set()

        def skip_vote_upvote(self, user_id):
            with self.poll_lock:
                if user_id not in self.voted_user:
                    self.skip_poll_up += 1
                    self.voted_user.add(user_id)

        def skip_vote_downvote(self, user_id):
            with self.poll_lock:
                if user_id not in self.voted_user:
                    self.skip_poll_down += 1
                    self.voted_user.add(user_id)
        
    def __init__(self):
        self.song = self.Song()

def initial():
    global global_states
    global_states = States()