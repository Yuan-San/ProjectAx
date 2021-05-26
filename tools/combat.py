from re import A
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import random
import asyncio
from tools import _json, embeds, tools

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def get_player_stats(weapon):
    for b in db["WeaponStats"].find({"_id": weapon}):
        return (b["damage"], b["accuracy"], b["defence"], b["speed"])

def get_weapon_emote_id(weapon):
    return _json.get_art()[f"{weapon}_emote_id"]

def get_weapons(id):
    for b in db["Inventory"].find({"_id": id}):
        return (b["main_weapon"], b["secondary_weapon"])

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

def miss_counter(misses):
    if misses == 0 or misses == 1: return ""
    return f"({misses})"

def hit_counter(hits):
    if hits == 0 or hits == 1: return ""
    return f"({hits})"

# async def pve(spd, dmg, acc, df, hp):
#     a = 1
#     spd = float(spd/10)
#     while a==1:
#         attack(dmg, acc, df, hp)
#         await asyncio.sleep(spd)


def winner(youHP, enemyHP):
    if youHP == 0.0:
        return "Enemy"
    elif enemyHP == 0.0:
        return "you"
    else:
        return "?"

def get_gamemode_easy():
    pass
def get_gamemode_medium():
    pass
def get_gamemode_hard():
    pass
