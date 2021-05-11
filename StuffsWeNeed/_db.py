import json
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
        main_weapon = b["main_weapon"]
        secondary_weapon = b["secondary_weapon"]
        main_weapon_xp = b["main_weapon_xp"]
        secondary_weapon_xp = b["secondary_weapon_xp"]
    
    return (main_weapon, secondary_weapon, secondary_weapon_xp, main_weapon_xp)

def main_weapon_e_picker(main_weapon):
    if main_weapon == "longsword": main_weapon_e = "<:LongSwordMK50:841591365649170463>"
    elif main_weapon == "katana": main_weapon_e = "<:KatanaMK50:841591388055273472>"
    elif main_weapon == "dagger": main_weapon_e = "<:DaggerMK50:841591344308158516>"
    elif main_weapon == "greatsword": main_weapon_e = "<:GreatSwordMK50:841591317368799242>"
    elif main_weapon == "sledgehammer": main_weapon_e = "<:SledgeHammerMK50:841591294115315753>"
    elif main_weapon == "mace": main_weapon_e = "<:MaceMK50:841591275567579156>"

    return main_weapon_e

def secondary_weapon_e_picker(secondary_weapon):
    if secondary_weapon == "bow": secondary_weapon_e = "<:BowMK50:841631789675053077>"
    elif secondary_weapon == "longbow": secondary_weapon_e = "<:LongBowMK50:841592788084326400>"

    return secondary_weapon_e

def get_balance(id):
    for b in db["Inventory"].find({"_id": id}):
        balance = b["balance"]
    
    return balance

def get_items(id):
    for b in db["Inventory"].find({"_id": id}):
        try:
            healing_potion = b["healing_potion"]
        except:
            healing_potion = 0
    
    return (healing_potion)