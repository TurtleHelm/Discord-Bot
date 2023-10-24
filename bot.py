import platform, discord, json, asyncio
from discord.ext import commands
from datetime import datetime
from botutils import json
from random import choice
from pathlib import Path
from os import listdir

class Client(discord.Client):
    def __init__(self, bot):
        self.bot = bot
        self.cwd = str(Path(__file__).parents[0])
        self.config_token = json.load(open(self.cwd+'/bot_config/secrets.json'))['token']
        self.blacklisted_users = []
        self.bot.color_list = [c for c in {
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
            'DARK_NAVY': 0x2C3E50
        }.values()]
        self.bot.version = 'x.x.x'
        self.bot.DEFAULTPREFIX = '-'

def get_prefix(client, message): 
    # Gets Bot Prefix from Prefixes Json File
    data = json.read_json('prefixes')
    if not str(message.guild.id) in data: return commands.when_mentioned_or(client.bot.DEFAULTPREFIX)(client, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(client, message)

client = Client(commands.Bot(command_prefix=get_prefix, owner_id='YOUR DISCORD ID HERE', case_insensitive=True, help_command=None, intents=discord.Intents.all()))

def GetTime(): return f'{datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}'
def GetDate(): return f'{("0"+str(datetime.today().day)) if datetime.today().day < 10 else datetime.today().day}/{datetime.today().month}/{datetime.today().year}'

@client.bot.event
async def on_ready():
    print(f'Logged In As: {client.bot.user.name}\nID: {client.bot.user.id}')
    print(f'Logged In At: {GetDate()} {GetTime()}')
    print(f'Bot Version: {client.bot.version}\nDiscord Version: {discord.__version__}')
    print(f'Python Version: {platform.python_version()}')
    await client.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"Presence | {len(client.bot.guilds)} Servers"))

#Checks for Prefix in message and then executes command
@client.bot.event
async def on_message(message):
    if message.author.id == client.bot.user.id: return
    if message.author.id in client.blacklisted_users: return

    if f'<@!{client.bot.user.id}>' in message.content:
        data = json.read_json('prefixes')
        if str(message.guild.id) in data: prefix = data[str(message.guild.id)]
        else: prefix = client.bot.DEFAULT_PREFIX
        prefixMsg = await message.channel.send(f'Prefix is {prefix}')

    await client.bot.process_commands(message)

async def loadExtensions():
    for file in listdir(client.cwd+'/cogs'):
        if file.endswith('.py') and not file.startswith('_'):
            await client.bot.load_extension(f'cogs.{file[:-3]}')
            
async def main():
    async with client.bot:
        await loadExtensions()
        await client.bot.start(client.config_token)

#Runs Bot
asyncio.run(main())