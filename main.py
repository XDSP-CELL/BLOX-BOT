import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

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

def get_specific_stock(stock_type):
    url = "https://www.gamersberg.com/blox-fruits/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Website se connect nahi ho paya."

        soup = BeautifulSoup(response.content, 'html.parser')
        matched_fruits = []
        
        # Pura page ka text ya elements check karenge
        for element in soup.find_all(['div', 'span', 'p', 'h3', 'a', 'strong', 'li', 'td']):
            text = element.get_text(strip=True).lower()
            
            # Agar text ke andar fruit ka naam hai, toh use le lenge
            for fruit_key, fruit_display in FRUIT_EMOJIS.items():
                if fruit_key in text:
                    if fruit_display not in matched_fruits:
                        matched_fruits.append(fruit_display)

        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"

        if matched_fruits:
            fruit_list = "\n• ".join(matched_fruits)
            return f"🔥 *Gamersberg {stock_type} Stock:*\n\n• {fruit_list}{footer_text}"
        else:
            return f"⚠️ Stock fetch nahi ho paya. (Website ka layout dynamic ho sakta hai).{footer_text}"

    except Exception as e:
        return f"❌ Error: {e}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 Normal Stock", callback_data="Normal"),
        InlineKeyboardButton("✨ Mirage Stock", callback_data="Mirage")
    )
    bot.reply_to(message, "👇 Kiska stock dekhna chahte hain, select karein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    stock_type = call.data  
    bot.answer_callback_query(call.id, f"{stock_type} stock check kiya ja raha hai...")
    stock_text = get_specific_stock(stock_type)
    bot.send_message(call.message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
