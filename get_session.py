"""
Mavjud 'userbot_session.session' faylini o'qib,
StringSession matniga aylantirib, ekranga chiqaradi.
Bu matnni Render.com da SESSION_STRING muhit o'zgaruvchisi sifatida ishlating.
"""

import asyncio
import os
import sys

from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID   = os.getenv("API_ID", "YOUR_API_ID")
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")

SESSION_FILE = "userbot_session"


async def main():
    # Sessiya fayli mavjudligini tekshirish
    if not os.path.exists(f"{SESSION_FILE}.session"):
        print(f"[XATO]  '{SESSION_FILE}.session' fayli topilmadi!")
        print("   Avval main.py ni ishga tushirib, sessiyani yarating.")
        sys.exit(1)

    # Fayl sessiyasidan klientni ochish
    client = TelegramClient(SESSION_FILE, int(API_ID), API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("[XATO]  Sessiya avtorizatsiya qilinmagan!")
        await client.disconnect()
        sys.exit(1)

    # StringSession ga aylantirish
    string_session = StringSession.save(client.session)

    print()
    print("=" * 60)
    print("  [OK]  SESSION_STRING tayyor!")
    print("=" * 60)
    print()
    print(string_session)
    print()
    print("=" * 60)
    print("  Yuqoridagi matnni Render.com da")
    print("  SESSION_STRING muhit o'zgaruvchisiga joylashtiring.")
    print("=" * 60)
    print()

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
