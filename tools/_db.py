from dotenv import load_dotenv
from pymongo import MongoClient
import os
from tools import _json
import discord

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def get_prefix(id):
    for b in db["Prefix"].find({"server_id": id}):
        prefix = b["prefix"]
        return prefix

    # return "ax "


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
        try: x = b[item]
        except: x = 0

    if mainCommand == "nm":
        return f"Inventory: `{x}`\nVault: `N/A`"
    elif mainCommand == "m":
        return x

def get_item(id, item, guild_id, mainCommand):
    check = db["Inventory"].count_documents({"_id": id})
    if check != 0:
        return get_items_precheck(id, item, mainCommand)

    return f"You don't have a profile yet. Create one: `{get_prefix(guild_id)}createprofile`"

def get_weapon_stats(weapon, stat):
    for b in db["WeaponStats"].find({"_id": weapon}):
        return b[stat]

def get_weapon_stats_list(weapon):
    return f"Damage: {get_weapon_stats(weapon, 'damage')}\nAccuracy: {get_weapon_stats(weapon, 'accuracy')}%\nDefence: {get_weapon_stats(weapon, 'defence')}%"

def get_profile_looks(id):
    for b in db["Profile"].find({"_id": id}):
        return b["looks"]

def get_training_status(id):
    if db["Training"].count_documents({"_id": id}) == 0: return False
    return True

def get_dummy_stats(id, stat):
    for b in db["Training"].find({"_id": id}):
        return b[stat]

async def profile_check(id):
    check = db["Profile"].count_documents({"_id": id})
    return check



def warning_doc_check(u_id, s_id):
    check = db["Warnings"].count_documents({"_id": f"{u_id} @ {s_id}"})
    return check

def create_warning_log(u_id, s_id):
    db["Warnings"].insert_one({"_id": f"{u_id} @ {s_id}"})

def get_warning_num(u_id, s_id):
    for b in db["Warnings"].find({"_id": f"{u_id} @ {s_id}"}):
        warning_list = list(b.items())
        warning_list_max = len(warning_list)
        return warning_list_max

def get_warning(target, w_id, u_id, s_id):
    for b in db["Warnings"].find({"_id": f"{u_id} @ {s_id}"}):
        return b[f"warning_{w_id}"]

def split_warning(warning):
    split_1 = warning.split(' @ ')
    split_2 = split_1[1].split(' -///- ')
    split_3 = split_1[0].split(' - ')
    return split_3[0], split_3[1], split_2[0], split_2[1]

def get_warnings_list(u_id, s_id):
    num = get_warning_num(u_id, s_id)
    for b in db["Warnings"].find({"_id": f"{u_id} @ {s_id}"}):
        warnings = []
        for i in range(1, num):
            warnings.append(b[f"warning_{i}"])
    return warnings
