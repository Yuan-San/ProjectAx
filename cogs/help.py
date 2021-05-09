import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('Help module is ready.')

    @commands.group(invoke_without_command=True, aliases=['h'])
    async def help(self, ctx):
      em = discord.Embed(color = 0xadcca6, title="Project Ax")

      em.add_field(name="Modules", value="`Configuration`\n`Profile`\n`Miscellaneous`\n`Bot Admin Only`")
      em.set_footer(text = "do \"ax help <module>\" to see all commands in a module.",)
      em.set_thumbnail(url = "https://media.discordapp.net/attachments/839537047470473227/840579240088043560/pixil-frame-0_40.png?width=425&height=425")
      await ctx.send(embed = em)
    
    # list of modules;
    @help.command(aliases=['configuration'])
    async def config(self, ctx):
      em = discord.Embed(color = 0xadcca6, title="Project Ax Configuration")
      em.add_field(name="Commands", value="`ax prefix`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text="do \"ax help <command>\" to see the details of a command.")
      await ctx.send(embed=em)

    @help.command()
    async def profiles(self, ctx):
      em = discord.Embed(color = 0xadcca6, title="Project Ax Profiles")
      em.add_field(name="Commands", value="`ax createprofile` / `ax cp`\n`ax profile` / `ax p`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text="do \"ax help <command>\" to see the details of a command.")
      await ctx.send(embed=em)  

    @help.command(aliases=['misc'])
    async def miscellaneous(self, ctx):
      em = discord.Embed(color = 0xadcca6, title="Project Ax Miscellaneous")
      em.add_field(name="Commands", value="`ax ping`\n`ax invite`\n`ax readme`\n`ax say`\n`ax stats`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text="do \"ax help <command>\" to see the details of a command.")
      await ctx.send(embed=em)  

    @help.command(aliases=['botadmin', 'botadminonly', 'admin', 'bot', 'owneronly', 'adminonly'])
    async def admin_only(self, ctx):
      em = discord.Embed(color = 0xadcca6, title="Project Ax Admin Only")
      em.add_field(name="Commands", value="`ax die`\n`ax delprofile`\n`ax editprofile`")
      em.set_thumbnail(url="https://media.discordapp.net/attachments/839537047470473227/840563743284133908/pixil-frame-0_37.png?width=425&height=425")
      em.set_footer(text="do \"ax help <command>\" to see the details of a command.")
      await ctx.send(embed=em)


    @help.command()
    async def prefix(self, ctx):
      em = discord.Embed(title = "`prefix`", description = f"Changes the bot's prefix. Do `ax prefix ax` or `ax prefix default` to change it back to the default one. To see the bot's current prefix, do `@ProjectAx prefix`", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "ManageGuild Permission", inline=False)
      em.add_field(name = "Usage", value = "`ax prefix`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['cprofile', 'createp', 'cp'])
    async def createprofile(self, ctx):
      em = discord.Embed(title = "`createprofile` / `cp`", description = "Create a Project Ax profile!", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax createprofile`\n`ax cp`\n`ax cprofile`", inline=False)
      
      await ctx.send(embed = em)

    @help.command(aliases=['p'])
    async def profile(self, ctx):
      em = discord.Embed(title = "`profile` / `p`", description = "Shows your Project Ax profile. If you don't already have one, create a profile by doing `ax createprofile`!", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax profile`\n`ax p`", inline=False)

      await ctx.send(embed = em)
    
    @help.command()
    async def ping(self, ctx):
      em = discord.Embed(title = "`prefix`", description = "Shows the bot's latency.", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax prefix`", inline=False)

      await ctx.send(embed = em)
    
    @help.command(aliases=['inv'])
    async def invite(self, ctx):
      em = discord.Embed(title = "`invite` / `inv`", description = "Invite Project Ax to your own server!", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax invite`\n`ax inv`", inline=False)

      await ctx.send(embed = em)
    
    @help.command(aliases=['docs'])
    async def readme(self, ctx):
      em = discord.Embed(title = "`readme` / `docs`", description = "shows Project Ax's Docs", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax readme`\n`ax docs`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['repeat'])
    async def say(self, ctx):
      em = discord.Embed(title = "`say` / `repeat`", description = "Make the bot say something!", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "ManageGuild Permission", inline=False)
      em.add_field(name = "Usage", value = "`ax say Hi, I'm super cool!`\n`ax repeat \"Project Ax is so cool..\"`", inline=False)

      await ctx.send(embed = em)

    @help.command()
    async def stats(self, ctx):
      em = discord.Embed(title = "`stats`", description = "Displays Project Ax's stats.", color = 0xadcca6)
      em.add_field(name = "Usage", value = "`ax stats`", inline=False)

      await ctx.send(embed = em)
    
    @help.command()
    async def die(self, ctx):
      em = discord.Embed(title = "`die`", description = "Kills and restarts the bot. Add a \"pull\" parameter to make it update by pulling from the [GitHub](https://github.com/Dok4440/ProjectAx).", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = "`ax die`\n`ax die pull`", inline=False)

      await ctx.send(embed = em)

    @help.command(aliases=['delp', 'deletep'])
    async def delprofile(self, ctx):
      em = discord.Embed(title = "`delprofile` / `delp`", description = "Deletes a Project Ax profile. This action is irreversable.", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = "`ax delprofile 387984284734062592`", inline=False)

      await ctx.send(embed = em)
  
    @help.command(aliases=['editp', 'eprofile'])
    async def editprofile(self, ctx):
      em = discord.Embed(title = "`editprofile` / `editp`", description = "Edits a Project Ax profile. List of things you can change; `age`, `world`, `district`, `first_name`, `last_name`, `friend_id`, `gender`, `height`, `looks`, `xp`.", color = 0xadcca6)
      em.add_field(name = "Permissions", value = "Bot Owner", inline=False)
      em.add_field(name = "Usage", value = "`ax editprofile @Dok first_name \"Chad\"`\n`ax editp @JuicBblue age 69`", inline=False)

      await ctx.send(embed = em)

def setup(client):
    client.add_cog(Help(client))