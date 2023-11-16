import os

import discord
from discord import ApplicationContext
from dotenv import load_dotenv

from homework_bot.bot import MainBot
from homework_bot.cogs import GuildConfig, HWInfo, HWList, HWManagement

load_dotenv()

API_URL = "http://localhost:5000"

key = os.getenv("KEY").encode("utf8")

main_bot = MainBot(
    status=discord.Status.dnd,
    activity=discord.Game("with your homework"),
    intents=discord.Intents.default(),
    debug_guilds=[856028294645153802],
)


@main_bot.slash_command()
async def ping(ctx: ApplicationContext):
    # TODO: change the respond in future
    await ctx.respond(f"Pong! {main_bot.latency * 1000:.2f}ms")


main_bot.add_cog(HWManagement(main_bot, key, API_URL))
main_bot.add_cog(GuildConfig(main_bot, key))
main_bot.add_cog(HWList(main_bot, API_URL))
main_bot.add_cog(HWInfo(main_bot, API_URL))

main_bot.run(os.getenv("TOKEN"))
