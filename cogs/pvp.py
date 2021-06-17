import discord
from discord.ext import commands
from discord.ext.commands import cog
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from tools import _db, embeds, combat, _json, tools
import asyncio

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
      print ('pvp.py -> on_ready()')

    @commands.command()
    async def pvp(self, ctx, target: discord.Member, param=None):
        # PROFILE CHECKS
        if (await _db.profile_check(ctx.author.id) == 0):
            await ctx.send(embed=discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake."))
            return


        if (await _db.profile_check(target.id) == 0):
            await ctx.send(embed=discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** The user you're challenging doesn't have a Project Ax profile yet. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake."))
            return



        pvp_message = await ctx.send(embeds.pvp_message(target.display_name, ctx.author.display_name ))

        await pvp_message.add_reaction(emoji='✅')
        await pvp_message.add_reaction(emoji='🛑')

        def checkforR(reaction, msg):
            return msg == target and reaction.emoji in ['✅', '🛑']

        reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)
        await pvp_message.clear_reactions()

        if reaction.emoji == '🛑':
            await pvp_message.clear_reactions()
            latestMsg = pvp_message.content
            await pvp_message.edit(content=f"{latestMsg}\n**{target.display_name}** ran away!")



        ## PLAYER AGREES TO PVP
        if reaction.emoji == '✅':

            # select weapons
            weapon_p = await combat.weapon_select(ctx.author, pvp_message, self.client)
            await pvp_message.clear_reactions()

            weapon_e = await combat.weapon_select(target, pvp_message, self.client)
            await pvp_message.clear_reactions()

            # get players stats
            # player
            p_atk = combat.get_player_stats(weapon_p)[0]
            p_acc = combat.get_player_stats(weapon_p)[1]
            p_def = combat.get_player_stats(weapon_p)[2]
            p_hp = 500

            # enemy
            e_atk = combat.get_player_stats(weapon_e)[0]
            e_acc = combat.get_player_stats(weapon_e)[1]
            e_def = combat.get_player_stats(weapon_e)[2]
            e_hp = 500

            # some extra needed variables
            thumnail = "https://media.discordapp.net/attachments/804705780557021214/840565105959632926/pixil-frame-0_37.png"
            title = "TempTitle/pvp"
            enemy = target.display_name
            player = target.display_name
            hit_or_miss_p = 0
            hit_or_miss_d = 0
            miss_counter_p = ""
            miss_counter_d = ""
            hit_counter_p = ""
            hit_counter_d = ""


            # display embed before actual combat
            embeds.pvp_combat_embed(p_hp, e_hp, thumnail, title, enemy, player, hit_or_miss_p, hit_or_miss_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, enemy_move_indicator, beta)

            # pvp starts
            while p_hp > 0 and e_hp > 0:





def setup(client):
    client.add_cog(training(client))
