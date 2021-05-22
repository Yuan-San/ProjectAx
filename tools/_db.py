from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def get_prefix(id):
    for b in (db["Prefix"].find({"server_id": id})): prefix = b["prefix"]
    return prefix


def create_inventory(id, main_weapon, secondary_weapon):
    db["Inventory"].insert_one({"_id": id, "main_weapon": main_weapon, "secondary_weapon": secondary_weapon, "main_weapon_xp": 0, "secondary_weapon_xp": 0, "balance": 0})
    
def delete_inventory(id):
    db["Inventory"].delete_one({"_id": id})

def get_weapons(id):
    for b in db["Inventory"].find({"_id": id}):
        return (b["main_weapon"], b["secondary_weapon"], b["main_weapon_xp"], b["secondary_weapon_xp"])

def get_balance(id):
    for b in db["Inventory"].find({"_id": id}):
        balance = b["balance"]
    
    return balance

def get_items_precheck(id, item, mainCommand):
    for b in db["Inventory"].find({"_id": id}):
        try:
            x = b[item]
        except:
            x = 0
    if mainCommand == "nm":
        return f"Inventory: `{x}`\nVault: `N/A`"
    elif mainCommand == "m":
        return x

def get_item(id, item, guild_id, mainCommand):
    check = db["Inventory"].count_documents({"_id": id})
    if check != 0:
        return get_items_precheck(id, item, mainCommand)
    else:
        p = get_prefix(guild_id)
        return f"You don't have a profile yet. Create one: `{p}createprofile`"

def get_weapon_stats(weapon, stat):
    for b in db["WeaponStats"].find({"_id": weapon}): 
        stats = b[stat]
    return stats

def get_weapon_stats_list(weapon):
    damage="damage"
    accuracy="accuracy"
    defence="defence"
    speed="speed"

    list = f"Damage: {get_weapon_stats(weapon, damage)}\nAccuracy: {get_weapon_stats(weapon, accuracy)}%\nDefence: {get_weapon_stats(weapon, defence)}%\nSpeed: {get_weapon_stats(weapon, speed)}00ms"
    return list

def get_profile_looks(id):
    for b in db["Profile"].find({"_id": id}):
        looks = b["looks"]

    return looks