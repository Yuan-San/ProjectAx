import discord
import time, datetime
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from StuffsWeNeed import defaultstuff

start_time=time.time()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('misc.py -> on_ready()')

    # ping
    @commands.command()
    async def ping(self, ctx):
      em = discord.Embed(color=0xadcca6, description = (f"**{ctx.author.name}#{ctx.author.discriminator}** Latency: `{round(self.client.latency * 1000)}ms`"))

      await ctx.send(embed=em)

    # invite
    @commands.command()
    async def invite(self, ctx):
      em = discord.Embed(description = "As the bot is still in BETA, you can't invite it to your server yet.", color = 0xadcca6)

      await ctx.send(embed = em)

    # rando command idfk
    @commands.command(aliases=['docs'])
    async def readme(self, ctx):
        em = discord.Embed(title = "Documentation", description = "soon.", color = 0xadcca6)

        await ctx.send(embed = em)
		
    # say
    @commands.command(aliases=['repeat'])
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx, *, msg="Please provide text for me to say!"):
        await ctx.send(msg)
        await ctx.message.delete()
		
    # bot stats
    @commands.command()
    async def stats(self, ctx):
        em = discord.Embed(color = 0xadcca6)
        
        v=defaultstuff.get_version()
        
        em.set_author(name=f"Project Ax {v}", icon_url = "https://images-ext-2.discordapp.net/external/JpvcRi_vZuUxHv57rebrT8Bm1qGKmQmgSGq3PqEUO_o/https/media.discordapp.net/attachments/803967265338032140/805094438807666768/pixil-frame-0_6.png")
        em.add_field(name="Team", value="Axie#3706\nDok#4440\nJuicyBblue#5335")
        
        uptime=str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
        em.add_field(name="uptime", value=f"{uptime}", inline=False)

        em.add_field(name="server count", value = f"{str(len(self.client.guilds))}")

        await ctx.send(embed = em)    
    
    @commands.command(aliases=['v'])
    async def version(self, ctx):
      em = discord.Embed(color = 0xadcca6, description=f"`{defaultstuff.get_version()}`", title="Project Ax Version")
      await ctx.send(embed=em)

# this is the end of the code, type all mod commands above this
def setup(client):
    client.add_cog(Miscellaneous(client))