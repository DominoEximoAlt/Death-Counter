import time
from utils.state import load_state, save_state
from utils.game_selector import game_exe as game_name

class Timer:
    is_running = False

    def __init__(self, game_exe):
        state = load_state(game_exe)
        self.is_running = False
        self.pause_start = time.time()
        self.paused_time = 0
        self.start_time = time.time()
        self.elapsed_before = state.get("elapsed", 0)
        self.deaths = state.get("deaths", 0)

    def get_instance(game_exe):
        if not hasattr(Timer, "_instance"):
            Timer._instance = Timer(game_exe)
        return Timer._instance

    def start(self):
        if self.start_time == 0:
            self.start_time = time.time()
        self.is_running = True

    def pause(self):
        self.is_running = False
        self.pause_start = time.time()              


    def resume(self):
        self.is_running = True
        pause_time = time.time() - self.pause_start
        self.start_time += pause_time

    def get_elapsed(self):
        total = self.elapsed_before
        if not self.is_running:
            self.paused_time = time.time() - self.pause_start
        if self.is_running:
            total += time.time() - self.start_time
        else:
            total += self.pause_start - self.start_time
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
        state = load_state(game_name)
        state["deaths"] = self.get_deaths()
        state["elapsed"] = self.get_elapsed()
        save_state(state, game_name)

    def is_running(self):
        return self.is_running