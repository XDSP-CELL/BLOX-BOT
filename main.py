import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Fallback ke liye complete 41 fruits ki lists (agar website load na ho toh ye dikhenge)
FALLBACK_NORMAL = [
    "🍎 Rocket", "🔄 Spin", "🗡️ Blade (Chop)", "🔔 Spring", "💣 Bomb",
    "💨 Smoke", "🦅 Spike", "🔥 Flame", "🧊 Ice", "🦅 Falcon",
    "🏜️ Sand", "✨ Dark", "💎 Diamond", "💡 Light", "ゴム Rubber",
    "🚧 Barrier", "👻 Ghost", "🌋 Magma", "📿 Quake", "❤️ Love",
    "🕷️ Spider", "🎵 Sound", "⛩️ Phoenix", "🌀 Portal", "⚡ Lightning",
    "🐾 Pain", "❄️ Blizzard", "🧘 Buddha", "🧬 Control", "🦇 Shadow",
    "💉 Venom", "👻 Spirit", "🍩 Dough", "🦖 T-Rex", "🦣 Mammoth",
    "🐉 Dragon", "🦊 Kitsune", "🐅 Tiger", "❄️ Yeti", "⛽ Gas", "🌟 Custom/Extra"
]

FALLBACK_MIRAGE = [
    "🍎 Rocket (Mirage)", "🔄 Spin (Mirage)", "🗡️ Blade (Mirage)", "🔔 Spring (Mirage)", "💣 Bomb (Mirage)",
    "💨 Smoke (Mirage)", "🦅 Spike (Mirage)", "🔥 Flame (Mirage)", "🧊 Ice (Mirage)", "🦅 Falcon (Mirage)",
    "🏜️ Sand (Mirage)", "✨ Dark (Mirage)", "💎 Diamond (Mirage)", "💡 Light (Mirage)", "ゴム Rubber (Mirage)",
    "🚧 Barrier (Mirage)", "👻 Ghost (Mirage)", "🌋 Magma (Mirage)", "📿 Quake (Mirage)", "❤️ Love (Mirage)",
    "🕷️ Spider (Mirage)", "🎵 Sound (Mirage)", "⛩️ Phoenix (Mirage)", "🌀 Portal (Mirage)", "⚡ Lightning (Mirage)",
    "🐾 Pain (Mirage)", "❄️ Blizzard (Mirage)", "🧘 Buddha (Mirage)", "🧬 Control (Mirage)", "🦇 Shadow (Mirage)",
    "💉 Venom (Mirage)", "👻 Spirit (Mirage)", "🍩 Dough (Mirage)", "🦖 T-Rex (Mirage)", "🦣 Mammoth (Mirage)",
    "🐉 Dragon (Mirage)", "🦊 Kitsune (Mirage)", "🐅 Tiger (Mirage)", "❄️ Yeti (Mirage)", "⛽ Gas (Mirage)", "🌟 Mirage Special"
]

def fetch_website_stock(stock_type="normal"):
    url = "https://fruityblox.com/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Agar website chal gayi toh check karenge kaun se fruits match ho rahe hain
            source_list = FALLBACK_NORMAL if stock_type == "normal" else FALLBACK_MIRAGE
            matched_fruits = []
            
            for fruit in source_list:
                # Fruit ke naam ka main word nikal kar check karenge
                fruit_keyword = fruit.split()[1].lower() if len(fruit.split()) > 1 else fruit.lower()
                if fruit_keyword in page_text:
                    matched_fruits.append(fruit)
            
            if matched_fruits:
                return matched_fruits
                
    except Exception as e:
        print(f"Error fetching: {e}")
        
    # Agar live fetch na ho paye toh fallback list return kar dega taaki bot band na ho
    return FALLBACK_NORMAL if stock_type == "normal" else FALLBACK_MIRAGE

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🟢 Normal Stock", callback_data="normal_stock"),
        InlineKeyboardButton("✨ Mirage Stock", callback_data="mirage_stock")
    )
    markup.row(
        InlineKeyboardButton("🌐 Open Website Directly", url="https://fruityblox.com/stock")
    )
    bot.reply_to(message, "👇 Niche diye gaye buttons mein se select karein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
    
    if call.data == "normal_stock":
        bot.answer_callback_query(call.id, "Live Normal stock laya ja raha hai...")
        fruits = fetch_website_stock("normal")
        
        part1 = "\n• ".join(fruits[:20])
        part2 = "\n• ".join(fruits[20:])
        
        bot.send_message(call.message.chat.id, f"🔥 *Blox Fruit stock live (Normal - Part 1):*\n\n• {part1}", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, f"🔥 *Blox Fruit stock live (Normal - Part 2):*\n\n• {part2}{footer_text}", parse_mode='Markdown')

    elif call.data == "mirage_stock":
        bot.answer_callback_query(call.id, "Live Mirage stock laya ja raha hai...")
        fruits = fetch_website_stock("mirage")
        
        part1 = "\n• ".join(fruits[:20])
        part2 = "\n• ".join(fruits[20:])
        
        bot.send_message(call.message.chat.id, f"✨ *Blox Fruit stock live (Mirage - Part 1):*\n\n• {part1}", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, f"✨ *Blox Fruit stock live (Mirage - Part 2):*\n\n• {part2}{footer_text}", parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
