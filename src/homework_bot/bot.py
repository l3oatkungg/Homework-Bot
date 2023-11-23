import logging

import databases
import discord
import httpx
from discord import Colour

from homework_bot.utils import pretty_time

logger = logging.getLogger(__name__)


class MainBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_color = Colour.from_rgb(185, 153, 146)

        self.http_client = httpx.AsyncClient()
        self.db = databases.Database("sqlite:///database.db")

    async def on_ready(self):
        await self.wait_until_ready()

        logger.info(f"Logged in as {self.user}")
        logger.info(f"ID:   {self.user.id}")
        logger.info(f"Ping: {pretty_time(self.latency)}")

        logger.info("-" * 20)
        logger.info("Setting up...")

        await self.db.connect()

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds (
            GuildID BIGINT PRIMARY KEY,
            ClassroomSecret TEXT
            )
            """
        )

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            UserID BIGINT PRIMARY KEY,
            GuildID BIGINT,
            Password TEXT,
            FOREIGN KEY (GuildID) REFERENCES guilds(GuildID)
            )
            """
        )

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS notify (
            UserID BIGINT PRIMARY KEY,
            GuildID BIGINT,
            Mode TEXT,
            BeforeDue INTEGER,
            FOREIGN KEY (GuildID) REFERENCES guilds(GuildID)
            )
            """
        )

        logger.info("Ready!")
        logger.info("-" * 20)

    async def close(self):
        logger.info("Closing...")

        await self.http_client.aclose()
        await self.db.disconnect()
        await super().close()
