import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
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

      check = collection.count_documents({"_id": ctx.message.author.id})
      if check != 0:
        
        profile = db["Profile"].find({"_id": ctx.message.author.id})
        for b in profile:
          first_name=b["first_name"]
          last_name=b["last_name"]
          xp = b["xp"]

        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** You seem to already have a profile **({first_name} {last_name} - xp: `{xp}`)**.\nPlease join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")

        await ctx.send(embed=em)
        return

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
          age = ['18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
          choice = random.choice(maleFemaleRatio)

          if choice == 1:
            gender = "Male"
            looks = random.choice(MaleLooks)
            first_name = random.choice(CharacterFirstNameMale)
            last_name = random.choice(CharacterLastName)
            height = random.choice(male_height)
            age = random.choice(age)
          else:
            gender = "Female"
            looks = random.choice(FemaleLooks)
            first_name = random.choice(CharacterFirstNameFemale)
            last_name = random.choice(CharacterLastName)
            height = random.choice(female_height)
            age = random.choice(age)

          user_name = f"{ctx.author.name}#{ctx.author.discriminator}"

          em=discord.Embed(title=f"{first_name} {last_name}", color = 0xadcca6)
          em.add_field(name="Info Card", value=f"Gender: {gender}\nHeight: {height}\nAge: {age}\n Friend ID: {user_name}", inline=False)
          em.add_field(name="Region", value="World: Heimur\nDistrict: Svart", inline=False)
          em.add_field(name="Level", value="Player Level: `0`\nPrimary Weapon: `N/A`\nSecondary Weapon: `N/A`", inline=False)
          em.set_thumbnail(url=looks)
          await ctx.send(embed=em)

          collection.update_one({"_id": ctx.message.author.id}, {"$set":{"gender": "Male", "looks": looks, "first_name": first_name, "last_name": last_name, "height": height, "world": "Heimur", "district": "Svart", "friend_id": user_name, "age": age, "xp": 0}}, upsert=True)

        else:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled."))
          return

      except asyncio.TimeoutError:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))
    

    @commands.command(aliases=['p'])
    async def profile(self, ctx):
      check = db["Profile"].count_documents({"_id": ctx.message.author.id})
      if check == 0:
        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")

        await ctx.send(embed=em)
        return
      
      profile = db["Profile"].find({"_id": ctx.message.author.id})
      for b in profile:
        age = b["age"]
        district = b["district"]
        first_name=b["first_name"]
        friend_id=b["friend_id"]
        gender=b["gender"]
        height=b["height"]
        last_name=b["last_name"]
        looks=b["looks"]
        world=b["world"]
        xp = b["xp"]
      
      em=discord.Embed(title=f"{first_name} {last_name}", color = 0xadcca6)
      em.add_field(name="Info Card", value=f"Gender: {gender}\nHeight: {height}\nAge: {age}\n Friend ID: {friend_id}", inline=False)
      em.add_field(name="Region", value=f"World: {world}\nDistrict: {district}", inline=False)
      em.add_field(name="Level", value=f"Player Level: `{xp}`\nPrimary Weapon: `N/A`\nSecondary Weapon: `N/A`", inline=False)
      em.set_thumbnail(url=looks)
      await ctx.send(embed=em)

    

def setup(client):
    client.add_cog(profile(client))