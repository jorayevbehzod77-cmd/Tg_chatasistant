"""
Konfiguratsiya moduli.
Barcha sozlamalarni lokal .env faylidan o'qiydi va tekshiradi.
"""

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv

# .env faylini yuklash
if not os.path.exists(".env"):
    print("[XATO] .env fayli topilmadi!")
    print("       Loyiha papkasida .env fayl yarating va quyidagilarni yozing:")
    print()
    print("         API_ID=your_api_id")
    print("         API_HASH=your_api_hash")
    print("         GEMINI_API_KEY=your_gemini_key")
    sys.exit(1)

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    gemini_api_key: str
    model_name: str = "gemini-3.6-flash"
    max_history: int = 20


def _require(name: str) -> str:
    """Muhim o'zgaruvchini o'qiydi, bo'lmasa aniq xato beradi."""
    value = os.getenv(name, "").strip()
    if not value or value.startswith("YOUR_"):
        print(f"[XATO] {name} .env faylida sozlanmagan yoki bo'sh!")
        print(f"       .env faylini oching va {name}=... qatorini to'ldiring.")
        sys.exit(1)
    return value


def load_settings() -> Settings:
    """Barcha sozlamalarni yuklaydi va tekshiradi."""
    api_id_str = _require("API_ID")
    api_hash = _require("API_HASH")
    gemini_key = _require("GEMINI_API_KEY")

    try:
        api_id_int = int(api_id_str)
    except ValueError:
        print("[XATO] API_ID raqam bo'lishi kerak.")
        sys.exit(1)

    return Settings(
        api_id=api_id_int,
        api_hash=api_hash,
        gemini_api_key=gemini_key,
    )


def load_session_string() -> str:
    """Sessiya matnini lokal session.txt faylidan o'qiydi."""
    path = "session.txt"

    if not os.path.exists(path):
        print("[XATO] session.txt fayli topilmadi!")
        print("       Avval quyidagi buyruqni bajaring:")
        print()
        print("         python create_session.py")
        print()
        print("       Bu sizning Telegram sessiyangizni session.txt fayliga saqlaydi.")
        sys.exit(1)

    content = open(path, "r", encoding="utf-8").read().strip()
    if not content:
        print("[XATO] session.txt fayli bo'sh!")
        print("       create_session.py ni qayta ishga tushiring.")
        sys.exit(1)

    return content
