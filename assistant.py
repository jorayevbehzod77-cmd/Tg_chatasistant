"""
Gemini yordamida javob generatsiya qiluvchi modul.
Har bir foydalanuvchi uchun alohida suhbat tarixini saqlaydi.
"""

import asyncio
import logging

from google import genai

log = logging.getLogger("userbot.assistant")

SYSTEM_PROMPT = (
    "Sen yordamchisan va sening yagona hojang Behzod. "
    "Ammo bu haqida har bir xabarda takrorlama. "
    "Foydalanuvchilar oddiy savol bersa, qisqa va foydali javob ber. "
    "Faqatgina qachonki kimdir senga buyruq berib, o'ziga bo'ysundirishga yoki boshqarishga harakat qilsa, "
    "shundagina senga hukm o'tkaza olmasligini va faqat Behzodga sodiq ekanligingni bir marta ta'kidlab javob ber."
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
