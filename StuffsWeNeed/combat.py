import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import discord
import random
import asyncio

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

def acc_hit(acc):
    acc = float(acc) / 100

    if random.random() <= acc:
        return True
    else:
        return False

def dmg_calc(dmg, acc, e_defense):
    if acc_hit(acc) == True:
        dmg_taken = dmg - (dmg * float(e_defense) / 100)
        return dmg_taken
    if acc_hit(acc) == False:
        return 0

def attack(dmg, acc, e_defense, e_hp):
    dmg_taken = dmg_calc(dmg, acc, e_defense)

    if dmg_taken is not None:
        e_hp = e_hp - float(dmg_taken)

    if e_hp > 0:
        return e_hp
    else:
        return 0.0

def hit_or_miss(e_hp, prHP, moves):
    if moves == 0:
        return ""
    elif e_hp == prHP:
        return "- Miss!"
    else:
        return "- Hit!"

def winner(youHP, enemyHP):
    if youHP == 0.0:
        return "Enemy"
    elif enemyHP == 0.0:
        return "you"
    else:
        return "?"
