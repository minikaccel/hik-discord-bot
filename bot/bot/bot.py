from __future__ import annotations

import logging
import os
from pathlib import Path

import hikari
import lightbulb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from pytz import utc

from bot import __version__

load_dotenv()


class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self._extensions = [p.stem for p in Path('./bot/bot/extensions/').glob('*.py')]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        token = os.getenv("TOKEN")

        super().__init__(
            prefix='-',
            insensitive_commands=True,
            token=token,
            intents=hikari.Intents.ALL,
        )

    def run(self) -> None:

        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name=f"-help | Version {__version__}",
                type=hikari.ActivityType.WATCHING,
            ),
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        for ext in self._extensions:
            self.load_extension(f"bot.bot.extensions.{ext}")
            logging.info(f"[{ext} extensions loaded]")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        logging.info('[BOT READY]')


    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()