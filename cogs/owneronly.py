import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class owneronly(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('owneronly.py -> on_ready()')

      if os.getenv('ISMAIN') == "True":
        msg = db["DieMessage"].find({"_id": 1})
        for a in msg:
          channel = a["channel_id"]
          user_name = a["user_name"]
          user_discrim = a["user_discrim"]
          time_on_die = a["time_on_die"]

        time_now = datetime.now()
        restart_time = (time_now - time_on_die).total_seconds()

        em = discord.Embed(color=0xadcca6, description = (f"**{user_name}#{user_discrim}** It took me {round(restart_time, 2)} seconds to restart."))

        ch = self.client.get_channel(channel)
        await ch.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx, *, message=None):
      em = discord.Embed(color = 0xadcca6)
      time_on_die = datetime.now()

      collection = db["DieMessage"]
      collection.update_one({"_id": 1}, {"$set":{"channel_id": ctx.message.channel.id, "user_name": ctx.author.name, "user_discrim": ctx.author.discriminator, "time_on_die": time_on_die}}, upsert=True)

      if message == "pull":
        if (os.system("sudo sh rAIOmp.sh") / 256) > 1:
          var = os.system("sudo sh rAIOmp.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOmp.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Updating Project Ax.."
          await ctx.send(embed = em)
      else:
        if (os.system("sudo sh rAIOm.sh") / 256) > 1:
          var = os.system("sudo sh rAIOm.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOm.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Shutting Down.."
          await ctx.send(embed = em)

    @die.error
    async def die_error(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        await ctx.send("Error: you're not bot owner.")

def setup(client):
    client.add_cog(owneronly(client))
