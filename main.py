import os
import time
from flask import Flask
from threading import Thread
import telebot
import google.generativeai as genai

# Render ko zinda rakhne ke liye ek chota sa web server
app = Flask('')

@app.route('/')
def home():
    return "Abhi AI Bot is Alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
BOT_TOKEN = "8974797579:AAFR8WKA8t0BrgbJJspmWijZVxNoostPktA"
GEMINI_KEY = "AIzaSyA5V-kWwYOBUt2QtqVnQA8waGjIm5I5xfY"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Ekdum simple aur sahi format bina kisi 'models/' ke
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "🚀 *Welcome Bhai!*\n\nMain hoon aapka apna *Abhi AI Chatbot*.\nApna sawaal niche type karo 👇"
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(user_text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Sorry bhai, mujhe iska jawab nahi mila.")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Sorry bhai, ek baar fir se koshish karo! (Error: {str(e)[:50]})")

if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    
    print("🟢 Bot starting...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)
