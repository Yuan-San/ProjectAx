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

    @commands.command(aliases=['cprofile', 'createp', 'cp'])
    async def createprofile(self, ctx):

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
          female_height = ["4'7", "4'8", "4'9", "4'10", "4'11", "5'", "5'1", "5'2", "5'3", "5'4", "5'5", "5'6", "5'7", "5'8"]
          male_height = ["4'9", "4'10", "4'11", "5'", "5'11", "6'", "6'1", "5'4", "5'5", "5'6", "5'7", "5'8", "5'9", "5'10"]
          choice = random.choice(maleFemaleRatio)

          if choice == 1:
            gender = "Male"
            looks = random.choice(MaleLooks)
            first_name = random.choice(CharacterFirstNameMale)
            last_name = random.choice(CharacterLastName)
            height = random.choice(male_height)
          else:
            gender = "Female"
            looks = random.choice(FemaleLooks)
            first_name = random.choice(CharacterFirstNameFemale)
            last_name = random.choice(CharacterLastName)
            height = random.choice(female_height)


          em=discord.Embed(color = 0xadcca6)
          em.set_author(name=f"{first_name} {last_name}", icon_url="https://media.discordapp.net/attachments/804705780557021214/804827293087563776/Throwing_Knives.png")
          em.add_field(name="Info Card", value=f"Gender: {gender}\nHeight: {height}\n Friend ID: 1234", inline=False)
          em.add_field(name="Region", value="World: Heimur\nDistrict: Svart", inline=False)
          em.add_field(name="Level", value="Player Level: `0`\nPrimary Weapon: `N/A`\nSecondary Weapon: `N/A`", inline=False)
          # em.set_footer(text="To add a friend, wait u impatient fuck.")
          em.set_thumbnail(url=looks)
          await ctx.send(embed=em)



        else:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled."))
          return

      except asyncio.TimeoutError:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))

def setup(client):
    client.add_cog(profile(client))