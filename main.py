import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Fruits ke naam aur unki emojis ki dictionary
FRUIT_EMOJIS = {
    'kitsune': '🦊 Kitsune',
    'dragon': '🐉 Dragon',
    't-rex': '🦖 T-Rex',
    'mammoth': '🦣 Mammoth',
    'dough': '🍩 Dough',
    'spirit': '👻 Spirit',
    'control': '🎮 Control',
    'venom': '🐍 Venom',
    'shadow': '👥 Shadow',
    'blizzard': '❄️ Blizzard',
    'portal': '🌀 Portal',
    'buddha': '🧘 Buddha',
    'phoenix': '🔥 Phoenix',
    'sound': '🎵 Sound',
    'pain': '💔 Pain',
    'rumble': '⚡ Rumble',
    'magma': '🌋 Magma',
    'ice': '🧊 Ice',
    'light': '💡 Light',
    'quake': '🌊 Quake',
    'love': '❤️ Love',
    'spider': '🕷️ Spider'
}

def get_stock_data(stock_type="Normal"):
    url = "https://www.gamersberg.com/blox-fruits/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Website se connect nahi ho paya."

        soup = BeautifulSoup(response.content, 'html.parser')
        found_fruits = set()

        for element in soup.find_all(['div', 'span', 'p', 'h3', 'a', 'strong', 'li']):
            text = element.get_text(strip=True).lower()
            for fruit_key, fruit_display in FRUIT_EMOJIS.items():
                if fruit_key in text:
                    found_fruits.add(fruit_display)

        if found_fruits:
            fruit_list = "\n• ".join(list(found_fruits))
            return f"🔥 *Gamersberg {stock_type} Stock:*\n\n• {fruit_list}"
        else:
            return f"⚠️ Filhal {stock_type} stock data load nahi ho paya ya website par update ho raha hai."

    except Exception as e:
        return f"❌ Error: {e}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye niche diye gaye button par click karein ya /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    # Buttons banana Normal aur Mirage stock ke liye
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 Normal Stock", callback_data="normal_stock"),
        InlineKeyboardButton("✨ Mirage Stock", callback_data="mirage_stock")
    )
    bot.reply_to(message, "👇 Kiska stock dekhna chahte hain, select karein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "normal_stock":
        bot.answer_callback_query(call.id, "Normal stock nikala ja raha hai...")
        stock_text = get_stock_data("Normal")
        bot.send_message(call.message.chat.id, stock_text, parse_mode='Markdown')
    elif call.data == "mirage_stock":
        bot.answer_callback_query(call.id, "Mirage stock nikala ja raha hai...")
        stock_text = get_stock_data("Mirage")
        bot.send_message(call.message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
