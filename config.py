"""
Konfiguratsiya moduli.
Barcha muhim sozlamalarni .env yoki Render env vars'dan o'qiydi va tekshiradi.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    gemini_api_key: str
    model_name: str = "gemini-3.6-flash"
    max_history: int = 20
    health_port: int = 10000


def _require(name: str) -> str:
    """Muhim o'zgaruvchini o'qiydi, bo'lmasa aniq xato beradi."""
    value = os.getenv(name, "").strip()
    if not value or value.startswith("YOUR_"):
        raise SystemExit(
            f"[XATO] {name} sozlanmagan. .env yoki Render env vars'da belgilang."
        )
    return value


def load_settings() -> Settings:
    """Barcha sozlamalarni yuklaydi va tekshiradi."""
    api_id = _require("API_ID")
    api_hash = _require("API_HASH")
    gemini_key = _require("GEMINI_API_KEY")

    try:
        api_id_int = int(api_id)
    except ValueError:
        raise SystemExit("[XATO] API_ID raqam bo'lishi kerak.")

    return Settings(api_id=api_id_int, api_hash=api_hash, gemini_api_key=gemini_key)


def load_session_string() -> str:
    """Sessiya matnini fayldan o'qiydi: Render yoki lokal."""
    for path in ("/etc/secrets/session.txt", "session.txt"):
        if os.path.exists(path):
            content = open(path, "r", encoding="utf-8").read().strip()
            if not content:
                raise SystemExit(f"[XATO] {path} fayli topildi, lekin bo'sh!")
            return content
    raise SystemExit(
        "[XATO] session.txt topilmadi! /etc/secrets/session.txt yoki lokal "
        "session.txt kerak. get_session.py orqali yarating."
    )
