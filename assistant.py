"""
Gemini yordamida javob generatsiya qiluvchi modul.
Har bir foydalanuvchi uchun alohida suhbat tarixini saqlaydi.
"""

import asyncio
import logging

from google import genai

log = logging.getLogger("userbot.assistant")

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

FRIENDLY_ERROR_BUSY = (
    "Uzur, hozirda sun'iy intellekt yordamchimga so'rovlar juda ko'p. "
    "Iltimos, birozdan so'ng qayta yozing."
)
FRIENDLY_ERROR_GENERIC = (
    "Uzur, yordamchimda qandaydir texnik nosozlik yuz berdi. "
    "Iltimos, keyinroq qayta urinib ko'ring."
)


class GeminiAssistant:
    """Foydalanuvchilar bilan suhbat tarixini va Gemini so'rovlarini boshqaradi."""

    def __init__(self, api_key: str, model_name: str, max_history: int):
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name
        self._max_history = max_history
        self._histories: dict[int, list[dict]] = {}

    def _history_for(self, user_id: int) -> list[dict]:
        return self._histories.setdefault(user_id, [])

    async def reply(self, user_id: int, user_text: str) -> str:
        """Foydalanuvchi xabariga Gemini orqali javob qaytaradi."""
        history = self._history_for(user_id)
        history.append({"role": "user", "parts": [{"text": user_text}]})
        del history[: -self._max_history]  # eng oxirgi N ta xabarni saqlab qolish

        answer = await self._ask_gemini(history)

        history.append({"role": "model", "parts": [{"text": answer}]})
        return answer

    async def _ask_gemini(self, history: list[dict]) -> str:
        try:
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=self._model_name,
                contents=[{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}] + history,
            )
            return response.text.strip() if response.text else "…"
        except Exception as exc:
            log.error("Gemini xatosi: %s", exc)
            exc_text = str(exc).lower()
            if "503" in exc_text or "overloaded" in exc_text or "unavailable" in exc_text:
                return FRIENDLY_ERROR_BUSY
            return FRIENDLY_ERROR_GENERIC
