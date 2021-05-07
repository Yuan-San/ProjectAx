import discord
import time, datetime
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv

start_time=time.time()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('admin.py -> on_ready()')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, message):
      collection = db["Prefix"]
      if message == "default" or message == "ax": message = "ax "
      message = message.replace('"', '')

      b = "ax "
      prefix = collection.find({"server_id": ctx.message.guild.id})
      for a in prefix:
        b = a["prefix"]

      collection.update_one({"server_id": ctx.message.guild.id}, {"$set":{"prefix": message}}, upsert=True)

      em = discord.Embed(color=0xadcca6)
      em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Changed prefix on this server from `{b}` to `{message}`"
      await ctx.send(embed=em)

    @prefix.error
    async def prefix_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == "message":
          collection = db["Prefix"]

          b = "ax "
          prefix = collection.find({"server_id": ctx.message.guild.id})
          for a in prefix:
            b = a["prefix"]

          em = discord.Embed(color=0xadcca6)
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Prefix on this server is `{b}`"
          await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx, *, message=None):
      em = discord.Embed(color = 0xadcca6)
      # uptime=str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
      # em.add_field(name="uptime", value=uptime)

      if message == "pull":
        if (os.system("sudo sh rAIOmp.sh") / 256) > 1:
          var = os.system("sudo sh rAIOmp.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOmp.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = "Updating Project Ax..."
          await ctx.send(embed = em)
      else:
        if (os.system("sudo sh rAIOm.sh") / 256) > 1:
          var = os.system("sudo sh rAIOm.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOm.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = "Shutting Down.."
          await ctx.send(embed = em)

    @die.error
    async def die_error(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        await ctx.send("Error: you're not bot owner.")

def setup(client):
    client.add_cog(Admin(client))