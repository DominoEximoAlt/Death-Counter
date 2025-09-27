import json
import os
from datetime import datetime, date
from utils.timer import Timer

t = Timer.get_instance()
#DEATH METHODS

def read_death():
    return t.get_deaths()

def add_death():
    t.add_death()
    

##TIME METHODS


