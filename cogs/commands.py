import discord
from discord.ext import commands
import platform
import random
import asyncio
import re
import utils.json
import utils.decorators
from utils.util import GetMessage

def count(counter):
    counter = counter + 1    
    return

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog loaded')

    @commands.command(name='hi', description="A simple Test command", aliases=['hello'], usage="<command>")
    async def _hi(self, ctx):
        await ctx.send(f'Hi {ctx.author.mention}!')

    @commands.command(name="echo", description="Repeats a specific Users Message", usage="<command>")
    async def echo(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(title="Please tell me what you want me to repeat",description="This request will timeout after 1 minute")
        sent =  await ctx.send("embed-em")
        try:
            msg = await self.bot.wait_for("message", timeout=60, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling due to timeout", delete_after=10)

    @commands.command(name="channelstats", description="Sends an embed with channel stats", aliases=['cs'], usage="<command>")
    @utils.decorators.mc_Perm()
    async def channelstats(self, ctx):
        channel = ctx.channel
        em = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=random.choice(self.bot.color_list))
        em.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        em.add_field(name="Channel Id", value=channel.id, inline=False)
        em.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic'}", inline=False)
        em.add_field(name="Channel Position", value=channel.position, inline=False)
        em.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        em.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        em.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        em.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        em.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
        em.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Commands(bot))