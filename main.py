import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Sabhi fruits ki complete mapping list (Yeti, Gas, aur Lightning/Rumble ke sath)
FRUIT_EMOJIS = {
    'blade': '🗡️ Blade (Chop)',
    'smoke': '💨 Smoke',
    'flame': '🔥 Flame',
    'ghost': '👻 Ghost',
    'ice': '🧊 Ice',
    'sand': '🏜️ Sand',
    'dark': '✨ Dark',
    'diamond': '💎 Diamond',
    'light': '💡 Light',
    'rubber': 'ゴム Rubber',
    'barrier': '🚧 Barrier',
    'magma': '🌋 Magma',
    'quake': '📿 Quake',
    'love': '❤️ Love',
    'spider': '🕷️ Spider',
    'sound': '🎵 Sound',
    'phoenix': '⛩️ Phoenix',
    'portal': '🌀 Portal',
    'lightning': '⚡ Lightning',
    'rumble': '⚡ Lightning (Rumble)',
    'pain': '🐾 Pain',
    'blizzard': '❄️ Blizzard',
    'buddha': '🧘 Buddha',
    'control': '🧬 Control',
    'shadow': '🦇 Shadow',
    'venom': '💉 Venom',
    'spirit': '👻 Spirit',
    'dough': '🍩 Dough',
    't-rex': '🦖 T-Rex',
    'mammoth': '🦣 Mammoth',
    'dragon': '🐉 Dragon',
    'kitsune': '🦊 Kitsune',
    'leopard': '🐆 Leopard',
    'yeti': '❄️ Yeti',
    'gas': '⛽ Gas'
}

def get_fandom_stock():
    url = "https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"❌ Fandom se connect nahi ho paya. (Status: {response.status_code})"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        stock_items = []
        for el in soup.find_all(['div', 'span', 'figcaption', 'td', 'a']):
            text = el.get_text(strip=True).lower()
            for key, emoji_name in FRUIT_EMOJIS.items():
                if key == text or text.startswith(key + " "):
                    if emoji_name not in stock_items:
                        stock_items.append(emoji_name)

        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"

        if stock_items:
            fruit_list = "\n• ".join(stock_items[:6])
            return f"🔥 *Blox Fruits Live Stock (Fandom):*\n\n• {fruit_list}{footer_text}"
        else:
            return f"⚠️ Stock fetch nahi ho paya.{footer_text}"

    except Exception as e:
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        return f"❌ Error: {e}{footer_text}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ Fandom se live stock laya ja raha hai...")
    stock_text = get_fandom_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
