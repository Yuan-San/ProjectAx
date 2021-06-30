import discord
from discord.ext import commands
from tools import _db, _json, embeds

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('help.py -> on_ready()')

    # modules;
    @commands.command(aliases=['modules', "mdls", "mdl", 'cmds', 'cmd'])
    async def module(self, ctx, param):
        p = _db.get_prefix(ctx.message.guild.id)
        module = _json.get_help()["modules"][param]

        cmdList = ""
        for cmd in module["commands"]:
            cmdList += "`" + cmd.replace("{0}", str(p)) + "`\n"

        em = embeds.help_module_embed(module["title"], cmdList, _json.get_art()["bot_icon_greatsword"], p)
        await ctx.send(embed=em)

    @module.error
    async def module_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'param':
                await ctx.send(embed=embeds.help_embed(_db.get_prefix(ctx.message.guild.id)))
        else:
            await ctx.send(embed=embeds.error_4(ctx.author.name, ctx.author.discriminator))

    # commands
    @commands.command(aliases=['h'])
    async def help(self, ctx, param):
        p = _db.get_prefix(ctx.message.guild.id)

        botCommand = self.client.get_command(param.lower())
        command = _json.get_help()["commands"][str(botCommand)]

        uL = ""
        for usage in command["usage"]:
            uL += "`" + usage.replace("{0}", str(p)) + "`\n"

        # cmds = command["cmd"].split(' ')
        cmds = botCommand.aliases
        cL = "`" + str(botCommand) + "`"
        for cmd in cmds:
            cL += " / `" + cmd + "`"

        em = embeds.help_command_embed(cL, command["desc"], command["perms"], uL)
        await ctx.send(embed=em)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'param':
                await ctx.send(embed=embeds.help_embed(_db.get_prefix(ctx.message.guild.id)))
        else:
            await ctx.send(embed=embeds.error_3(ctx.author.name, ctx.author.discriminator))


def setup(client):
    client.add_cog(Help(client))
