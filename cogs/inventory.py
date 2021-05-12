import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from StuffsWeNeed import _db, embeds
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class inventory(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('inventory -> on_ready()')

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, *, target: discord.Member=None):
        
        # find who's profile to pull up.
        target = embeds.get_target(target, ctx.message.author.id)

        # inventory variables
        main_weapon = _db.get_weapons(target)[0]
        secondary_weapon = _db.get_weapons(target)[1]
        main_weapon_xp = _db.get_weapons(target)[2]
        secondary_weapon_xp = _db.get_weapons(target)[3]
        main_weapon_e = _db.main_weapon_e_picker(main_weapon)
        secondary_weapon_e = _db.secondary_weapon_e_picker(secondary_weapon)
        balance = _db.get_balance(target)
        p = _db.get_prefix(ctx.message.guild.id)
        healing_potion = _db.get_items(target)

        # create inventory embed
        em = embeds.inventory_embed(balance, main_weapon_e, main_weapon, main_weapon_xp, secondary_weapon_e, secondary_weapon, secondary_weapon_xp, healing_potion, p)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(inventory(client))