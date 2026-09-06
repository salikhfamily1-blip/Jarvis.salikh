import os
import threading
import time
from flask import Flask, request, jsonify, render_template
import requests
import telebot

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "Sen 'Jarvis' ismli shaxsiy AI-yordamchisan. "
    "Foydalanuvchiga o'zbek tilida, do'stona, aniq va foydali javob ber. "
    "Javoblaring qisqa va tushunarli bo'lsin, lekin kerak bo'lsa batafsil tushuntir."
)

app = Flask(__name__)

# Oddiy xotira: har bir suhbat uchun oxirgi xabarlarni saqlaymiz (RAM ichida)
chat_histories = {}  # key: user_id (str), value: list of {"role":..,"content":..}
MAX_HISTORY = 12  # oxirgi nechta xabarni eslab qolish


def get_ai_reply(user_id: str, user_message: str) -> str:
    """Groq API orqali Jarvisdan javob olish."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY sozlanmagan. Server administratoriga murojaat qiling."

    history = chat_histories.get(user_id, [])
    history.append({"role": "user", "content": user_message})
    history = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Xatolik yuz berdi: {e}"

    history.append({"role": "assistant", "content": reply})
    chat_histories[user_id] = history[-MAX_HISTORY:]
    return reply


# ---------------------- VEB-CHAT ----------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    user_id = str(data.get("session_id", "web_user"))
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Iltimos, biror xabar yozing."})
    reply = get_ai_reply(f"web_{user_id}", message)
    return jsonify({"reply": reply})


@app.route("/health")
def health():
    return "OK", 200


# ---------------------- TELEGRAM BOT ----------------------

def run_telegram_bot():
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN topilmadi, Telegram bot ishga tushmaydi.")
        return

    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

    @bot.message_handler(commands=["start"])
    def start_handler(message):
        bot.reply_to(
            message,
            "Salom! Men sizning shaxsiy yordamchingiz Jarvisman. "
            "Menga istalgan savolingizni yozing.\n\n"
            "/reset - suhbat tarixini tozalash",
        )

    @bot.message_handler(commands=["reset"])
    def reset_handler(message):
        chat_histories.pop(f"tg_{message.chat.id}", None)
        bot.reply_to(message, "Suhbat tarixi tozalandi. Yangidan boshlaymiz!")

    @bot.message_handler(func=lambda m: True, content_types=["text"])
    def text_handler(message):
        bot.send_chat_action(message.chat.id, "typing")
        reply = get_ai_reply(f"tg_{message.chat.id}", message.text)
        bot.reply_to(message, reply)

    print("Telegram bot ishga tushdi (polling)...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30)
        except Exception as e:
            print(f"Telegram bot xatosi: {e}. 5 soniyadan keyin qayta urinamiz...")
            time.sleep(5)


# Telegram botni alohida oqimda (thread) ishga tushiramiz, agar token berilgan bo'lsa
if TELEGRAM_BOT_TOKEN:
    threading.Thread(target=run_telegram_bot, daemon=True).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
