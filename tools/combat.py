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
        return (b["damage"], b["accuracy"], b["defence"])

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

def get_gamemode_stats(gamemode):
    dmg = _json.get_gamemode()[f"{gamemode}_dmg"]
    acc = _json.get_gamemode()[f"{gamemode}_acc"]
    df = _json.get_gamemode()[f"{gamemode}_def"]
    spd = _json.get_gamemode()[f"{gamemode}_spd"]
    hp = _json.get_gamemode()[f"{gamemode}_hp"]

    return (dmg, acc, df, spd, hp)

def get_winner_message(a, winner):
    if a == "Easy" or a == "Medium" or a == "Hard":
        if winner == "Training Dummy":
            return f"{a} Mode - You've lost! Try again."
        if winner == "you":
            return f"{a} Mode - You won!"

    elif a == "-":
        if winner == "Training Dummy":
            return "You've lost! Ouch."
        if winner == "you":
            return "You won. Congrats!"

    return "?"


async def weapon_select(target, pvp_message, clientFetch):
    await pvp_message.edit(content=f"**{target.display_name}**, which weapon do you want to pick for battle?")

    primary_emote = clientFetch.get_emoji(_json.get_emote_id(get_weapons(target.id)[0]))
    secondary_emote = clientFetch.get_emoji(_json.get_emote_id(get_weapons(target.id)[1]))

    await pvp_message.add_reaction(emoji=primary_emote)
    await pvp_message.add_reaction(emoji=secondary_emote)
    await pvp_message.add_reaction(emoji='🛑')

    def checkforR(reaction, msg):
        return msg == target and reaction.emoji in [primary_emote, secondary_emote, '🛑']

    reaction, msg = await clientFetch.wait_for('reaction_add', timeout=30, check=checkforR)

    if reaction.emoji == primary_emote: return get_weapons(target.id)[0]
    elif reaction.emoji == secondary_emote: return get_weapons(target.id)[1]
    elif reaction.emoji == '🛑':
        await ctx.send(embed=embeds.error_2(target.name, target.discriminator))
        return
