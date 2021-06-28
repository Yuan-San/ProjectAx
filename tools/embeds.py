from tools.combat import miss_counter
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import discord
from tools import _db, _json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]


def show_inv(balance, main_weapon_e, main_weapon, main_weapon_xp, secondary_weapon_e, secondary_weapon, secondary_weapon_xp, healing_potion, healing_potion_emote, p):
    em=discord.Embed(color=0xadcca6, title=f"Inventory", description=f"Balance: {balance}")
    em.add_field(name="Weapons", value=f"{main_weapon_e} {main_weapon} - xp: `{main_weapon_xp}`\n{secondary_weapon_e} {secondary_weapon} - xp: `{secondary_weapon_xp}`")
    em.add_field(name="Items", value=f"{healing_potion_emote} Healing potion - `{healing_potion}`", inline=False)
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




def pvp_combat_embed(p_hp, p_atk, p_acc, p_def, e_hp, e_atk, e_acc, e_def, thumbnail, title, enemy, player, comment, hit_or_miss_p, hit_or_miss_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, enemy_move_indicator, beta):
    em=discord.Embed(color=0xadcca6)
    # em.set_author(name=title)
    em.add_field(name=f"{player_move_indicator}{player} {hit_or_miss_p} {miss_counter_p}{hit_counter_p}", value=f"HP: {int(p_hp)}\nATK: {p_atk}\nACC: {p_acc}\nDEF: {p_def}\n---------------------", inline=True)
    em.add_field(name=f"{enemy_move_indicator}{enemy} {hit_or_miss_d} {miss_counter_d}{hit_counter_d}", value=f"HP: {int(e_hp)}\nATK: {e_atk}\nACC: {e_acc}\nDEF: {e_def}", inline=True)

    if not beta:
        em.set_footer(text=f"Prax Bèta; Testing - Moves: {moves}")

    em.set_thumbnail(url=thumbnail)

    return em




def pve_combat_embed_winner(p_hp, e_hp, thumbnail, title, enemy, winner):
    em=discord.Embed(color=0xadcca6, title=winner)
    em.set_author(name=title)
    em.add_field(name="You", value=f"Hp: {int(p_hp)}")
    em.add_field(name=enemy, value=f"Hp: {int(e_hp)}")
    em.set_thumbnail(url=thumbnail)

    return em

def dummy_stat_embed_1(a, b):
    em=discord.Embed(color=0xadcca6, description = f"**{a}#{b}** What should the stats of the training dummy be?")
    em.add_field(name="Game Modes", value="**1. Easy** - The gods of Axem deem this a piece of cake\n**2. Medium** - Prepare well! fancy a ride?\n**3. Hard** - Prepare yourself to die.")
    em.add_field(name="Custom Stats", value="**4. Previous Stats** - Pick the stats you picked last time!\n**5. Other Stats** - You're the God now, pick!", inline=False)

    return em

def dummy_stat_embed_2(a, b):
    em=discord.Embed(color=0xadcca6, description = f"**{a}#{b}** What should the stats of the training dummy be?")
    em.add_field(name="Values", value="`dmg` - the amount of damage the dummy inflicts\n`acc` - a % chance of inflicting damage\n`def` - a % of damage that subtracts from the damage the dummy receives\n`spd` - the amount of milliseconds between each attempt to hit\n`hp`  - the amount of health point the dummy has")
    em.add_field(name="Examples", value="30,34,60,750,250\n70, 50, 50, 2500, 400\n..", inline=False)
    em.set_footer(text="Type the stats below, seperated by a comma.")

    return em

def help_module_embed(title, cmdList, url, p):
    em = discord.Embed(color = 0xadcca6, title=title)
    em.add_field(name="Commands", value=cmdList)
    em.set_thumbnail(url=url)
    em.set_footer(text=f"do \"{p}help <command>\" to see the details of a command.")

    return em

def help_command_embed(title, desc, perms, uL):
    em = discord.Embed(color = 0xadcca6, title=title, description=desc)
    em.add_field(name="Permissions", value=perms, inline=False)
    em.add_field(name="Usage", value=uL, inline=False)

    return em

def help_embed(p):
     em = discord.Embed(color = 0xadcca6, title="Project Ax")
     em.add_field(name="Profile", value="`Profile` - Create & manage your profile\n`Inventory` - Check your inventory or vault")
     em.add_field(name="Combat", value="`Training` - Try out your stats & items\n`PvP` - Challenge your friends", inline=False)
     em.add_field(name="Bot Configuration", value="`Configuration` - Configure the bot's settings\n`Miscellaneous` - Get some universal bot information\n`Help` - View all the help commands", inline=False)
     em.set_footer(text = f"do \"{p}cmds <module>\" to see all commands in a module.")
     em.set_thumbnail(url = _json.get_art()["bot_icon_longsword"])

     return em


def pvp_message(m, n): return f"**{m}**, {n} challenged you to a friendly PvP battle!"



# errors
def error_1(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Something went wrong.")
    return em

def error_2(a,b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** The command was canceled.")
    return em

def error_3(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Couldn't find that command.")
    return em

def error_4(a, b):
    em=discord.Embed(color=0xadcca6, description=f"**{a}#{b}** Couldn't find that module.")
    return em
