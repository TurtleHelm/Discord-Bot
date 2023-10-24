import discord
from discord.ext import commands
import random
from aiohttp import ClientSession
import re
import asyncio
from botutils import json, GetMessage

responses = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes - definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.']

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    
    for key, value in matches:
        try: time += time_dict[value] * float(key)
        except KeyError: raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valid arguments")
        except ValueError: raise commands.BadArgument(f'{key} is not a number')
        
    return time

class Fun(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): print(f'{self.__class__.__name__} Cog loaded')

    @commands.command(name="_8ball", description="A simple 8ball command", aliases=['8ball'], usage="<command> <question>")
    async def _8ball(self, ctx): await ctx.send(f"Answer: {random.choice(responses)}")

    @commands.command(name="rps", description="A simple Rock Paper Scissors command", usage="<command> <r, p, s>")
    async def rps(self, ctx, message): return

    # @commands.command(name="giveaway", description="A simple giveaway command", aliases=["gw"], usage="<command>")
    # @commands.guild_only()
    # async def giveaway(self, ctx):
    #     await ctx.send("Lets start the giveaway, answer the questions and we will proceed")

    #     questionList = [
    #         ["Giveaway channel?", "Mention the channel"],
    #         ["How long should this giveaway last?", "`d|h|m|s`"],
    #         ["What are you giving away?", "I.E. An Iphone X"]]

    #     answers = {}

    #     for i, question in enumerate(questionList):
    #         answer = await GetMessage(self.bot, ctx, question[0], question[1])

    #         if not answer:
    #             await ctx.send("You failed to answer, please be quicker next time")
    #             return
            
    #         answers[i] = answer

    #     em = discord.Embed(name="Giveaway")
    #     for key, value in answers.items():
    #         em.add_field(name=f'Question: `{questionList[key][0]}`', value=f'Answer: `{value}`', inline=False)

    #     m = await ctx.send("Are these all valid?", embed=em)
    #     await m.add_reaction("🟩")
    #     await m.add_reaction("🟥")

    #     try:
    #         reaction, member = await self.bot.wait_for("reaction_add", timeout=60, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel)
    #     except asyncio.TimeoutError:
    #         await ctx.send("Confimation Failed, please try again")
    #         return

    #     if str(reaction.emoji) not in ["🟩", "🟥"] or str(reaction.emoji) == "🟥":
    #         await ctx.send("Cancelling giveaway")
    #         return

    #     channelId = re.findall(r"[0-9]+", answers[0])[0]
    #     channel = self.bot.get_channel(int(channelId))

    #     time = convert(answers[1])

    #     gwEm = discord.Embed(title="🎉 **Giveaway** 🎉", description=answers[2])
    #     gwEm.set_footer(text=f'This giveaway ends {time} seconds from this message')
    #     gwMsg = await channel.send(embed=gwEm)
    #     await gwMsg.add_reaction("🎉")

    #     await asyncio.sleep(time)

    #     message = await channel.fetch_message(gwMsg.id)
    #     users = await message.reactions[0].users().flatten()
    #     users.pop(users.index(ctx.guild.me))
    #     users.pop(users.index(ctx.author))

    #     if len(users) == 0:
    #         await channel.send("No winner was decided")

    #     winner = random.choice(users)

    #     await channel.send(f"**Congrats** {winner.mention} Won {answers[2]}!\nPlease contact {ctx.author.mention} about your prize")

async def setup(bot): await bot.add_cog(Fun(bot))