from discord.ext import commands
import discord
from tools import embeds
from pymongo import MongoClient
import random
import os
import dotenv
from tools import _json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

dotenv.load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class hunt(commands.cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print ('hunt.py -> on_ready()')

  @commands.command()
  async def hunt(self, ctx):
    check = db["Profile"].count_documents({"_id": ctx.message.author.id})
    if check == 0:
        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")
        await ctx.send(embed=em)
        return 
    
    profile = db["Profile"].find({"_id": ctx.message.author.id})
    for b in profile:
      district = b["district"]

    if district == "Svart":
     _items="Slime Ball"
     _cash=random.randint(15, 150)
     _xp=random.randint(30, 100)
     rolls=random.randint(1, 100)
     if (rolls < 5):
       _item=2
     elif (rolls < 20) and (rolls > 5):
       _item=1
     else:
       _item=0
    _mob = _json.get_mob()["Area 1"]

    await ctx.send(embed=embeds.hunt_embed(_cash, _xp, _item, _mob, _items))