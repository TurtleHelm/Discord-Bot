import discord, platform, os, asyncio, re
from botutils import json, decorators
from discord.ext import commands

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?") # Basic Regex
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400} # Sets Time

#Converts time into proper units
class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valid arguments")
            except ValueError:
                raise commands.BadArgument(f'{key} is not a number')
        return time

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = 0 # Log Channel ID

    ownerMsg = "You must be the owner to use this command"
    adminMsg = "You must be an admin to use this command"

    # On ready prints loaded cog to console
    @commands.Cog.listener()
    async def on_ready(self): print(f'{self.__class__.__name__} Cog loaded')

    @commands.command(name='stats', description=f"A useful command to display stats about the bot\n({adminMsg})", aliases=['botstats', 'bstats'], usage="<command>")
    @decorators.admin_Perm()
    async def stats(self, ctx):
        """
        A useful command to display stats about the bot
        """
        #Checks Python Version
        pythonVersion = platform.python_version()
        #Checks Discord.py Version
        dpyVersion = discord.__version__
        #Checks Server Count
        serverCount = len(self.bot.guilds)
        #Checks Member Count
        memberCount = len(set(self.bot.get_all_members()))
        
        #Sets up an embed
        em = discord.Embed(title=f'{self.bot.user.name}', description='\uFEFF', color=ctx.author.color, timestamp=ctx.message.created_at)

        #Adds Fields
        em.add_field(name='Bot Version:', value=self.bot.version)
        em.add_field(name='Python Version:', value=pythonVersion)
        em.add_field(name='Discord.py Version:', value=dpyVersion)
        em.add_field(name='Total Servers:', value=serverCount)
        em.add_field(name='Total Users:', value=memberCount)
        em.add_field(name='Bot Dev(s):', value='<YOUR_ID>\n')

        #Sets footer + Author
        em.set_footer(text=f'{self.bot.user.name}')
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        #Sends Embed
        await ctx.send(embed=em)

    @commands.command(name='logout', description='Disconnects the bot from discord', aliases=['disconnect', 'close', 'stop'], usage="<command>")
    @commands.is_owner()
    async def logout(self, ctx):
        """
        Disconnects bot from discord (must be owner)
        """
        await ctx.send(f"Logging out :wave:")
        await self.bot.logout()

    @commands.command(name="blacklist", description=f'Blacklists A specific user from using commands', aliases=['bl'], usage="<command> <member>")
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("You cannot blacklist yourself")
            return

        self.bot.blacklisted_users.append(user.id)
        data = json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        json.write_json(data, "blacklist")
        await ctx.send(f"blacklisted {user.name}")

    @commands.command(name="unblacklist", description=f'Unblacklists a specific user', aliases=['ubl'], usage="<command> <member>")
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        json.write_json(data, "blacklist")
        await ctx.send(f"Unblacklisted {user.name}")

    @commands.command(name="prefix", description="Sets a new prefix", aliases=['p'], usage="<command> <prefix>")
    @decorators.admin_Perm()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre='-'):
        """
        Sets a custom prefix
        """
        data = json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        json.write_json(data, 'prefixes')
        await ctx.send(f"Changed prefix to {pre}")

    @commands.command(name="kick", description="kicks a specific user from the server", aliases=['boot'], usage="<command> <member> [reason]")
    @decorators.kick_Perm()
    @commands.guild_only()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.kick(user=user, reason=reason)
        em = discord.Embed(title=f"{ctx.author.name} kicked: {user.name}", desctription=reason)
        await self.log_channel.send(embed=em)

    @commands.command(name="ban", description="Bans a specficic user from the server", usage="<command> <member> [reason]")
    @decorators.ban_Perm()
    @commands.guild_only()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.ban(user=user, reason=reason)
        em = discord.Embed(title=f"{ctx.author.name} banned: {user.name}", description=reason)
        await self.log_channel.send(embed=em)

    @commands.command(name="unban", description="Unbans a specific user", usage="<command> <member> [reason]")
    @decorators.ban_Perm()
    @commands.guild_only()
    async def unban(self, ctx, user: discord.Member, *, reason=None):
        user = await self.bot.fetch_user(int(user))
        await ctx.guild.unban(user=user, reason=reason)
        em = discord.Embed(title=f"{ctx.author.name} unbanned: {user.name}", description=reason)
        await self.log_channel.send(embed=em)

    @commands.command(name="purge", description="Removes a specific amount of messages (default: 15)", aliases=['clear'], usage="<command> [amount of msgs]")
    @decorators.mm_Perm()
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount+1)
        em = discord.Embed(title=f"{ctx.author.name} purged: {ctx.author.name}", description=f"{amount} msgs were cleared")
        await self.log_channel.send(embed=em)

    @commands.command(name="lockdown", description="Stops messages being sent in a specific channel", usage="<command> [channel]")
    @decorators.multi_check()
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = { ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False) }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"Put **{channel.name}** Into lockdown")

        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"Put **{channel.name}** Into lockdown")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"Removed **{channel.name}** From lockdown")

    @commands.command(name="reload", description=f"Reloads all cogs\n({ownerMsg})", usage="<command> [cog]")
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(title="Reloading all cogs!",color=0x808080,timestamp=ctx.message.created_at)
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.reload_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(name=f"Reloaded: {ext}",value='\uFEFF',inline=False)
                        except Exception as e:
                            embed.add_field(name=f"Failed to reload: {ext}",value=e,inline=False)
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                embed = discord.Embed(title="Reloading all cogs",color=0x808080,timestamp=ctx.message.created_at)
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    embed.add_field(name=f"Failed to reload: {ext}",value="This cog does not exist.",inline=False)
                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.reload_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(name=f"Reloaded: {ext}",value='\uFEFF',inline=False)
                    except Exception as e:
                        embed.add_field(name=f"Failed to reload: {ext}",value=e,inline=False)
                await ctx.send(embed=embed)

    @commands.command(name='mute', description='Mutes a given user for x time', usage='<member> [time]')
    @decorators.mr_Perm()
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found")
            return
        await member.add_roles(role)
        await self.log_channel.send((f'Muted {member.display_name} for {time}s' if time else f'Muted {member.display_name}'))

        if time:
            await asyncio.sleep(time)
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.display_name}")

    @commands.command(name='unmute', description='Unmutes a given user', usage='<member>')
    @decorators.mr_Perm()
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role")

        if role not in member.roles: await ctx.send(f"This member is not muted")
        await member.remove_roles(role)
        await ctx.send(f"Unmuted {member.display_name}")

async def setup(bot): await bot.add_cog(Admin(bot))