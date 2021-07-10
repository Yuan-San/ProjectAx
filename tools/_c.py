# discord-components
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
import asyncio
import discord

async def timeout_button(msg):
    await msg.edit(components=[
        Button(style=4, label="Timed Out!", disabled=True, custom_id="timed_out"),
        ],
    )

async def clear(msg):
    await msg.edit(components=[])

async def cancel(msg):
    await msg.edit(components=[
        Button(style=4, label="The command was canceled", disabled=True, custom_id="cmd_canceled"),
        ],
    )

def accept():
    return "Accept"
 
def deny():
    return "Run Away"
