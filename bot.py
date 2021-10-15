from pathlib import Path
from discord.ext import commands 
import discord
import json
import platform 
import logging
import os
import utils.json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n")

#Gets Bot Prefix from Prefixes Json File
def get_prefix(bot, message):
    data = utils.json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Sets Default Prefix to '-'
DEFAULTPREFIX = "-"
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
#Sets up bot with basic stuff
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id='YOUR DISCORD ID HERE', help_command=None)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

#Adds basic info to bot
bot.DEFAULTPREFIX = DEFAULTPREFIX
bot.blacklisted_users = []
bot.cwd = cwd

#Version
bot.version = '1.0.0'

#Different Colors
bot.colors = {
    'WHITE': 0xFFFFFF, 
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LIGHT_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x11806A,
    'DARK_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50 }

bot.color_list = [c for c in bot.colors.values()]

#Sets up bot when it is ready
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} : {bot.user.id}")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"Python Discord Bot | {len(bot.guilds)} Servers"))

#Checks for Prefix in message and then executes command
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.author.id in bot.blacklisted_users:
        return

    if f'<@!{bot.user.id}>' in message.content:
        data = utils.json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = bot.DEFAULTPREFIX
        prefixMsg = await message.channel.send(f'Prefix is {prefix}')

    await bot.process_commands(message)

#Loads Cogs
if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f'cogs.{file[:-3]}')
    bot.run(bot.config_token) 

#Runs Bot
bot.run(bot.config_token)