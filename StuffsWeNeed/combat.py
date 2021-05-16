import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import discord

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def get_player_stats(weapon):
    for b in db["WeaponStats"].find({"_id": weapon}):
        dmg = b["damage"]
        acc = b["accuracy"]
        defence = b["defence"]
        spd = b["speed"]
    return (dmg, acc, defence, spd)

def get_weapon_emote_id(weapon):
    for b in db["WeaponStats"].find({"_id": weapon}):
        emote_id = b["emote_id"]
    return emote_id

def get_weapons(id):
    for b in db["Inventory"].find({"_id": id}):
        main_weapon = b["main_weapon"]
        secondary_weapon = b["secondary_weapon"]
    return (main_weapon, secondary_weapon)