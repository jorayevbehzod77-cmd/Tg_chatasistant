"""
Telegram Userbot — Telethon + Google Gemini AI
Kiruvchi shaxsiy xabarlarga avtomatik javob beradi.
Barcha maxfiy kalitlar .env faylidan yoki Render env vars'dan o'qiladi.
"""

import logging

from assistant import GeminiAssistant
from bot import UserBot
from config import load_session_string, load_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)


def main() -> None:
    settings = load_settings()
    session_string = load_session_string()

    assistant = GeminiAssistant(
        api_key=settings.gemini_api_key,
        model_name=settings.model_name,
        max_history=settings.max_history,
    )
    bot = UserBot(settings=settings, session_string=session_string, assistant=assistant)
    bot.run()


if __name__ == "__main__":
    main()
