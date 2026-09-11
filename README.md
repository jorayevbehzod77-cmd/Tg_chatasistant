# Telegram Userbot — Gemini AI Auto-Reply

Telethon + Google Gemini asosida ishlovchi Telegram Userbot.
Kiruvchi **shaxsiy** xabarlarga avtomatik ravishda AI javob qaytaradi.

## Tuzilishi

```
telegram-userbot/
├── .env                 # Maxfiy kalitlar (git-ga tushmaydi)
├── .gitignore
├── requirements.txt
├── main.py              # Asosiy bot kodi
└── README.md
```

## Ishga tushirish

```bash
# 1. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 2. Botni ishga tushirish
python main.py
```

Birinchi marta ishga tushirganda Telethon **telefon raqam** va **tasdiqlash kodi** so'raydi — shu orqali sessiya yaratiladi.

## Muhim

| Sozlama | Tavsif |
|---------|--------|
| **Faqat shaxsiy chatlar** | Guruh va kanal xabarlariga javob bermaydi |
| **Bot xabarlari** | Boshqa botlarning xabarlariga javob bermaydi |
| **Suhbat tarixi** | Har bir foydalanuvchi uchun oxirgi 20 ta xabar kontekst sifatida saqlanadi |
| **Model** | `gemini-2.0-flash` (bepul) |
