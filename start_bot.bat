@echo off
chcp 65001 >nul
title Telegram Userbot

:: ── Loyiha papkasi ──────────────────────────────────────────
cd /d "D:\Projects\Tg slave"

:: ── Virtual muhitni faollashtirish ──────────────────────────
call venv\Scripts\activate.bat

:: ── Cheksiz tsikl: crash bo'lsa qayta ishga tushadi ─────────
:loop
echo [%date% %time%] Bot ishga tushmoqda...
python main.py
echo [%date% %time%] Bot to'xtadi (exit code: %errorlevel%). 10 soniyadan so'ng qayta ishga tushadi...
timeout /t 10 /nobreak >nul
goto loop
