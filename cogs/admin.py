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

      msg = db["DieMessage"].find({"_id": 1})
      for a in msg:
        ch = self.client.get_channel(a["channel_id"])
        await ch.send("I'm back!")

        # msg = self.client.fetch_message(a["message_id"])
        await a["message_id"].edit("wbt")

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

      collection = db["DieMessage"]

      if message == "pull":
        if (os.system("sudo sh rAIOmp.sh") / 256) > 1:
          var = os.system("sudo sh rAIOmp.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOmp.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Updating Project Ax.."
          msg = await ctx.send(embed = em)
          msg = await ctx.fetch_message(msg.id)
          collection.update_one({"_id": 1}, {"$set":{"channel_id": ctx.message.channel.id, "message_id": msg}}, upsert=True)
      else:
        if (os.system("sudo sh rAIOm.sh") / 256) > 1:
          var = os.system("sudo sh rAIOm.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOm.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Shutting Down.."
          msg = await ctx.send(embed = em)
          msg = await ctx.fetch_message(msg.id)
          collection.update_one({"_id": 1}, {"$set":{"channel_id": ctx.message.channel.id, "message_id": msg}}, upsert=True)

    @die.error
    async def die_error(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        await ctx.send("Error: you're not bot owner.")

def setup(client):
    client.add_cog(Admin(client))