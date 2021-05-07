import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
import json
from StuffsWeNeed import defaultstuff
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('profile.py -> on_ready()')

    @commands.command(aliases=['p'])
    async def profile(self, ctx):

      collection = db["Profile"]

      em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to create your profile? **You can only do this once, and changing your profile is impossible.**")
      em.set_footer(text="Please type \"yes\" to confirm. Type anything else to cancel this command.")

      await ctx.send(embed=em)

      try: 
        msg = await self.client.wait_for('message', timeout=30, check=lambda message:message.author == ctx.author and message.channel.id == ctx.channel.id)

        if msg.content.lower() == "yes":

          MaleLooks = defaultstuff.profile()["MaleLooks"]
          FemaleLooks = defaultstuff.profile()["FemaleLooks"]
          CharacterLastName = defaultstuff.profile()["CharacterLastName"]
          CharacterFirstNameMale = defaultstuff.profile()["CharacterFirstNameMale"]
          CharacterFirstNameFemale = defaultstuff.profile()["CharacterFirstNameFemale"]

          maleFemaleRatio = [1, 2]
          choice = random.choice(maleFemaleRatio)

          if choice == 1:
            looks = random.choice(MaleLooks)
            first_name = random.choice(CharacterFirstNameMale)
            last_name = random.choice(CharacterLastName)
          else:
            looks = random.choice(FemaleLooks)
            first_name = random.choice(CharacterFirstNameFemale)
            last_name = random.choice(CharacterLastName)

          em=discord.Embed(color = 0xadcca6, title=f"{first_name} {last_name}")
          em.set_author(name="Project Ax Profile", icon_url="https://media.discordapp.net/attachments/804705780557021214/804827293087563776/Throwing_Knives.png")
          em.set_thumbnail(url=looks)
          await ctx.send(embed=em)



        else:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled."))
          return

      except asyncio.TimeoutError:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))

def setup(client):
    client.add_cog(profile(client))