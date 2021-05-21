import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from tools import _db, _json, tools, embeds
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

      try:
        await first_embed.add_reaction(emoji='✅')
        await first_embed.add_reaction(emoji='🛑')
      except:
        await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
        return

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
          em = discord.Embed(color=0xadcca6)
          em.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} Let's choose some weapons! First off, what do you want your main weapon to be? Note that only your first weapon will be free!")
          em.add_field(name=f"{longsword} Longsword {longsword}", value=_db.get_weapon_stats_list("longsword"))
          em.add_field(name=f"{katana} Katana {katana}", value=_db.get_weapon_stats_list("katana"))
          em.add_field(name=f"{dagger} Dagger {dagger}", value=_db.get_weapon_stats_list("dagger"))
          em.add_field(name=f"{greatsword} Greatsword {greatsword}", value=_db.get_weapon_stats_list("greatsword"))
          em.add_field(name=f"{sledgehammer} Slegdehammer {sledgehammer}", value=_db.get_weapon_stats_list("sledgehammer"))
          em.add_field(name=f"{mace} Mace {mace}", value=_db.get_weapon_stats_list("mace"))
          em.set_footer(text="React to the corresponding emote to select that weapon.")
          second_embed = await first_embed.edit(embed=em)
          
          try: 
            await first_embed.add_reaction(emoji=longsword)
            await first_embed.add_reaction(emoji=katana)
            await first_embed.add_reaction(emoji=dagger)
            await first_embed.add_reaction(emoji=greatsword)
            await first_embed.add_reaction(emoji=sledgehammer)
            await first_embed.add_reaction(emoji=mace)
            await first_embed.add_reaction(emoji='🛑')
          except:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
            return

          reaction, msg = await self.client.wait_for('reaction_add', timeout=120, check=checkforR)

          if reaction.emoji == longsword: main_weapon = "longsword"
          elif reaction.emoji == katana: main_weapon = "katana"
          elif reaction.emoji == dagger: main_weapon = "dagger"
          elif reaction.emoji == greatsword: main_weapon = "greatsword"
          elif reaction.emoji == sledgehammer: main_weapon = "sledgehammer"
          elif reaction.emoji == mace: main_weapon = "mace"
          else: 
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return

          await first_embed.clear_reactions()

          # confirmation
          second_confirm_embed = await first_embed.edit(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{main_weapon}** as your main weapon?"))
          
          try:
            await first_embed.add_reaction(emoji='✅')
            await first_embed.add_reaction(emoji='🛑')
          except:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
            return

          reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

          if reaction.emoji == '🛑':
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return

          await first_embed.clear_reactions()

          # secondary weapon
          em = discord.Embed(color=0xadcca6)
          em.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} And what will your secondary weapon be? Note that only your first weapon will be free!")
          em.add_field(name=f"{bow} Bow {bow}", value=_db.get_weapon_stats_list("bow"))
          em.add_field(name=f"{longbow} Longbow {longbow}", value=_db.get_weapon_stats_list("longbow"))
          em.set_footer(text="React to the corresponding emote to select that weapon.")

          await first_embed.edit(embed=em)

          try:
            await first_embed.add_reaction(emoji=bow)
            await first_embed.add_reaction(emoji=longbow)
            await first_embed.add_reaction(emoji='🛑')
          except:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
            return

          reaction, msg = await self.client.wait_for('reaction_add', timeout=120, check=checkforR)

          if reaction.emoji == bow: secondary_weapon = "bow"
          elif reaction.emoji == longbow: secondary_weapon = "longbow"
          elif reaction.emoji == '🛑':
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return

          await first_embed.clear_reactions()
        
          # confirmation
          await first_embed.edit(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{secondary_weapon}** as your secondary weapon?"))
          
          try:
            await first_embed.add_reaction(emoji='✅')
            await first_embed.add_reaction(emoji='🛑')
          except:
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
            return

          reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

          if reaction.emoji == '🛑':
            await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** The command was canceled.")) 
            return
          
          await first_embed.clear_reactions()



          # check if the weapons are actually registered
          if main_weapon == None or secondary_weapon == None:

            em=embeds.error_1(ctx.author.name, ctx.author.discriminator)
            em.set_footer("main_weapon == None or secondary_weapon == None")

            await ctx.send(embed=em)
            return
          
          # add both weapons to the database (inventory)
          try: 
            _db.create_inventory(ctx.message.author.id, main_weapon, secondary_weapon)
          except:
            await ctx.send(embed=embeds.error_1(ctx.author.name, ctx.author.discriminator))
            return



          MaleLooks = _json.get_profile()["MaleLooks"]
          FemaleLooks = _json.get_profile()["FemaleLooks"]
          CharacterLastName = _json.get_profile()["CharacterLastName"]
          CharacterFirstNameMale = _json.get_profile()["CharacterFirstNameMale"]
          CharacterFirstNameFemale = _json.get_profile()["CharacterFirstNameFemale"]

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
          em.add_field(name="Level", value=f"Player Level: `0`\nPrimary Weapon: `{main_weapon}`\nSecondary Weapon: `{secondary_weapon}`", inline=False)
          em.set_thumbnail(url=looks)
          await first_embed.edit(embed=em)

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
      
      # find who's profile to pull up.
      target = tools.get_target(target, ctx.message.author.id)


      check = db["Profile"].count_documents({"_id": target})
      if check == 0:
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

        def checkforR(reaction, msg):
          return msg == ctx.message.author and reaction.emoji in ['✅', '🛑']

        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to delete this profile **({first_name} {last_name} - xp: `{xp}`**)? This action is irreversable.")
        em.set_footer(text="Please react to this message to confirm.")

        message_embed = await ctx.send(embed=em)

        try:
          await message_embed.add_reaction(emoji='✅')
          await message_embed.add_reaction(emoji='🛑')
        except:
          await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Something went wrong. Make sure I have permissions to add reactions to messages!")) 
          return

        try: 
          reaction, msg = await self.client.wait_for('reaction_add', timeout=30, check=checkforR)

          if reaction.emoji == '✅':
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

              await message_embed.clear_reactions()
              await message_embed.edit(embed=em)
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
      
    @commands.command()
    @commands.is_owner()
    async def insert_weapon(self, ctx, weapon: str, damage: int, accuracy: int, defence: int, speed: int):
      collection = db["WeaponStats"]
      collection.insert_one({"_id": weapon, "damage": damage, "accuracy": accuracy, "defence": defence, "speed": speed})
      await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Added weapon ({weapon}) to the database.\nDamaga: {damage}\nAccuracy: {accuracy}\nDefence: {defence}\nSpeed: {speed}"))
    
    @commands.command()
    @commands.is_owner()
    async def update_weapon(self, ctx, weapon: str, damage: int, accuracy: int, defence: int, speed: int):
      collection = db["WeaponStats"]
      collection.update_one({"_id": weapon}, {"$set":{"damage": damage, "accuracy": accuracy, "defence": defence, "speed": speed}})
      await ctx.send(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Updated weapon ({weapon}) database.\nDamaga: {damage}\nAccuracy: {accuracy}\nDefence: {defence}\nSpeed: {speed}"))

def setup(client):
    client.add_cog(profile(client))