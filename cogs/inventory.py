import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from tools import _db, embeds, tools, _json, combat

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

load_dotenv('.env')
dbclient = MongoClient(os.getenv('DBSTRING1'))
db = dbclient[os.getenv('DBSTRING2')]

class inventory(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
      print ('inventory -> on_ready()')


    @commands.group(invoke_without_command=True, aliases=['inv', 'info'])
    async def inventory(self, ctx, *, target: discord.Member=None):

        # find who's profile to pull up.
        target = tools.get_target(target, ctx.message.author.id)

        # check if the user's profile actually exists
        check = db["Inventory"].count_documents({"_id": target})
        if check == 0:
            em = discord.Embed(color=0xadcca6, description = f"**{ctx.author.name}#{ctx.author.discriminator}** I couldn't find any profile linked to your account. Do `ax createprofile` to create one. Please join the [Support Server](https://discord.gg/2TCQtNs8kN) if you believe this is a mistake.")
            await ctx.send(embed=em)
            return

        # inventory variables
        main_weapon = _db.get_weapons(target)[0]
        secondary_weapon = _db.get_weapons(target)[1]

        main_weapon_xp = _db.get_weapons(target)[2]
        secondary_weapon_xp = _db.get_weapons(target)[3]

        main_weapon_e = self.client.get_emoji(_json.get_emote_id(main_weapon))
        secondary_weapon_e = self.client.get_emoji(_json.get_emote_id(secondary_weapon))
        
        balance = _db.get_balance(target)
        p = _db.get_prefix(ctx.message.guild.id)

        healing_potion = _db.get_item(target, "healing_potion", ctx.message.guild.id,"m")
        healing_potion_emote = self.client.get_emoji(_json.get_emote_id("healing_potion"))

        # create inventory embed
        em = embeds.show_inv(balance, main_weapon_e, main_weapon, main_weapon_xp, secondary_weapon_e, secondary_weapon, secondary_weapon_xp, healing_potion, healing_potion_emote, p)

        await ctx.send(embed=em)
    
    # each item
    @inventory.command(aliases=['healing', 'healingpotion'])
    async def healing_potion(self, ctx, *, target: discord.Member=None):

        # find who's profile to pull up.
        target = tools.get_target(target, ctx.message.author.id)

        # variables
        item = "Healing Potion"
        desc = "Item used for healing your character"
        stats = "Heals `150` of your character's life points"
        amount = _db.get_item(target, "healing_potion", ctx.message.guild.id, "nm")
        thumbnail = "https://media.discordapp.net/attachments/804705780557021214/842031340521783316/pixil-frame-0_6.png"
        p = _db.get_prefix(ctx.message.guild.id)

        # create embed
        em = embeds.inventory_item(amount, desc, item, stats, p, thumbnail)

        await ctx.send(embed=em)
    
    # weapon info
    @inventory.command(aliases=['wpn'])
    async def weapon(self, ctx, *, weapon):

        # variables
        desc = "Project Ax - v1 Weapon (stage 1)"
        thumbnail = _json.get_art()[weapon.lower()]
        p = _db.get_prefix(ctx.message.guild.id)

        await ctx.send(embed=embeds.inventory_weapon(weapon.lower(), desc, thumbnail, p))

def setup(client):
    client.add_cog(inventory(client))