import os
import time
from flask import Flask
from threading import Thread
import telebot
import google.generativeai as genai

# Server Setup
app = Flask('')

@app.route('/')
def home():
    return "Abhi AI Bot is Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
BOT_TOKEN = "8974797579:AAEC_gGu-gn_isb6YtaMel41o2-v7c0i8pI"
GEMINI_KEY = "AIzaSyA5V-kWwYOBUt2QtqVnQA8waGjIm5I5xfY"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Ekdum sahi model string format
model = genai.GenerativeModel('gemini-2.5-flash')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 *Welcome Bhai!*\n\nMain zinda hoon! Apna sawaal pucho.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(user_text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Google ne koi jawab nahi diya bhai.")
    except Exception as e:
        # Agar koi dikkat aayegi toh seedha chat me batayega
        bot.reply_to(message, f"Galti mili bhai: {str(e)}")

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    
    print("🟢 Bot starting...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
        
