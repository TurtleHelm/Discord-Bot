import discord, platform, random, asyncio
from botutils import json, decorators
from discord.ext import commands

def count(counter): counter = counter + 1

class Commands(commands.Cog):

    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): print(f'{self.__class__.__name__} Cog loaded')

    @commands.command(name='hi', description="A simple Test command", aliases=['hello'], usage="<command>")
    async def _hi(self, ctx):
        await ctx.send(f'Hi {ctx.author.mention}!')

    @commands.command(name="echo", description="Repeats a specific Users Message", usage="<command> <sentence>")
    async def echo(self, ctx, *args):
        
        if args == (): await ctx.send('Remember to add text to echo!', delete_after=10)
        else:
            await ctx.message.delete()
            await ctx.send(" ".join(args))

    @commands.command(name="channelstats", description="Sends an embed with channel stats", aliases=['cs'], usage="<command>")
    @decorators.mc_Perm()
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

async def setup(bot): await bot.add_cog(Commands(bot))