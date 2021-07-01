import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from tools import _db, _json, tools, embeds

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('moderation.py -> on_ready()')

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member, *, reason=None):
        if reason==None: reason = "*No reason given*"
        actualReason = ctx.author.name + "#" + ctx.author.discriminator + " | " + str(reason)

        if tools.hierarchy_check(ctx.author, target) == 0:
            await ctx.send(embed=embeds.error_5(ctx.author.name, ctx.author.discriminator))
            return

        try:
            await ctx.guild.ban(target, reason=actualReason)
        except:
            await ctx.send(embed=embeds.error_5(ctx.author.name, ctx.author.discriminator))
            return

        await ctx.send(embed=embeds.ban_success(ctx.author.name, ctx.author.discriminator, target, reason))




def setup(client):
    client.add_cog(moderation(client))
