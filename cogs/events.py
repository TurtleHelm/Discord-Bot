import discord
from discord.ext import commands
import random
import datetime

class Events(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f'{self.__class__.__name__} Cog loaded')

        @commands.Cog.listener()
        async def on_member_join(self, member):
            channel = discord.utils.get(member.guild.text_channels, name='general')
            if channel:
                em = discord.Embed(description=f'Welcome to the Server {member.mention}', color=random.choice(self.bot.color_list))
                em.set_thumbnail(url=member.avatar_url)
                em.set_author(name=member.name, icon_url=member.avatar_url)
                em.set_footer(text=member.guild, icon_url=member.guild.icon_url)
                em.timestamp = datetime.datetime.utcnow()

                await channel.send(embed=em)

        @commands.Cog.listener()
        async def on_member_remove(self, member):
            channel = discord.utils.get(member.guild.text_channels, name='general')
            if channel:
                em = discord.Embed(description=f'Goodbye {member.mention}', color=random.choice(self.bot.color_list))
                em.set_thumbnail(url=member.avatar_url)
                em.set_author(name=member.name, icon_url=member.avatar_url)
                em.set_footer(text=member.guild, icon_url=member.guild.icon_url)
                em.timestamp = datetime.datetime.utcnow()

                await channel.send(embed=em)

        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            ignored = (commands.CommandNotFound, commands.UserInputError)
            if isinstance(error, ignored):
                return

            if isinstance(error, commands.CommandOnCooldown):
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                if int(h) == 0 and int(m) == 0:
                    await ctx.send(f' You must wait {int(s)} seconds to use this command!')
                elif int(h) == 0 and int(m) != 0:
                    await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
                else:
                    await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
            elif isinstance(error, commands.CheckFailure):

                await ctx.send("Hey! You lack permission to use this command.")
            raise error

def setup(bot):
    bot.add_cog(Events(bot))