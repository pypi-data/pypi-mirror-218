from datetime import datetime

import discord
from discord.ext import commands

from GustavSelfBot.Commands import quote, ping
from GustavSelfBot import log, os


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


async def func_on_message(bot: commands.Bot, message: discord.Message):
    if bot.user in message.mentions:
        if message.author.id == bot.user.id:
            return
        else:
            log.info(f"Message received from {message.author.display_name} (ID: {message.author.id}): {message.content}")

    if message.content.startswith(">"):
        if message.author.id != bot.user.id:
            return
        if message.author.id == bot.user.id:
            if message.content.__contains__("|") or message.content.__contains__("||"):
                return
        if message.content.__contains__("ping"):
            ctx = await bot.get_context(message)
            await ping(bot, ctx, message)
        elif message.content.__contains__("quote"):
            ctx = await bot.get_context(message)
            await quote(bot, ctx, message)
    if message.guild is not None:
        guild_folder = f"_chatlogs/{message.guild.name}_{message.guild.id}"
        channel_folder = f"{guild_folder}/{message.channel.name}_{message.channel.id}"
    else:
        guild_folder = f"_chatlogs/_DMS"
        channel_folder = f"{guild_folder}/{message.channel.recipient.display_name}_{message.channel.id}"
    log_filename = f"{channel_folder}/{timestamp}.log"

    os.makedirs(channel_folder, exist_ok=True)

    with open(log_filename, "a") as log_file:
        log_file.write(f"{message.author.display_name} ({message.author.id}): {message.content}\n")
