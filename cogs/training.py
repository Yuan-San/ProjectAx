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
      print ('training.py -> on_ready()')

    @commands.command()
    async def train(self, ctx):

        try:
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

            primary_emote = self.client.get_emoji(_json.get_emote_id(combat.get_weapons(ctx.message.author.id)[0]))
            secondary_emote = self.client.get_emoji(_json.get_emote_id(combat.get_weapons(ctx.message.author.id)[1]))

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

            await message.clear_reactions()

            thumbnail = "https://media.discordapp.net/attachments/804705780557021214/843115592319107113/pixil-frame-0_45.png"
            title = "Training Mode"
            enemy = "Dummy"


            # ask for dummy stats
            await message.edit(embed=embeds.dummy_stat_embed(ctx.author.name, ctx.author.discriminator))
            msg = await self.client.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)

            await msg.delete()

            dummyS=msg.content.lower().split(',')
            print(dummyS[0].strip(), dummyS[1].strip(), dummyS[2].strip(), dummyS[3].strip(), dummyS[4].strip())

            for i in dummyS:
                if int(i.strip())>5000 or int(i.strip())<0:
                    await ctx.send(embed=discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Woah there! Those numbers you use are not allowed, please use numbers between **0** and **5000**"))
                    return

            if int(dummyS[3].strip()) < 500:
                await ctx.send(embed=discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Because we don't want our bot to explode, we don't allow combat speeds below **500** milliseconds. Try again :/"))
                return

            # dummy's stats
            d_dmg = int(dummyS[0].strip())
            d_acc = int(dummyS[1].strip())
            d_def = int(dummyS[2].strip())
            d_spd = int(dummyS[3].strip())
            d_hp = int(dummyS[4].strip())

            # player's stats
            p_dmg = combat.get_player_stats(weapon)[0]
            p_acc = combat.get_player_stats(weapon)[1]
            p_def = combat.get_player_stats(weapon)[2]
            p_spd = combat.get_player_stats(weapon)[3]
            p_hp = 500

            prHP_d=d_hp
            prHP_p = p_hp
            moves=0
            misses=0

            # the fight
            while d_hp > 0 and p_hp > 0:

                HorM_p = combat.hit_or_miss(d_hp, prHP_d, moves)
                HorM_d = combat.hit_or_miss(p_hp, prHP_p, moves)

                # miss counter
                # player
                if HorM_p == "- Miss!":
                    misses_p += 1
                else:
                    misses_p = 0

                # dummy
                if HorM_d == "- Miss!":
                    misses_d += 1
                else:
                    misses_d = 0

                miss_counter_p = combat.miss_counter(misses_p)
                miss_counter_d = combat.miss_counter(misses_d)

                prHP_d = d_hp
                prHP_p = p_hp

                await message.edit(embed=embeds.pve_combat_embed(p_hp, weapon, p_dmg, p_acc, p_def, p_spd, d_hp, thumbnail, title, enemy, HorM_p, HorM_d, miss_counter_p, miss_counter_d, moves, tools.ismain()))

                # player move
                d_hp = combat.attack(p_dmg, p_acc, d_def, d_hp)
                moves += 1

                # turn based for now.
                await asyncio.sleep(1)

                # dummy move
                p_hp = combat.attack(d_dmg, d_acc, p_def, p_hp)
                moves += 1

            # results
            winner = combat.winner(p_hp, d_hp)
            if winner == "Enemy": winner = "Training Dummy"
            else:
                thumbnail = _db.get_profile_looks(ctx.message.author.id)

            await message.edit(embed=embeds.pve_combat_embed_winner(p_hp, d_hp, thumbnail, title, enemy, winner))


        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))


def setup(client):
    client.add_cog(training(client))
