import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 489797963481219087
TARGET_CHANNEL_ID = 1296497584709435412

last_status = None

@bot.event  
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    global last_status
    user = await bot.fetch_user(TARGET_USER_ID)
    for guild in bot.guilds:
        member = guild.get_member(TARGET_USER_ID)
        if member:
            last_status = member.status
            break

@bot.event
async def on_presence_update(before, after):
    global last_status
    
    if after.id != TARGET_USER_ID:
        return
        
    if last_status == discord.Status.offline and after.status != discord.Status.offline:
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if channel:
            await channel.send(f'Slymi is online!')
    
    last_status = after.status

bot.run(os.getenv('DISCORD_TOKEN'))