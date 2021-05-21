import json
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
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

def inventory_weapon(weapon, desc, thumbnail, p):
    dmg = _db.get_weapon_stats(weapon, "damage")
    acc = _db.get_weapon_stats(weapon, "accuracy")
    spd = _db.get_weapon_stats(weapon, "speed")
    df = _db.get_weapon_stats(weapon, "defence")

    em=discord.Embed(color=0xadcca6, title=f"Weapon - {weapon}", description=desc)
    em.add_field(name="Stats", value=f"Damage: {dmg}\nAccuracy: {acc}\nSpeed: {spd}\nDefense: {df}")
    em.set_thumbnail(url=thumbnail)
    em.set_footer(text=f"Do \"{p}inventory\" to see your all your items.")

    return em

def pve_combat_embed(p_hp, p_weapon, p_dmg, p_acc, p_def, p_spd, e_hp, thumbnail, title, enemy, hit_or_miss):
    em=discord.Embed(color=0xadcca6)
    em.set_author(name=title)
    em.add_field(name=f"You {hit_or_miss}", value=f"hp: {int(p_hp)}", inline=False)
    em.add_field(name=enemy, value=f"hp: {int(e_hp)}", inline=False)
    em.set_thumbnail(url=thumbnail)

    return em

def pve_combat_embed_winner(p_hp, e_hp, thumbnail, title, enemy, winner):
    em=discord.Embed(color=0xadcca6, title=f"The winner of the fight is **{winner}**!!")
    em.set_author(name=title)
    em.add_field(name="You", value=f"Hp: {int(p_hp)}")
    em.add_field(name=enemy, value=f"Hp: {int(e_hp)}")
    em.set_thumbnail(url=thumbnail)
    em.title=f"The winner of the fight is **{winner}**!!"

    return em