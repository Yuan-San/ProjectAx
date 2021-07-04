import discord
from discord.ext import commands
from discord.ext.commands import cog
from tools import _db, _json, embeds
import typing

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('help.py -> on_ready()')

    # modules;
    @commands.command(aliases=['modules', "mdls", "mdl", 'cmds', 'cmd'])
    async def module(self, ctx, param: typing.Optional[str]):

        if param == None:
            await ctx.send(embed=embeds.help_embed(_db.get_prefix(ctx.message.guild.id)))
            return

        p = _db.get_prefix(ctx.message.guild.id)

        botCog = [i for i in _json.get_help()["modules"] if i.lower().startswith(param.lower())]
        module = _json.get_help()["modules"][botCog[0]]
        cog = self.client.get_cog(botCog[0])

        cmdList = ""
        for cmd in cog.get_commands():
            cmdList += "`" + str(p) + str(cmd) + "`\n"

        title = f"Project Ax {botCog[0].capitalize()}"

        em = embeds.help_module_embed(title, cmdList, _json.get_art()["bot_icon_greatsword"], p)
        await ctx.send(embed=em)

    @module.error
    async def module_error(self, ctx, error):
        await ctx.send(embed=embeds.error_4(ctx.author.name, ctx.author.discriminator))

    # commands
    @commands.command(aliases=['h'])
    async def help(self, ctx, param: typing.Optional[str]):

        if param == None:
            await ctx.send(embed=embeds.help_embed(_db.get_prefix(ctx.message.guild.id)))
            return

        p = _db.get_prefix(ctx.message.guild.id)

        botCommand = self.client.get_command(param.lower())

        try:
            command = _json.get_help()["commands"][str(botCommand)]
        except:
            command = _json.get_help()["commands"]["no_command_data"]

        uL = ""
        for usage in command["usage"]:
            uL += "`" + usage.replace("{0}", str(p)) + "`\n"

        cmds = botCommand.aliases
        cL = "`" + str(botCommand) + "`"
        for cmd in cmds:
            cL += " / `" + cmd + "`"

        em = embeds.help_command_embed(cL, command["desc"], command["perms"], uL)
        await ctx.send(embed=em)

    @help.error
    async def help_error(self, ctx, error):
        await ctx.send(embed=embeds.error_3(ctx.author.name, ctx.author.discriminator))


def setup(client):
    client.add_cog(help(client))
