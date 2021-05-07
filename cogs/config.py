import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv

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

def setup(client):
    client.add_cog(Admin(client))