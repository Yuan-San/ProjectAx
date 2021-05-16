import discord
from discord.ext import commands
from discord.ext.commands import cog
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from StuffsWeNeed import _db, defaultstuff, embeds, combat
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class training(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('training.py -> on_ready()')
    
    @commands.command()
    async def train(self, ctx):

        # check if profile (& thus inv) exists.
        check = db["Profile"].count_documents({"_id": ctx.message.author.id})
        if check == 0:
            em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")

            await ctx.send(embed=em)
            return
        
        # ask which weapon to use
        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Which weapon do you want to use? You can choose between your equipped primary & secondary weapons. ")
        em.set_footer(text="React with the corresponding weapon")
        message = await ctx.send(embed=em)

        primary_emote = self.client.get_emoji(combat.get_weapon_emote_id(combat.get_weapons(ctx.message.author.id)[0]))
        secondary_emote = self.client.get_emoji(combat.get_weapon_emote_id(combat.get_weapons(ctx.message.author.id)[1]))

        await message.add_reaction(emoji=primary_emote)
        await message.add_reaction(emoji=secondary_emote)
        await message.add_reaction(emoji='🛑')

        def checkforR(reaction, msg):
            return msg == ctx.message.author and reaction.emoji in [primary_emote, secondary_emote, '🛑']
        
        reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

        if reaction.emoji == primary_emote: weapon = combat.get_weapons(ctx.message.author.id)[0]
        elif reaction.emoji == secondary_emote: weapon = combat.get_weapons(ctx.message.author.id)[1]
        elif reaction.emoji == '🛑':
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return

        # dummy's stats
        d_dmg = 0
        d_acc = 0
        d_def = 0
        d_spd = 20
        d_hp = 10000

        # player's stats
        p_dmg = combat.get_player_stats(weapon)[0]
        p_acc = combat.get_player_stats(weapon)[1]
        p_def = combat.get_player_stats(weapon)[2]
        p_spd = combat.get_player_stats(weapon)[3]
        p_hp = 1000

        # the fight

        


def setup(client):
    client.add_cog(training(client))