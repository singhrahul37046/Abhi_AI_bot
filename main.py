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
    # Render automatically $PORT environment variable deta hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
BOT_TOKEN = "8974797579:AAEC_gGu-gn_isb6YtaMel41o2-v7c0i8pI"
GEMINI_KEY = "AIzaSyDZ1RQ67W09gQxrXXs0bd2wlVsXX3JDbj4"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Sorry bhai, ek baar fir se koshish karo!")

# Dono cheezein saath mein chalane ke liye thread ka use
if __name__ == "__main__":
    # Web server chalu karo taaki Render ko signal milta rahe
    t = Thread(target=run_web_server)
    t.start()
    
    print("🟢 Bot starting...")
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            time.sleep(5)
