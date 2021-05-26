# all stuff needed to define permissions
from discord.ext import commands
from tools import _json

owners = _json.get_config()["owners"]

def is_owner(ctx):
  return ctx.author.id in owners

async def check_permissions(ctx, perms, *, check=all):
    if ctx.author.id in owners:
        return True
    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)