import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from StuffsWeNeed import _db
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
    async def inventory(self, ctx):
        main_weapon = _db.get_weapons(ctx.message.author.id)[0]
        secondary_weapon = _db.get_weapons(ctx.message.author.id)[1]
        main_weapon_xp = _db.get_weapons(ctx.message.author.id)[2]
        secondary_weapon_xp = _db.get_weapons(ctx.message.author.id)[3]
        main_weapon_e = _db.main_weapon_e_picker(main_weapon)
        secondary_weapon_e = _db.secondary_weapon_e_picker(secondary_weapon)
        balance = _db.get_balance(ctx.message.author.id)
        p = _db.get_prefix(ctx.message.guild.id)
        healing_potion = _db.get_items(ctx.message.author.id)


        em=discord.Embed(color=0xadcca6, title=f"Inventory", description=f"Balance: {balance}")
        em.add_field(name="Weapons", value=f"{main_weapon_e} {main_weapon} - xp: `{main_weapon_xp}`\n{secondary_weapon_e} {secondary_weapon} - xp: `{secondary_weapon_xp}`")
        em.add_field(name="Items", value=f"Healing potion - `{healing_potion}`", inline=False)
        em.set_footer(text=f"Do \"{p}inv <weapon/item>\" to see more info.")

        await ctx.send(embed=em)

        

def setup(client):
    client.add_cog(inventory(client))