import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import discord
from StuffsWeNeed import _db

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

def show_inv(balance, main_weapon_e, main_weapon, main_weapon_xp, secondary_weapon_e, secondary_weapon, secondary_weapon_xp, healing_potion, p):
    em=discord.Embed(color=0xadcca6, title=f"Inventory", description=f"Balance: {balance}")
    em.add_field(name="Weapons", value=f"{main_weapon_e} {main_weapon} - xp: `{main_weapon_xp}`\n{secondary_weapon_e} {secondary_weapon} - xp: `{secondary_weapon_xp}`")
    em.add_field(name="Items", value=f"Healing potion - `{healing_potion}`", inline=False)
    em.set_footer(text=f"Do \"{p}inv <weapon/item>\" to see more info.")

    return em

def inventory_item(amount, desc, item, stats, p, thumbnail):
    em=discord.Embed(color=0xadcca6, title=f"Inventory - {item}", description=desc)
    em.add_field(name="Stats", value=stats, inline=False)
    em.add_field(name="Amount", value=amount, inline=False)
    em.set_thumbnail(url=thumbnail)
    em.set_footer(text=f"Do \"{p}inventory\" to see your all your items.")

    return em