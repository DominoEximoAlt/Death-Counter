import json
import os

def read_death():
    
    with open(os.getenv("SAVE_FILE"), 'r') as f:
        data = json.load(f)
    return data['deaths']

def add_death():
    data = read_death()
    data += 1
    with open(os.getenv("SAVE_FILE"), 'w') as f:
        json.dump({"deaths": data}, f)
    
