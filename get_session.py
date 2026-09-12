"""
Mavjud 'userbot_session.session' faylini o'qib,
StringSession matniga aylantirib, ekranga chiqaradi.
Bu matnni Render.com da session.txt sifatida yoki lokal session.txt
faylida saqlang.
"""

import asyncio
import os
import sys

from telethon import TelegramClient
from telethon.sessions import StringSession

from config import load_settings

SESSION_FILE = "userbot_session"


async def main():
    settings = load_settings()

    if not os.path.exists(f"{SESSION_FILE}.session"):
        print(f"[XATO]  '{SESSION_FILE}.session' fayli topilmadi!")
        print("   Avval main.py ni ishga tushirib, sessiyani yarating.")
        sys.exit(1)

    client = TelegramClient(SESSION_FILE, settings.api_id, settings.api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        print("[XATO]  Sessiya avtorizatsiya qilinmagan!")
        await client.disconnect()
        sys.exit(1)

    string_session = StringSession.save(client.session)

    print()
    print("=" * 60)
    print("  [OK]  SESSION_STRING tayyor!")
    print("=" * 60)
    print()
    print(string_session)
    print()
    print("=" * 60)
    print("  Yuqoridagi matnni session.txt fayliga (yoki Render'dagi")
    print("  secret file /etc/secrets/session.txt ga) joylashtiring.")
    print("=" * 60)
    print()

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
