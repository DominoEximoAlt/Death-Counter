import time
from utils.state import load_state, save_state

class Timer:
    def __init__(self):
        state = load_state()
        self.start_time = time.time()
        self.elapsed_before = state.get("elapsed", 0)
        self.deaths = state.get("deaths", 0)

    def get_instance():
        if not hasattr(Timer, "_instance"):
            Timer._instance = Timer()
        return Timer._instance

    def start(self):
        if self.start_time == 0:
            self.start_time = time.time()

    def stop(self):
        if self.start_time != 0:
            self.elapsed_before += time.time() - self.start_time
            self.start_time = 0
        self._persist()

    def get_elapsed(self):
        total = self.elapsed_before
        if self.start_time is not None:
            total += time.time() - self.start_time
        return int(total)

    def get_deaths(self):
        total = self.deaths
        return total

    def add_death(self):
        self.deaths += 1
        
    def get_formatted(self):
        total = self.get_elapsed()
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02}"

    def _persist(self):
        state = load_state()
        state["elapsed"] = self.elapsed_before
        save_state(state)
