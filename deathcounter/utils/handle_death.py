import json
import os

#DEATH METHODS

def read_death():
    
    try:
        with open(os.environ["SAVE_FILE"], 'r') as f:
            data = json.load(f)
        return data['deaths']
    except KeyError:
        return 0

def add_death():
    data = read_death()
    data += 1
    with open(os.environ["SAVE_FILE"], 'w') as f:
        json.dump({"deaths": data, "time": 0}, f)
    

##TIME METHODS
    
def read_time():
    try:
        with open(os.environ["SAVE_FILE"], 'r') as f:
            data = json.load(f)
        return data['time']
    except KeyError:
        return 0

def add_time(seconds):
    data = read_death()
    seconds = read_time() + seconds
    with open(os.environ["SAVE_FILE"], 'w') as f:
        json.dump({"deaths": data, "time": seconds}, f)
