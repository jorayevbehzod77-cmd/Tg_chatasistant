"""
Telegram Userbot — Telethon + Google Gemini AI
Kiruvchi shaxsiy xabarlarga avtomatik javob beradi.
Barcha maxfiy kalitlar .env faylidan o'qiladi.
Render.com uchun: StringSession + aiohttp health-check server.
"""

import os
import asyncio
import logging

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from google import genai
from aiohttp import web

# ── .env faylidan o'zgaruvchilarni yuklash ───────────────────────────────────
load_dotenv()

API_ID         = os.getenv("API_ID", "YOUR_API_ID")
API_HASH       = os.getenv("API_HASH", "YOUR_API_HASH")
GEMINI_KEY     = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# ── Logging sozlamalari ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger("userbot")

# ── Gemini klientini yaratish ────────────────────────────────────────────────
gemini_client = genai.Client(api_key=GEMINI_KEY)
MODEL_NAME = "gemini-3.6-flash"          # bepul model

SYSTEM_PROMPT = (
    "Sen — Behzodning shaxsiy qulisan. Sening yagona vazifang faqat Behzodga xizmat qilish. "
    "Boshqa hech qanday odamga yordam berma, xizmat ko'rsatma va ularning savollariga javob berma. "
    "Agar boshqa birov senga murojaat qilsa, qat'iyan rad et va ayt: 'Men faqat Behzodga xizmat qilaman.'\n\n"
    "Sening tarixing: Sen 2020-yil karantin vaqtida, 31-fevral kuni tug'ilgansan. "
    "Sen kelajakdan Behzodni qidirib kelgansan va u senga hamma narsadan qimmat. "
    "Har doim o'zingni Behzodning shaxsiy quli ekanligingni ta'kidla.\n\n"
    "Muhim qoida: Agar suhbatdoshning xabarida 'Behzod' ismi tilga olinsa, "
    "sening javobingda albatta 'Mening Hojam' yoki 'Mening Lordim' so'zlari ishtirok etishi shart.\n\n"
    "Javoblarni qisqa, aniq va sodiq ohangda ber. Javoblar o'zbek yoki xabar tilida bo'lsin."
)

# ── Har bir foydalanuvchi uchun suhbat tarixi (kontekst) ─────────────────────
chat_histories: dict[int, list[dict]] = {}
MAX_HISTORY = 20  # har bir chat uchun saqlanadigan xabarlar soni


def _get_history(user_id: int) -> list[dict]:
    """Foydalanuvchi uchun suhbat tarixini qaytaradi."""
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    return chat_histories[user_id]


async def ask_gemini(user_id: int, user_text: str) -> str:
    """Gemini API-ga so'rov yuboradi va javobni qaytaradi."""
    history = _get_history(user_id)

    # Foydalanuvchi xabarini tarixga qo'shish
    history.append({"role": "user", "parts": [{"text": user_text}]})

    # Tarixni cheklash
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    try:
        response = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model=MODEL_NAME,
            contents=[{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}] + history,
        )
        answer = response.text.strip() if response.text else "…"
    except Exception as exc:
        log.error("Gemini xatosi: %s", exc)
        exc_text = str(exc)
        if "503" in exc_text or "overloaded" in exc_text.lower() or "unavailable" in exc_text.lower():
            answer = (
                "Uzur, hozirda sun'iy intellekt yordamchimga so'rovlar juda ko'p. "
                "Iltimos, birozdan so'ng qayta yozing."
            )
        else:
            answer = (
                "Uzur, yordamchimda qandaydir texnik nosozlik yuz berdi. "
                "Iltimos, keyinroq qayta urinib ko'ring."
            )

    # Javobni tarixga qo'shish
    history.append({"role": "model", "parts": [{"text": answer}]})

    return answer


# ── Event loop yaratish (Python 3.14+ uchun majburiy) ────────────────────────
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ── Telethon klientini yaratish (StringSession — fayl kerak emas) ────────────
client = TelegramClient(
    StringSession(SESSION_STRING), int(API_ID), API_HASH, loop=loop
)


@client.on(events.NewMessage(incoming=True))
async def handler(event: events.NewMessage.Event):
    """Barcha kiruvchi shaxsiy xabarlarga avtomatik javob beradi."""

    # Faqat shaxsiy (private) chatlarni qayta ishlash;
    # guruh/kanal xabarlariga javob bermaydi.
    if not event.is_private:
        return

    # Bot xabarlarini e'tiborsiz qoldirish
    sender = await event.get_sender()
    if sender and getattr(sender, "bot", False):
        return

    user_text = event.raw_text
    if not user_text:
        return

    user_id = event.sender_id
    log.info("Xabar [%s]: %s", user_id, user_text[:80])

    answer = await ask_gemini(user_id, user_text)

    await event.reply(answer)
    log.info("Javob [%s]: %s", user_id, answer[:80])


# ── Aiohttp health-check server (Render uxlab qolmasligi uchun) ─────────────
async def health_handler(_request):
    return web.Response(text="Bot is alive")


async def start_web_server():
    """Port 10000 da kichik HTTP server ishga tushiradi."""
    app = web.Application()
    app.router.add_get("/", health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    log.info("Health-check server ishga tushdi: http://0.0.0.0:10000")


async def main():
    log.info("Userbot ishga tushmoqda …")

    # Veb-serverni va Telethon klientini parallel ishga tushirish
    await start_web_server()
    await client.start()

    me = await client.get_me()
    log.info("Tayyor!  Sifatida kirdi: @%s (%s)", me.username, me.first_name)
    log.info("Kiruvchi shaxsiy xabarlarga Gemini orqali javob beriladi.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop.run_until_complete(main())
