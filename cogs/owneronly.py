import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from tools import _db, _json, tools, embeds
from dotenv import load_dotenv
from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class owneronly(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print ('owneronly.py -> on_ready()')

      if os.getenv('ISMAIN') == "True":
        msg = db["DieMessage"].find({"_id": 1})
        for a in msg:
          channel = a["channel_id"]
          user_name = a["user_name"]
          user_discrim = a["user_discrim"]
          time_on_die = a["time_on_die"]

        time_now = datetime.now()
        restart_time = (time_now - time_on_die).total_seconds()

        em = discord.Embed(color=0xadcca6, description = (f"**{user_name}#{user_discrim}** It took me {round(restart_time, 2)} seconds to restart."))

        ch = self.client.get_channel(channel)
        await ch.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx, *, message=None):
      em = discord.Embed(color = 0xadcca6)
      time_on_die = datetime.now()

      collection = db["DieMessage"]
      collection.update_one({"_id": 1}, {"$set":{"channel_id": ctx.message.channel.id, "user_name": ctx.author.name, "user_discrim": ctx.author.discriminator, "time_on_die": time_on_die}}, upsert=True)

      if message == "pull":
        if (os.system("sudo sh rAIOmp.sh") / 256) > 1:
          var = os.system("sudo sh rAIOmp.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOmp.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Updating Project Ax.."
          await ctx.send(embed = em)
      else:
        if (os.system("sudo sh rAIOm.sh") / 256) > 1:
          var = os.system("sudo sh rAIOm.sh") # this will run os.system() AGAIN.
          await ctx.send(f"Couldn't run `rAIOm.sh`\n\n*os.system() output for BETA testing purposes; {var}*")
        else:
          em.description = f"**{ctx.author.name}#{ctx.author.discriminator}** Shutting Down.."
          await ctx.send(embed = em)

    @die.error
    async def die_error(self, ctx, error):
      if isinstance(error, commands.NotOwner):
        await ctx.send("Error: you're not bot owner.")

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

def setup(client):
    client.add_cog(owneronly(client))
