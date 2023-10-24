from discord.ext import commands

def multi_check():
    """
    Used to check if multiple decorators are true\n
    Usage:
    - @utils.decorators.multi_check()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_channels and ctx.me.guild_permissions.manage_channels
    return commands.check(predicate)

def kick_Perm():
    """
    Used to check if both the author and the bot has kick perms\n
    Usage:
    - @utils.decorators.kick_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.kick_members  and ctx.me.guild_permissions.kick_members
    return commands.check(predicate)

def ban_Perm():
    """
    Used to check if both the author and the bot has ban perms\n
    Usage:
    - @utils.decorators.kick_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.ban_members  and ctx.me.guild_permissions.ban_members
    return commands.check(predicate)

def admin_Perm():
    """
    Used to check if both the author and the bot has admin perms\n
    Usage:
    - @utils.decorators.admin_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.ban_members  and ctx.me.guild_permissions.ban_members
    return commands.check(predicate)

def mm_Perm():
    """
    Used to check if both the author and the bot has manage messages perms\n
    Usage:
    - @utils.decorators.mm_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_messages and ctx.me.guild_permissions.manage_messages
    return commands.check(predicate)

def mc_Perm():
    """
    Used to check if both the author and the bot has manage channel perms\n
    Usage:
    - @utils.decorators.mc_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_channels and ctx.me.guild_permissions.manage_channels
    return commands.check(predicate)

def mr_Perm():
    """
    Used to check if both the author and the bot has manage roles perms\n
    Usage:
    - @utils.decorators.mr_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_roles and ctx.me.guild_permissions.manage_roles
    return commands.check(predicate)

def val_Perm():
    """
    Used to check if both the author and the bot has manage roles perms\n
    Usage:
    - @utils.decorators.val_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.view_audit_log and ctx.me.guild_permissions.view_audit_log
    return commands.check(predicate)

def mw_Perm():
    """
    Used to check if both the author and the bot has manage roles perms\n
    Usage:
    - @utils.decorators.mw_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_webhooks and ctx.me.guild_permissions.manage_webhooks
    return commands.check(predicate)

def ms_Perm():
    """
    Used to check if both the author and the bot has manage roles perms\n
    Usage:
    - @utils.decorators.ms_Perm()
    """
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.manage_server and ctx.me.guild_permissions.manage_server
    return commands.check(predicate)
