"""
Mavjud 'userbot_session.session' faylini o'qib,
StringSession matniga aylantirib, session.txt fayliga saqlaydi.
Render.com uchun yoki lokal ishlatish uchun.
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
        print("   Avval Telethon orqali sessiya yarating:")
        print()
        print("   python -c \"from telethon.sync import TelegramClient; \\")
        print(f"     TelegramClient('{SESSION_FILE}', {API_ID}, '{API_HASH}').start()\"")
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

    # session.txt fayliga saqlash
    with open("session.txt", "w", encoding="utf-8") as f:
        f.write(string_session)

    print()
    print("=" * 60)
    print("  [OK]  session.txt fayli yaratildi!")
    print("=" * 60)
    print()
    print("  Endi botni ishga tushirishingiz mumkin:")
    print("    python main.py")
    print()
    print("  Render.com uchun: session.txt ichidagi matnni")
    print("  Secret Files bo'limiga joylashtiring.")
    print("=" * 60)
    print()

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
