import json

def get_config(filename: str = "config"):
    try:
        with open(f"tools/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename}.json wasn't found")

def get_profile(filename: str = "profile"):
    try:
        with open(f"tools/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename}.json wasn't found")

def get_art(filename: str = "art"):
    try:
        with open(f"tools/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename}.json wasn't found")

def get_emote_id(item):
    return get_art()[f"{item}_emote_id"]
