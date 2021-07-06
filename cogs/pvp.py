import discord
from discord.ext import commands
from discord.ext.commands import cog
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from tools import _db, embeds, combat, _json, tools
import asyncio
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class pvp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      DiscordComponents(self.client)
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


        buttons_1=[
            Button(style=ButtonStyle.blue, label="Accept"),
            Button(style=ButtonStyle.red, label="Run Away"),
        ],

        pvp_message = await ctx.send(embeds.pvp_message(target.display_name, ctx.author.display_name), components=list(buttons_1))

        def checkforR(button, msg):
            return msg == target and button.name in ["Accept", "Run Away"]


        # try:
        button, msg = await self.client.wait_for("button_click", check=checkforR, timeout=15)

        # except:
        #     await pvp_message.edit(components=[
        #         Button(style=ButtonStyle.red, label="Timed Out!", disabled=True),
        #         ],
        #     )

        #     return 


        if button.name == "Run Away":
            await pvp_message.edit(
                f"{pvp_message.content}\n**{target.display_name}** ran away!",
                components=[]
            )

        ## PLAYER AGREES TO PVP
        if button.name == "Accept":

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
            p_start_hp = 500

            # enemy
            e_atk = combat.get_player_stats(weapon_e)[0]
            e_acc = combat.get_player_stats(weapon_e)[1]
            e_def = combat.get_player_stats(weapon_e)[2]
            e_hp = 500
            e_start_hp = 500

            # some extra needed variables
            thumnail = "https://media.discordapp.net/attachments/804705780557021214/840565105959632926/pixil-frame-0_37.png"
            title = "TempTitle/pvp"
            enemy = target.display_name
            player = ctx.author.display_name
            hit_or_miss_p = ""
            hit_or_miss_d = ""
            miss_counter_p = ""
            miss_counter_d = ""
            hit_counter_p = ""
            hit_counter_d = ""
            player_move_indicator = ""
            enemy_move_indicator = ""
            comment = "Happy Project Ax fighting, and may the odds be ever in your favor."
            moves = 0


            # display embed before actual combat
            def display_pvp_embed():
                return embeds.pvp_combat_embed(p_hp, p_atk, p_acc, p_def, e_hp, e_atk, e_acc, e_def, thumnail, title, enemy, player, comment, hit_or_miss_p, hit_or_miss_d, miss_counter_p, miss_counter_d, hit_counter_p, hit_counter_d, moves, player_move_indicator, enemy_move_indicator, tools.ismain())

            await pvp_message.edit(embed=display_pvp_embed())
            await pvp_message.edit(content=f"**{player}** Your turn! React to this message to make a move.\n\n{comment}")

            # add reactions
            await pvp_message.add_reaction(emoji='⚔️')
            await pvp_message.add_reaction(emoji='🛡️')

            healing_potion_emote = self.client.get_emoji(_json.get_emote_id("healing_potion"))
            await pvp_message.add_reaction(emoji=healing_potion_emote)

            def checkforR2(reaction, msg):
                return msg == target and reaction.emoji in ['⚔️', '🛡️', healing_potion_emote]
            def checkforR3(reaction, msg):
                return msg == ctx.author and reaction.emoji in ['⚔️', '🛡️', healing_potion_emote]

            # pvp starts
            while p_hp > 0 and e_hp > 0:


                if moves%2 != 0:
                    ## PLAYER MOVE
                    await pvp_message.edit(content=f"**{player}** Your turn! React to this message to make a move.\n\n{comment}")
                    reaction, msg = await self.client.wait_for('reaction_add', timeout=10, check=checkforR3)
                    await pvp_message.remove_reaction(reaction.emoji, ctx.author)

                    if reaction.emoji == '⚔️':
                        e_hp = combat.pvp_atk(e_hp, p_atk, p_acc, e_def, player)[1]
                        comment = str(combat.pvp_atk(e_hp, p_atk, p_acc, e_def, player)[2])



                    elif reaction.emoji == '🛡️':
                        pass


                    elif reaction.emoji == healing_potion_emote:
                        incr = p_hp*0.1

                        if p_hp != p_start_hp:
                            if p_start_hp < (p_hp+incr):
                                incr = p_start_hp - p_hp

                            p_hp += incr
                            comment = f"{player} healed! Their health increased with {incr} points."

                        else:
                            if p_hp == p_start_hp:
                                comment = f"{player} tried to heal but their health is already maxed."


                else:
                    ## ENEMY MOVE
                    await pvp_message.edit(content=f"**{enemy}** Your turn! React to this message to make a move.\n\n{comment}")
                    reaction, msg = await self.client.wait_for('reaction_add', timeout=10, check=checkforR2)
                    await pvp_message.remove_reaction(reaction.emoji, target)


                await pvp_message.edit(embed=display_pvp_embed())
                await pvp_message.edit(content=f"{pvp_message.content}\n\n{comment}")
                comment = ""
                moves+=1


def setup(client):
    client.add_cog(pvp(client))
