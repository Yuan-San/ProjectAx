import json
from dotenv import load_dotenv
import os

def get_version():
    v="v1.2.1-a"
    return v 

def get_config(filename: str = "config"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("config.json wasn't found")


def get_profile(filename: str = "profile"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("profile.json wasn't found")
    
def get_art(filename: str = "art"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("art.json wasn't found")

def get_target(target, id):
    if target is None: target = id
    else:
        try: target = target.id
        except: pass
    return target