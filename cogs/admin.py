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
      print ('Admin module is gae.')

    # enable module
    @commands.command()
    @commands.is_owner()
    async def enableModule(self, ctx, extension):
      commands.load_extension(f'cogs.{extension}')
      await ctx.send('The module was enabled!')

    # disable module
    @commands.command()
    @commands.is_owner()
    async def disableModule(self, ctx, extension):
      commands.unload_extension(f'cogs.{extension}')
      await ctx.send('The module was disabled!')

    # set prefix
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, message):
      collection = db["Prefix"]

      message = message.replace('"', '')

      if message != "default" and message != "ax":
        post = {"server_id": ctx.message.guild.id, "prefix": message}
      else:
        post = {"server_id": ctx.message.guild.id, "prefix": "ax "}

      collection.delete_many({"server_id": ctx.message.guild.id})
      collection.insert_one(post)

      await ctx.send("Prefix has been set! **(prefix-case-sensitivy has been disabled globally.)**")

    # @prefix.error
    # async def prefix_error(self, ctx, error):
      # if isinstance(error, commands.MissingRequiredArgument):
      #   if error.param.name == 'message':

      #     collection = db["Prefix"]

      #     a = collection.find({"server_id": ctx.message.guild.id})
      #     for key, val in a.prefix():
      #       b = val

      #     await ctx.send(f"My current prefix is `{b}`")

    # die
    @commands.command()
    @commands.is_owner()
    async def die(self, ctx):
      em = discord.Embed(title="Shutting Down..", color = 0xadcca6)
      
      uptime=str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
      
      em.add_field(name="uptime", value=uptime)
      await ctx.send(embed = em)
      os.system("sudo sh rAIOm.sh")
		
    @die.error
    async def die_error(self, ctx, error):
      await ctx.send("Error;!is_owner()")


# this is the end of the code, type all mod commands above this
def setup(client):
    client.add_cog(Admin(client))