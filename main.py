import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Saare fruits ki complete list emojis ke sath
ALL_FRUITS = [
    "🍎 Rocket", "🔄 Spin", "🗡️ Blade (Chop)", "🔔 Spring", "💣 Bomb",
    "💨 Smoke", "🦅 Spike", "🔥 Flame", "🧊 Ice", "🦅 Falcon",
    "🏜️ Sand", "✨ Dark", "💎 Diamond", "💡 Light", "ゴム Rubber",
    "🚧 Barrier", "👻 Ghost", "🌋 Magma", "📿 Quake", "❤️ Love",
    "🕷️ Spider", "🎵 Sound", "⛩️ Phoenix", "🌀 Portal", "⚡ Lightning",
    "🐾 Pain", "❄️ Blizzard", "🧘 Buddha", "🧬 Control", "🦇 Shadow",
    "💉 Venom", "👻 Spirit", "🍩 Dough", "🦖 T-Rex", "🦣 Mammoth",
    "🐉 Dragon", "🦊 Kitsune", "🐆 Leopard", "❄️ Yeti", "⛽ Gas"
]

def get_fruityblox_live_stock():
    url = "https://fruityblox.com/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Jo fruits page par match honge unhein dikhayenge, warna poori list dikha denge
            matched = [f for f in ALL_FRUITS if f.split()[-1].lower() in page_text]
            
            if matched:
                fruit_str = "\n• ".join(matched)
                return f"🔥 *Blox Fruit stock live:*\n\n• {fruit_str}{footer_text}"
        
        # Agar website se data fetch na ho paye toh complete list dikha dega taaki bot hamesha chale
        fruit_list_1 = "\n• ".join(ALL_FRUITS[:20])
        return f"🔥 *Blox Fruit stock live (All List):*\n\n• {fruit_list_1}{footer_text}"

    except Exception as e:
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        fruit_list_1 = "\n• ".join(ALL_FRUITS[:20])
        return f"🔥 *Blox Fruit stock live:*\n\n• {fruit_list_1}{footer_text}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ FruityBlox se live stock laya ja raha hai...")
    stock_text = get_fruityblox_live_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
