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


            ## ASK WHICH DUMMY STATS TO USE
            message = await ctx.send(embed=embeds.dummy_stat_embed_1(ctx.author.name, ctx.author.discriminator))
            await message.add_reaction(emoji='1️⃣')
            await message.add_reaction(emoji='2️⃣')
            await message.add_reaction(emoji='3️⃣')
            await message.add_reaction(emoji='4️⃣')
            await message.add_reaction(emoji='5️⃣')
            await message.add_reaction(emoji='🛑')

            def checkforR1(reaction, msg):
                return msg == ctx.message.author and reaction.emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '🛑']

            reaction, msg = await self.client.wait_for('reaction_add', timeout=120, check=checkforR1)

            # OPTION 4 - CHOOSE PREVIOUS DUMMY STATS
            if reaction.emoji == '4️⃣':
                await message.clear_reactions()
                if _db.get_training_status(ctx.message.author.id):
                    dmg = _db.get_dummy_stats(ctx.message.author.id, 'd_dmg')
                    acc = _db.get_dummy_stats(ctx.message.author.id, 'd_acc')
                    df = _db.get_dummy_stats(ctx.message.author.id, 'd_def')
                    spd = _db.get_dummy_stats(ctx.message.author.id, 'd_spd')
                    hp = _db.get_dummy_stats(ctx.message.author.id, 'd_hp')
                else:
                    await ctx.send(embed=discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I can't find anything, seems like you're playing training mode for the first time! Try again."))
                    return


            # OPTION 5 - CHOOSE YOUR OWN WEAPON
            if reaction.emoji == '5️⃣':
                await message.clear_reactions()
                await message.edit(embed=embeds.dummy_stat_embed_2(ctx.author.name, ctx.author.discriminator))
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

                dmg = int(dummyS[0].strip())
                acc = int(dummyS[1].strip())
                df = int(dummyS[2].strip())
                spd = int(dummyS[3].strip())
                hp = int(dummyS[4].strip())
            ################################################################################################
            ################################################################################################

            # SHUT DOWN
            if reaction.emoji == '🛑':
                await ctx.send(embed=embeds.error_2(ctx.author.name, ctx.author.discriminator))
                return


            d_dmg = dmg
            d_acc = acc
            d_def = df
            d_spd = spd
            d_hp = hp

            ## SAVE DUMMY STATS TO DATABASE
            collection = db["Training"]
            collection.update_one({"_id": ctx.message.author.id}, {"$set":{"d_dmg": d_dmg, "d_acc": d_acc, "d_def": d_def, "d_spd": d_spd, "d_hp": d_hp}}, upsert=True)


            # ask which weapon to use
            em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Which weapon do you want to use? You can choose between your equipped primary & secondary weapons. ")
            em.set_footer(text="React with the corresponding weapon")
            await message.edit(embed=em)

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

            # player's stats
            p_dmg = combat.get_player_stats(weapon)[0]
            p_acc = combat.get_player_stats(weapon)[1]
            p_def = combat.get_player_stats(weapon)[2]
            p_spd = combat.get_player_stats(weapon)[3]
            p_hp = 250

            prHP_d=d_hp
            prHP_p = p_hp
            moves=0
            misses=0

            # the fight
            while d_hp > 0 and p_hp > 0:

                ## FIRST EMBED DISPLAY, BEFORE BATTLE
                if moves == 0:
                    miss_counter_d = ""
                    miss_counter_p = ""
                    hit_counter_d = ""
                    hit_counter_p = ""
                    HorM_d = ""
                    HorM_p = ""
                    misses_d = 0
                    misses_p = 0
                    hits_d = 0
                    hits_p = 0
                    player_move_indicator = ""
                    dummy_move_indicator = ""
                    await message.edit(embed=embeds.pve_combat_embed(p_hp, weapon, p_dmg, p_acc, p_def, p_spd, d_hp, thumbnail, title, enemy, HorM_p, HorM_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, dummy_move_indicator, tools.ismain()))


                ## PLAYER'S TURN
                player_move_indicator = "\> "
                dummy_move_indicator = ""

                d_hp = combat.attack(p_dmg, p_acc, d_def, d_hp)
                moves += 1

                HorM_p = combat.hit_or_miss(d_hp, prHP_d, moves)

                if HorM_p == "- Miss!":
                    misses_p += 1
                    hits_p = 0
                else:
                    misses_p = 0
                    hits_p += 1

                miss_counter_p = combat.miss_counter(misses_p)
                hit_counter_p = combat.hit_counter(hits_p)

                prHP_d = d_hp

                await message.edit(embed=embeds.pve_combat_embed(p_hp, weapon, p_dmg, p_acc, p_def, p_spd, d_hp, thumbnail, title, enemy, HorM_p, HorM_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, dummy_move_indicator, tools.ismain()))

                await asyncio.sleep(1)


                ## DUMMY'S TURN
                player_move_indicator = ""
                dummy_move_indicator = "\> "

                p_hp = combat.attack(d_dmg, d_acc, p_def, p_hp)
                moves += 1

                HorM_d = combat.hit_or_miss(p_hp, prHP_p, moves)

                if HorM_d == "- Miss!":
                    misses_d += 1
                    hits_d = 0
                else:
                    hits_d += 1
                    misses_d = 0

                miss_counter_d = combat.miss_counter(misses_d)
                hit_counter_d = combat.hit_counter(hits_d)

                prHP_p = p_hp

                await message.edit(embed=embeds.pve_combat_embed(p_hp, weapon, p_dmg, p_acc, p_def, p_spd, d_hp, thumbnail, title, enemy, HorM_p, HorM_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, dummy_move_indicator, tools.ismain()))

                await asyncio.sleep(1)


            ## RESULTS
            winner = combat.winner(p_hp, d_hp)
            if winner == "Enemy": winner = "Training Dummy"
            else:
                thumbnail = _db.get_profile_looks(ctx.message.author.id)

            await message.edit(embed=embeds.pve_combat_embed_winner(p_hp, d_hp, thumbnail, title, enemy, winner))


        ## TIMEOUT - INTERACTION
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))


def setup(client):
    client.add_cog(training(client))
