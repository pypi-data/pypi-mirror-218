import discord
from discord.ext import commands

from GustavSelfBot import log

from GustavSelfBot.Commands.Functions import func_ping
from GustavSelfBot.Commands.Functions import func_quote


async def _blacklist(ctx: commands.Context):
    pass


async def ping(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_ping(bot, ctx, message)
    except discord.errors.ClientException as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)


async def quote(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_quote(bot, ctx, message)
    except discord.errors.ClientException as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)
