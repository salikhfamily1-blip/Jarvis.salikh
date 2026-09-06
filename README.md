# 🤖 Jarvis — Shaxsiy AI Yordamchi

Bu loyiha sizga ikkita formatda ishlaydigan shaxsiy yordamchi beradi:
- 💬 **Veb-chat** — brauzerda ochiladigan chat sahifasi
- 📱 **Telegram bot** — telefoningizdagi Telegram ilovasida ishlaydi

Ikkalasi ham bepul **Groq** AI xizmatidan foydalanadi (juda tez va bepul limiti katta).

---

## 1-QADAM: Groq API kalitini olish (AI "miya")

1. https://console.groq.com manziliga kiring va ro'yxatdan o'ting (Google akkaunt bilan ham bo'ladi, karta talab qilinmaydi).
2. Chap menyudan **API Keys** bo'limiga o'ting.
3. **Create API Key** tugmasini bosing, nomini xohlagancha qo'ying (masalan "jarvis").
4. Chiqqan kalitni (masalan `gsk_...` bilan boshlanadi) nusxalab, xavfsiz joyga saqlab qo'ying — bu `GROQ_API_KEY`.

## 2-QADAM: Telegram bot yaratish

1. Telegramda **@BotFather** botini toping va oching.
2. `/newbot` buyrug'ini yuboring.
3. Botga nom bering (masalan: "Mening Jarvisim").
4. Foydalanuvchi nomini bering — u albatta `bot` bilan tugashi kerak (masalan: `mening_jarvisim_bot`).
5. BotFather sizga token beradi (masalan: `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxx`). Buni saqlab qo'ying — bu `TELEGRAM_BOT_TOKEN`.

## 3-QADAM: Kodni GitHub'ga yuklash

1. https://github.com da bepul akkaunt oching (agar yo'q bo'lsa).
2. Yangi **repository** yarating (masalan nomi: `jarvis-bot`), "Public" yoki "Private" — farqi yo'q.
3. Ushbu papkadagi barcha fayllarni (`app.py`, `requirements.txt`, `Procfile`, `templates/index.html`, `.env.example`) o'sha repository'ga yuklang.
   - Eng oson yo'li: GitHub sahifasida **"Add file" → "Upload files"** tugmasi orqali fayllarni sudrab tashlash.
   - `.env` faylini hech qachon GitHub'ga yuklamang — u yerda haqiqiy kalitlar bo'lmasligi kerak, faqat `.env.example` yetarli.

## 4-QADAM: Render.com'da bepul deploy qilish

1. https://render.com saytiga kiring, GitHub akkauntingiz bilan ro'yxatdan o'ting.
2. Dashboard'da **"New +" → "Web Service"** tugmasini bosing.
3. GitHub repository'ingizni tanlang (`jarvis-bot`).
4. Quyidagi sozlamalarni kiriting:
   - **Name**: `jarvis-bot` (yoki xohlagan nom)
   - **Region**: eng yaqin joyni tanlang
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 1 --threads 8 --timeout 120`
   - **Instance Type**: **Free**
5. Pastroqda **"Environment Variables"** bo'limini toping va quyidagilarni qo'shing:
   | Key | Value |
   |---|---|
   | `GROQ_API_KEY` | (1-qadamda olgan kalitingiz) |
   | `TELEGRAM_BOT_TOKEN` | (2-qadamda olgan tokeningiz) |
   | `GROQ_MODEL` | `llama-3.3-70b-versatile` |
6. **"Create Web Service"** tugmasini bosing va kutib turing (2-5 daqiqa).
7. Deploy tugagach, Render sizga bir link beradi, masalan: `https://jarvis-bot-xxxx.onrender.com` — shu havolani ochsangiz, veb-chat ochiladi!

## 5-QADAM: Sinab ko'rish

- **Veb-chat**: Render bergan havolani brauzerda oching va yozishni boshlang.
- **Telegram**: Telegramda o'z botingizni toping (2-qadamda bergan `@username` orqali) va `/start` buyrug'ini yuboring.

---

## ⚠️ Muhim eslatmalar

- **Bepul Render tarifi** 15 daqiqa foydalanilmasa "uxlab qoladi" — birinchi xabar biroz sekinroq (10-30 soniya) javob berishi mumkin. Bu normal holat, shaxsiy foydalanish uchun muammo emas.
- Agar suhbatni "unutishini" xohlasangiz: Telegramda `/reset`, veb-chatda esa "Tozalash" tugmasini bosing.
- Suhbat tarixi serverning operativ xotirasida (RAM) saqlanadi — server qayta ishga tushsa (masalan uyqudan uyg'onganda), eski suhbatlar tozalanishi mumkin. Bu shaxsiy loyiha uchun yetarli.
- Jarvis xarakterini o'zgartirmoqchi bo'lsangiz, `app.py` faylidagi `SYSTEM_PROMPT` matnini tahrirlang (masalan, "hazilkash bo'lsin", "faqat rasmiy uslubda gapirsin" va h.k.).

## 🔧 Kodni o'zgartirish

Loyiha juda sodda tuzilgan:
- `app.py` — barcha asosiy mantiq (AI bilan bog'lanish, veb-server, Telegram bot)
- `templates/index.html` — veb-chatning ko'rinishi (dizayn)
- `SYSTEM_PROMPT` — Jarvisning "shaxsiyati", uni xohlagancha o'zgartirishingiz mumkin

Savol tug'ilsa yoki xatolik chiqsa, xatolik matnini menga yuboring — birga tuzatamiz!
