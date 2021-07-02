import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import time, datetime
from discord.ext.commands import MemberConverter
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
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user, *, reason=None):

        try:
            target = await self.client.fetch_user(int(user))
        except:
            target = await MemberConverter().convert(ctx, user)

            if tools.hierarchy_check(ctx.author, target) == 0:
                await ctx.send(embed=embeds.error_5(ctx.author.name, ctx.author.discriminator))
                return

        if reason==None: reason = "*No reason given*"
        actualReason = ctx.author.name + "#" + ctx.author.discriminator + " | " + str(reason)

        await ctx.guild.ban(target, reason=actualReason)

        await ctx.send(embed=embeds.ban_success(ctx.author.name, ctx.author.discriminator, target, reason))


    @commands.command(aliases=['ub', 'pardon'])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        target = await self.client.fetch_user(id)

        await ctx.guild.unban(target)

        await ctx.send(embed=embeds.unban_success(ctx.author.name, ctx.author.discriminator, target))

    @commands.command(aliases=['sb'])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, target: discord.Member, *, reason=None):

        if reason==None: reason = "*No reason given*"
        actualReason = ctx.author.name + "#" + ctx.author.discriminator + " | " + str(reason)

        if tools.hierarchy_check(ctx.author, target) == 0:
            await ctx.send(embed=embeds.error_5(ctx.author.name, ctx.author.discriminator))
            return

        await ctx.guild.ban(target, reason=actualReason)
        await ctx.guild.unban(target)

        await ctx.send(embed=embeds.softban_success(ctx.author.name, ctx.author.discriminator, target, reason))


    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, target: discord.Member, *, reason=None):

        if reason==None: reason = "*No reason given*"
        actualReason = ctx.author.name + "#" + ctx.author.discriminator + " | " + str(reason)

        if tools.hierarchy_check(ctx.author, target) == 0:
            await ctx.send(embed=embeds.error_6(ctx.author.name, ctx.author.discriminator))
            return

        await ctx.guild.kick(target, reason=actualReason)

        await ctx.send(embed=embeds.kick_success(ctx.author.name, ctx.author.discriminator, target, reason))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, target: discord.Member, *, reason=None):

        if reason==None: reason = "*No reason given*"
        collection = db["Warnings"]

        # check if the target already have a warning log
        if _db.warning_doc_check(target.id, ctx.guild.id) == 0:
            _db.create_warning_log(target.id, ctx.guild.id)

        # # check warnings in that log
        warning_num = _db.get_warning_num(target.id, ctx.guild.id)
        # add warning
        collection.update_one({"_id": f"{target.id} @ {ctx.guild.id}"}, {"$set":{f"warning_{warning_num}": f"{ctx.author.id} @ {time.time()} -///- {reason}"}}, upsert=True)

        # output
        await ctx.send(embed=embeds.warn_success(target))

    @commands.command(aliases=['warnings'])
    @commands.has_permissions(kick_members=True)
    async def warnlog(self, ctx, target: discord.Member):

        pass

    @commands.command(aliases=['showw', 'showwarning', 'show_warning'])
    @commands.has_permissions(kick_members=True)
    async def warning(self, ctx, target: discord.Member, w_id: int):

        target = tools.get_target(target, ctx.author.id)

        try:
            warning = _db.get_warning(target, w_id)
        except:
            await ctx.send(embed=embeds.error_7(ctx.author.name, ctx.author.discriminator))




def setup(client):
    client.add_cog(moderation(client))
