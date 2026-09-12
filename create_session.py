"""
Telegram sessiyasini yaratib, session.txt fayliga saqlaydigan skript.
Birinchi marta ishga tushirganda telefon raqam va tasdiqlash kodi so'raladi.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = os.getenv("API_ID", "").strip()
API_HASH = os.getenv("API_HASH", "").strip()

if not API_ID or not API_HASH:
    print("[XATO] .env faylida API_ID va API_HASH belgilanmagan!")
    sys.exit(1)


async def main():
    print("Telegram sessiyasini yaratish...")
    print("Telefon raqamingizni kiriting (+998...)")
    print()

    client = TelegramClient(StringSession(), int(API_ID), API_HASH)
    await client.start()

    session_string = client.session.save()

    with open("session.txt", "w", encoding="utf-8") as f:
        f.write(session_string)

    me = await client.get_me()
    print()
    print("=" * 50)
    print(f"  Tayyor! @{me.username} ({me.first_name})")
    print("  session.txt fayli yaratildi.")
    print("  Endi botni ishga tushiring: python main.py")
    print("=" * 50)

    await client.disconnect()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
