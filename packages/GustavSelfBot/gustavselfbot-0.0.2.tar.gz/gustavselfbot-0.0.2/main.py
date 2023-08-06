import discord
import os

from GustavSelfBot import log, Config, bot

if __name__ == "__main__":
    try:
        os.makedirs("_chatlogs", exist_ok=True)
    except PermissionError as e:
        log.error(f"Could not create _chatlogs folder: {e}")
        raise Exception(f"Could not create _chatlogs folder: {e}")
    try:
        bot.run(token=Config["token"], log_handler=None)
    except discord.errors.LoginFailure as e:
        log.error(e)
        raise Exception(e)
