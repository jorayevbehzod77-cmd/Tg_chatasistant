"""
Telegram userbot moduli: Telethon klientini, xabar handlerini
va Render uchun health-check serverini o'z ichiga oladi.
"""

import asyncio
import logging

from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from assistant import GeminiAssistant
from config import Settings

log = logging.getLogger("userbot.bot")


class UserBot:
    """Telegram klientini va unga bog'liq handlerlarni boshqaradi."""

    def __init__(self, settings: Settings, session_string: str, assistant: GeminiAssistant):
        self._settings = settings
        self._assistant = assistant
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._client = TelegramClient(
            StringSession(session_string),
            settings.api_id,
            settings.api_hash,
            loop=self._loop,
        )
        self._client.add_event_handler(self._on_message, events.NewMessage(incoming=True))

    async def _on_message(self, event: events.NewMessage.Event) -> None:
        """Har bir kiruvchi shaxsiy xabarga Gemini javobini qaytaradi."""
        if not event.is_private:
            return

        sender = await event.get_sender()
        if sender and getattr(sender, "bot", False):
            return

        user_text = event.raw_text
        if not user_text:
            return

        user_id = event.sender_id
        log.info("Xabar [%s]: %s", user_id, user_text[:80])

        answer = await self._assistant.reply(user_id, user_text)

        await event.reply(answer)
        log.info("Javob [%s]: %s", user_id, answer[:80])

    async def _run_health_server(self) -> None:
        """Render uxlab qolmasligi uchun kichik HTTP server ishga tushiradi."""

        async def health_handler(_request):
            return web.Response(text="Bot is alive")

        app = web.Application()
        app.router.add_get("/", health_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self._settings.health_port)
        await site.start()
        log.info("Health-check server ishga tushdi: http://0.0.0.0:%s", self._settings.health_port)

    async def start(self) -> None:
        log.info("Userbot ishga tushmoqda …")

        await self._run_health_server()
        await self._client.start()

        me = await self._client.get_me()
        log.info("Tayyor! Sifatida kirdi: @%s (%s)", me.username, me.first_name)
        log.info("Kiruvchi shaxsiy xabarlarga Gemini orqali javob beriladi.")

        await self._client.run_until_disconnected()

    def run(self) -> None:
        self._loop.run_until_complete(self.start())
