import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def config(filename: str = "config"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("config.json wasn't found")


def profile(filename: str = "profile"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("profile.json wasn't found")


def texts(filename: str = "texts"):
    try:
        with open(f"StuffsWeNeed/jsons/{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("texts.json wasn't found")


def get_prefix(id):
    a = db["Prefix"].find({"server_id": id})
    for b in a:
        prefix = b["prefix"]
    
    return prefix