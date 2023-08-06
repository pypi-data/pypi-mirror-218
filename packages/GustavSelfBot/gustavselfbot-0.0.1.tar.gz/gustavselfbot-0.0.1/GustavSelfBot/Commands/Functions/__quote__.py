import urllib.parse

import aiohttp
import discord
from discord.ext import commands


async def func_quote(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    url="https://clashy-besi.ddns.net/api/quote",
                    headers={"Accept": "application/json"},
            ) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    quote = res.get("text")
                    author = res.get("author")

                    if quote and author:
                        encoded_quote = urllib.parse.quote(quote)
                        encoded_author = urllib.parse.quote(author)

                        embed = f"https://embed.rauf.workers.dev/?author={encoded_author}&title=Quote%21&description={encoded_quote}&color=241f31&redirect=https%253A%252F%252Fclashy-besi.ddns.net%252Fapi%252Fquote"
                    else:
                        encoded_author = urllib.parse.quote(
                            bot.user.display_name
                        )
                        error_description = urllib.parse.quote(
                            "An error has occurred while processing the response."
                        )
                        embed = f"https://embed.rauf.workers.dev/?author={encoded_author}&title=Error%21&description={error_description}&color=a51d2d&redirect=https%253A%252F%252Fclashy-besi.ddns.net%252Fapi%252Fquote"
                else:
                    encoded_author = urllib.parse.quote(bot.user.display_name)
                    error_description = urllib.parse.quote(
                        "An error has occurred while handling the request."
                    )
                    embed = f"https://embed.rauf.workers.dev/?author={encoded_author}&title=Error%21&description={error_description}&color=a51d2d&redirect=https%253A%252F%252Fclashy-besi.ddns.net%252Fapi%252Fquote"
        except aiohttp.ClientError:
            encoded_author = urllib.parse.quote(bot.user.display_name)
            error_description = urllib.parse.quote(
                "An error has occurred while processing the request."
            )
            embed = f"https://embed.rauf.workers.dev/?author={encoded_author}&title=Error%21&description={error_description}&color=a51d2d&redirect=https%253A%252F%252Fclashy-besi.ddns.net%252Fapi%252Fquote"

        test = f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|||||||||||| {embed}"

        await message.add_reaction("👍")
        await message.reply(content=test)
