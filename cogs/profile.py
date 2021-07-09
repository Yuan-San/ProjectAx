import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import asyncio
from tools import _db, _json, tools, embeds, _c, wembeds
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

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
        try:
            ## CHECK IF THE USER ALREADY HAS A PROFILE
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
                ## --------------------------------------


            em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to create your profile? **You can only do this once, and changing your profile is impossible.**")
            msg = await ctx.send(embed=em) # "msg" is the message that will be edited throughout the setup.

            ## DEFINE ALL BUTTONS
            buttons_1 = [
            Button(style=1, label="Yes"),
            Button(style=4, label="No")
            ],
            buttons_2 = [
                Button(style=1, emoji='◀️', custom_id="back"),
                Button(style=1, emoji='▶️', custom_id="next"),
                Button(style=3, label="Choose this weapon!"),
                Button(style=4, label=_c.deny()),
            ],

            await msg.edit(components=list(buttons_1))

            def checkforR(res):
                return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

            res = await self.client.wait_for("button_click", check=checkforR, timeout=15)
            await res.respond(type=6)


            if res.component.label.startswith("N"):
                await _c.cancel(msg)

            elif res.component.label.startswith("Y"):
                await _c.clear(msg)

                weapon=['longsword', 'katana', 'dagger', 'greatsword', 'sledgehammer', 'mace']
                page = 0
                main_weapon = ""
                await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))

                while True:

                    res = await self.client.wait_for("button_click", check=checkforR, timeout=15)
                    await res.respond(type=6)

                    if res.component.label == "Choose this weapon!":
                        main_weapon = weapon[page]
                        break


                    elif res.component.custom_id == "back":
                        if page == 0: page = (len(weapon)-1)
                        else: page -= 1
                        await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))


                    elif res.component.custom_id == "next":
                        if page == (len(weapon)-1): page = 0
                        else: page += 1
                        await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))


                    elif res.component.label == _c.deny():
                        break

                if main_weapon == "":
                    await _c.cancel(msg)
                    return



                await msg.edit(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{main_weapon}** as your main weapon?"))
                await msg.edit(components=list(buttons_1))


                res = await self.client.wait_for('button_click', timeout=15, check=checkforR)
                await res.respond(type=6)


                if res.component.label.startswith("N"):
                    await _c.cancel(msg)
                    return


                # secondary weapon
                await _c.clear(msg)
                weapon=['bow', 'longbow']
                page = 0
                secondary_weapon = ""
                await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))

                while True:

                    res = await self.client.wait_for("button_click", check=checkforR, timeout=15)
                    await res.respond(type=6)

                    if res.component.label == "Choose this weapon!":
                        secondary_weapon = weapon[page]
                        break


                    elif res.component.custom_id == "back":
                        if page == 0: page = (len(weapon)-1)
                        else: page -= 1
                        await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))


                    elif res.component.custom_id == "next":
                        if page == (len(weapon)-1): page = 0
                        else: page += 1
                        await msg.edit(embed=wembeds.w_page(weapon[page], ctx.author.avatar_url, self.client), components=list(buttons_2))


                    elif res.component.label == _c.deny():
                        break

                if secondary_weapon == "":
                    await _c.cancel(msg)
                    return


                await msg.edit(embed=discord.Embed(color=0xadcca6, description=f"**{ctx.author.name}#{ctx.author.discriminator}** Are you sure you want to pick **{secondary_weapon}** as your secondary weapon?"))
                await msg.edit(components=list(buttons_1))

                res = await self.client.wait_for('button_click', timeout=15, check=checkforR)
                await res.respond(type=6)


                if res.component.label.startswith("N"):
                    await _c.cancel(msg)
                    return

                await _c.clear(msg)


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
                await msg.edit(embed=em)

                collection.update_one({"_id": ctx.message.author.id}, {"$set":{"gender": gender, "looks": looks, "first_name": first_name, "last_name": last_name, "height": height, "world": "Heimur", "district": "Svart", "friend_id": user_name, "age": age, "xp": 0}}, upsert=True)

                print()
                print("----")
                print(f"Created profile for user {user_name} - {ctx.message.author.id}")
                print(f"Created inventory for profile. ({first_name} {last_name})")
                print("----")

        except asyncio.TimeoutError:
            await _c.timeout_button(msg)
            return

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

      main_weapon = _db.get_weapons(target)[0]
      secondary_weapon = _db.get_weapons(target)[1]

      """ badges """
      badges_string = ""

      try:
          badges = _db.get_badges(target)
          badges = _db.split_badges(badges)

          for i in range(0, len(badges)):
              badges_string += f"{self.client.get_emoji(_json.get_emote_id(badges[i]))} "
      except:
          pass

      # try:
      #     em.set_thumbnail(url=_json.get_art()[badges[0]])
      # except:
      #     em.set_thumbnail(url= looks)


      """ IMAGE """
      profile_image = Image.open("tools/art/scroll.png")
      profile_image_e = ImageDraw.Draw(profile_image)

      u_font = "tools/art/fonts/Charm/Charm-Bold.ttf"
      title_font = ImageFont.truetype(u_font, 40)
      l_title_font = ImageFont.truetype(u_font, 25)
      l_font = ImageFont.truetype(u_font, 15)

      RGB = [37, 39, 43]

      # name + last name
      profile_image_e.text((70,35), f"{first_name} {last_name}", (RGB[0], RGB[1], RGB[2]), font=title_font)

      # info card
      profile_image_e.text((70,85), f"Info", (RGB[0], RGB[1], RGB[2]), font=l_title_font)
      profile_image_e.text((70,115), f"Gender: {gender}\nHeight: {height}\nAge: {age}\nFriend ID: {friend_id}", (RGB[0], RGB[1], RGB[2]), font=l_font)

      # region
      profile_image_e.text((70,205), f"Region", (RGB[0], RGB[1], RGB[2]), font=l_title_font)
      profile_image_e.text((70,235), f"World: {world}\nDistrict: {district}", (RGB[0], RGB[1], RGB[2]), font=l_font)

      # level & weapons info
      profile_image_e.text((70,275), f"Level", (RGB[0], RGB[1], RGB[2]), font=l_title_font)
      profile_image_e.text((70,305), f"Player Level: {xp}\nPrimary Weapon: {main_weapon}\nSecondary Weapon: {secondary_weapon}", (RGB[0], RGB[1], RGB[2]), font=l_font)

      if target in  _json.get_config()["owners"]:
        """ Add Bot Admin Badge """
        badge_admin = Image.open('tools/art/badge_admin.png')
        badge_admin = badge_admin.resize((40,40))
        profile_image.paste(badge_admin, (260,45), badge_admin.convert('RGBA'))

      image = f"tools/art/result_profile_{target}.png"
      profile_image.save(image)
      await ctx.send(file=discord.File(image))

    @profile.error
    async def profile_error(self, ctx, error):
      if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** Couldn't find a Project Ax profile linked to that account.")

        await ctx.send(embed=em)

def setup(client):
    client.add_cog(profile(client))
