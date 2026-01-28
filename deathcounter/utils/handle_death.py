from .game_selector import game_exe
from .timer import Timer

t = Timer.get_instance(game_exe=game_exe)
#DEATH METHODS

def read_death():
    return t.get_deaths()

def add_death():
    t.add_death()
    

##TIME METHODS


