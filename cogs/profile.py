import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from StuffsWeNeed import _db, defaultstuff
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
      em.set_footer(text="Please react to this message to confirm.")

      first_embed = await ctx.send(embed=em)

      await first_embed.add_reaction(emoji='✅')
      await first_embed.add_reaction(emoji='🛑')

      main_weapon = "nah"
      secondary_weapon = "nah"

      # weapon variables
      longsword = self.client.get_emoji(841591365649170463)
      katana = self.client.get_emoji(841591388055273472)
      dagger = self.client.get_emoji(841591344308158516)
      greatsword = self.client.get_emoji(841591317368799242)
      sledgehammer = self.client.get_emoji(841591294115315753)
      mace =  self.client.get_emoji(841591275567579156)
      bow = self.client.get_emoji(841631789675053077)
      longbow = self.client.get_emoji(841592788084326400)

      def checkforR(reaction, msg):
        return msg == ctx.message.author and reaction.emoji in ['✅', '🛑', longsword, katana, dagger, greatsword, sledgehammer, mace, bow, longbow]

      try: 

        reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

        if reaction.emoji == '✅':

          await first_embed.clear_reactions()

          # main weapon
          em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Let's choose some weapons! First off, what do you want your **main weapon** to be? Note that only your first weapon will be free!")
          second_embed = await first_embed.edit(embed=em)
          
          await first_embed.add_reaction(emoji=longsword)
          await first_embed.add_reaction(emoji=katana)
          await first_embed.add_reaction(emoji=dagger)
          await first_embed.add_reaction(emoji=greatsword)
          await first_embed.add_reaction(emoji=sledgehammer)
          await first_embed.add_reaction(emoji=mace)
          await first_embed.add_reaction(emoji='🛑')

          reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

          if reaction.emoji == longsword: main_weapon = "longsword"
          elif reaction.emoji == katana: main_weapon = "katana"
          elif reaction.emoji == dagger: main_weapon = "dagger"
          elif reaction.emoji == greatsword: main_weapon = "greatsword"
          elif reaction.emoji == sledgehammer: main_weapon = "sledgehammer"
          elif reaction.emoji == mace: main_weapon = "mace"
          else: 
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled. {reaction.emoji}")) 
            return

          await first_embed.clear_reactions()

          # secondary weapon
          em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** And what will your **secondary weapon** be? Note that only your first weapon will be free!")
          third_embed = await first_embed.edit(embed=em)

          await first_embed.add_reaction(emoji=bow)
          await first_embed.add_reaction(emoji=longbow)
          await first_embed.add_reaction(emoji='🛑')

          reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

          if reaction.emoji == bow: secondary_weapon = "bow"
          elif reaction.emoji == longbow: secondary_weapon = "longbow"
          elif reaction.emoji == '🛑':
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return

          await first_embed.clear_reactions()

          # add both weapons to the database (inventory)
          if main_weapon != "nah":
            if secondary_weapon != "nah":
              try: 
                _db.create_inventory(ctx.message.author.id, main_weapon, secondary_weapon)
              except:
                await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong."))
                return
            else:
              await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong."))
              return
          else:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong."))
            return


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
          em.add_field(name="Level", value=f"Player Level: `0`\nPrimary Weapon: {main_weapon}\nSecondary Weapon: {secondary_weapon}", inline=False)
          em.set_thumbnail(url=looks)
          fourth_embed = await first_embed.edit(embed=em)

          collection.update_one({"_id": ctx.message.author.id}, {"$set":{"gender": gender, "looks": looks, "first_name": first_name, "last_name": last_name, "height": height, "world": "Heimur", "district": "Svart", "friend_id": user_name, "age": age, "xp": 0}}, upsert=True)

          print()
          print("----")
          print(f"Created profile for user {user_name} - {ctx.message.author.id}")
          print(f"Created inventory for profile. ({first_name} {last_name})")
          print("----")

        else:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled."))
          return

      except asyncio.TimeoutError:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))
    

    @commands.command(aliases=['p'])
    async def profile(self, ctx, *, target: discord.Member=None):
      if target is None:
        target = ctx.message.author.id
      else:
        try:
          target = target.id
        except:
          pass


      check = db["Profile"].count_documents({"_id": target})
      if check == 0:
        if target is ctx.message.author.id:
          em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")

        await ctx.send(embed=em)
        return
      
      profile = db["Profile"].find({"_id": target})
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
      
      main_weapon = _db.get_weapons(ctx.message.author.id)[0]
      secondary_weapon = _db.get_weapons(ctx.message.author.id)[1]
      
      em=discord.Embed(title=f"{first_name} {last_name}", color = 0xadcca6)
      em.add_field(name="Info Card", value=f"Gender: {gender}\nHeight: {height}\nAge: {age}\n Friend ID: {friend_id}", inline=False)
      em.add_field(name="Region", value=f"World: {world}\nDistrict: {district}", inline=False)
      em.add_field(name="Level", value=f"Player Level: `{xp}`\nPrimary Weapon: `{main_weapon}`\nSecondary Weapon: `{secondary_weapon}`", inline=False)
      em.set_thumbnail(url=looks)
      await ctx.send(embed=em)

    @profile.error
    async def profile_error(self, ctx, error):
      if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Couldn't find a Project Ax profile linked to that account.")

        await ctx.send(embed=em)
    
    @commands.command(aliases=['delp', 'deletep'])
    @commands.is_owner()
    async def delprofile(self, ctx, *, id: int):

      check = db["Profile"].count_documents({"_id": id})
      if check != 0:
        
        profile = db["Profile"].find({"_id": id})
        for b in profile:
          first_name=b["first_name"]
          last_name=b["last_name"]
          xp = b["xp"]

        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to delete this profile **({first_name} {last_name} - xp: `{xp}`**)? This action is irreversable.")
        em.set_footer(text="Please type \"yes\" to confirm. Type anything else to cancel this command.")

        await ctx.send(embed=em)

        try: 
          msg = await self.client.wait_for('message', timeout=30, check=lambda message:message.author == ctx.author and message.channel.id == ctx.channel.id)

          if msg.content.lower() == "yes":
            try:
              db["Profile"].delete_one({"_id": id})
              em=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Succesfully deleted the profile.")

              _db.delete_inventory(id)

              user_name=f"{ctx.author.name}#{ctx.author.discriminator}"

              print()
              print("----")
              print(f"Deleted profile from user {user_name} - {ctx.message.author.id}")
              print(f"Deleted inventory from profile ({first_name} {last_name})")
              print("----")

              await ctx.send(embed=em)
            except:
              em=discord.Embed(color = 0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong, please try again.")

              await ctx.send(embed=em)

          else:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled."))
            return

        except asyncio.TimeoutError:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** You failed to reply in time."))

      else:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Couldn't find any profile with that ID."))
    
    @commands.command(aliases=['eprofile', 'editp'])
    @commands.is_owner()
    async def editprofile(self, ctx, target: discord.Member, query: str, edit: str):
      try:
        target = target.id
      except:
        pass

      profile = db["Profile"].find({"_id": target})
      for b in profile:
        to_edit=b[query]

      try:
        db["Profile"].update_one({"_id": target}, {"$set":{query: edit}}, upsert=True)
      except:
        em=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong, please try again.")
        await ctx.send(embed=em)
      
      em=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Updated the value \"{query}\" from `{to_edit}` to `{edit}` in document with \"_id\": `{target}`.")
      await ctx.send(embed=em)
    
    @editprofile.error
    async def editprofile_error(self, ctx, error):
        em=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong, please try again.")
        await ctx.send(embed=em)      

def setup(client):
    client.add_cog(profile(client))