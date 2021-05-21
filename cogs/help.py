import discord
from discord.ext import commands
from tools import _db

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('help.py -> on_ready()')

    @commands.group(invoke_without_command=True, aliases=['h'])
    async def help(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(color = 0xadcca6, title="Project Ax")

      em.add_field(name="Modules", value="`Configuration`\n`Profile`\n`Miscellaneous`\n`Bot Admin Only`")
      em.set_footer(text = f"do \"{p}help <module>\" to see all commands in a module.")
      em.set_thumbnail(url = "https://media.discordapp.net/attachments/839537047470473227/840579240088043560/pixil-frame-0_40.png?width=425&height=425")
      await ctx.send(embed = em)
    
    # list of modules;
    @help.command(aliases=['configuration'])
    async def config(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(color = 0xadcca6, title="Project Ax Configuration")
      em.add_field(name="Commands", value=f"`{p}prefix`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text=f"do \"{p}help <command>\" to see the details of a command.")
      await ctx.send(embed=em)

    @help.command()
    async def profiles(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(color = 0xadcca6, title="Project Ax Profiles")
      em.add_field(name="Commands", value=f"`{p}createprofile` / `{p}cp`\n`{p}profile` / `{p}p`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text=f"do \"{p}help <command>\" to see the details of a command.")
      await ctx.send(embed=em)  

    @help.command(aliases=['misc'])
    async def miscellaneous(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(color = 0xadcca6, title="Project Ax Miscellaneous")
      em.add_field(name="Commands", value=f"`{p}ping`\n`{p}invite`\n`{p}readme`\n`{p}say`\n`{p}stats`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text=f"do \"{p}help <command>\" to see the details of a command.")
      await ctx.send(embed=em)  

    @help.command(aliases=['botadmin', 'botadminonly', 'admin', 'bot', 'owneronly', 'adminonly'])
    async def admin_only(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(color = 0xadcca6, title="Project Ax Admin Only")
      em.add_field(name="Commands", value=f"`{p}die`\n`{p}delprofile`\n`{p}editprofile`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text=f"do \"{p}help <command>\" to see the details of a command.")
      await ctx.send(embed=em)

    # commands
    @help.command()
    async def prefix(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`prefix`", description = f"Changes the bot's prefix. Do `{p}prefix ax` or `{p}prefix default` to change it back to the default one. To see the bot's current prefix, do `@ProjectAx prefix`", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "ManageGuild Permission", inline=False)
      em.add_field(name = "Usage", value = f"`{p}prefix`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['cprofile', 'createp', 'cp'])
    async def createprofile(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`createprofile` / `cp`", description = "Create a Project Ax profile!", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}createprofile`\n`{p}cp`\n`{p}cprofile`", inline=False)
      
      await ctx.send(embed = em)

    @help.command(aliases=['p'])
    async def profile(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`profile` / `p`", description = f"Shows your Project Ax profile. If you don't already have one, create a profile by doing `{p}createprofile`!", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}profile`\n`{p}p`", inline=False)

      await ctx.send(embed = em)
    
    @help.command()
    async def ping(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`prefix`", description = "Shows the bot's latency.", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}prefix`", inline=False)

      await ctx.send(embed = em)
    
    @help.command()
    async def invite(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`invite`", description = "Invite Project Ax to your own server!", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}invite`", inline=False)

      await ctx.send(embed = em)
    
    @help.command(aliases=['docs'])
    async def readme(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`readme` / `docs`", description = "shows Project Ax's Docs", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}readme`\n`{p}docs`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['repeat'])
    async def say(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`say` / `repeat`", description = "Make the bot say something!", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "ManageGuild Permission", inline=False)
      em.add_field(name = "Usage", value = f"`{p}say Hi, I'm super cool!`\n`{p}repeat \"Project Ax is so cool..\"`", inline=False)

      await ctx.send(embed = em)

    @help.command()
    async def stats(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`stats`", description = "Displays Project Ax's stats.", color = 0xadcca6)
      em.add_field(name = "Usage", value = f"`{p}stats`", inline=False)

      await ctx.send(embed = em)
    
    @help.command()
    async def die(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`die`", description = "Kills and restarts the bot. Add a \"pull\" parameter to make it update by pulling from the [GitHub](https://github.com/Dok4440/ProjectAx).", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = f"`{p}die`\n`{p}die pull`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['delp', 'deletep'])
    async def delprofile(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`delprofile` / `delp`", description = "Deletes a Project Ax profile. This action is irreversable.", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = f"`{p}delprofile 387984284734062592`", inline=False)

      await ctx.send(embed = em)
  
    @help.command(aliases=['editp', 'eprofile'])
    async def editprofile(self, ctx):
      p = _db.get_prefix(ctx.message.guild.id)

      em = discord.Embed(title = "`editprofile` / `editp`", description = "Edits a Project Ax profile. List of things you can change; `age`, `world`, `district`, `first_name`, `last_name`, `friend_id`, `gender`, `height`, `looks`, `xp`.", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = f"`{p}editprofile @Dok first_name \"Chad\"`\n`{p}editp @JuicBblue age 69`", inline=False)

      await ctx.send(embed = em)

def setup(client):
    client.add_cog(Help(client))