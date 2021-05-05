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

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('Miscellaneous module is ready.')

    # ping
    @commands.command()
    async def ping(self, ctx):
      await ctx.send(f"self.client.latency; `{round(self.client.latency * 1000)}ms`")

    # invite
    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
      em = discord.Embed(description = "As the bot is still in BETA, you can't invite it to your server yet.", color = 0xadcca6)

      await ctx.send(embed = em)

    # rando command idfk
    @commands.command(aliases=['docs'])
    async def readme(self, ctx):
        em = discord.Embed(title = "Documentation", description = "soon.", color = 0xadcca6)

        await ctx.send(embed = em)

     # open source
    @commands.command(aliases=['code', 'source'])
    async def opensource(self, ctx):
      await ctx.send("source code here soon idk")
    
    # avatar
    @commands.command(aliases=['av', 'pfp', 'profilepic', 'profilepicture'])
    @commands.guild_only() # only able to do this command in a server (not in DM)
    async def avatar(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        # size = size or 1024 # gotta figure this out later
        size = 1024
        await ctx.send(f"{user.name}'s avatar・꒷꒦\n{user.avatar_url_as(size=size)}")
		
    # say
    @commands.command(aliases=['repeat', 'speak'])
    async def say(self, ctx, *, msg="please provide text for me to say!"):
        await ctx.send(msg)
        await ctx.message.delete()
		
    # bot stats
    @commands.command()
    async def stats(self, ctx):
        em = discord.Embed(color = 0xadcca6)
        
        v=str(os.getenv('VERSION'))
        
        em.set_author(name=f"Project Ax {v}", icon_url = "https://images-ext-2.discordapp.net/external/JpvcRi_vZuUxHv57rebrT8Bm1qGKmQmgSGq3PqEUO_o/https/media.discordapp.net/attachments/803967265338032140/805094438807666768/pixil-frame-0_6.png")
        em.add_field(name="Team", value="Axie#3706\nDok#4440\nJuicyBblue#5335")
        
        uptime=str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
        em.add_field(name="uptime", value=f"{uptime}", inline=False)

        em.add_field(name="server count", value = f"{str(len(self.client.guilds))}")

        await ctx.send(embed = em)

    # greet msg
    @commands.Cog.listener()
    async def on_member_join(self, member):
      collection = db["Greetings"]
      results = collection.find({"server_id": member.guild.id})

      for result in results:
        msg = result["message"]
        guild = result["server_id"]
        ch = result["channel_id"]

      server = self.client.get_guild(guild)
      channel = server.get_channel(ch)
      await channel.send(msg)
        
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def greetmsg(self, ctx, *, message):
      collection = db["Greetings"]

      post = {"server_id": ctx.message.guild.id, "message": message, "channel_id": ctx.message.channel.id}

      collection.delete_many({"server_id": ctx.message.guild.id})
      collection.insert_one(post)

      await ctx.send("Welcome message has been set in this channel.")

    

# this is the end of the code, type all mod commands above this
def setup(client):
    client.add_cog(Miscellaneous(client))