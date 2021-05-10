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

def create_inventory(id):
    db["Inventory"].insert_one({"_id": id, "main_weapon": "N/A", "secondary_weapon": "N/A", "main_weapon_xp": 0, "secondary_weapon_xp": 0, "balance": 0})
    
def delete_inventory(id):
    db["Inventory"].delete_one({"_id": id})