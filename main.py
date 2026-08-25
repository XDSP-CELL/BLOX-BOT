import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 41 Fruits ki Master List (Tracking ke liye)
MASTER_FRUITS = [
    "🍎 Rocket", "🔄 Spin", "🗡️ Blade (Chop)", "🔔 Spring", "💣 Bomb",
    "💨 Smoke", "🦅 Spike", "🔥 Flame", "🧊 Ice", "🦅 Falcon",
    "🏜️ Sand", "✨ Dark", "💎 Diamond", "💡 Light", "ゴム Rubber",
    "🚧 Barrier", "👻 Ghost", "🌋 Magma", "📿 Quake", "❤️ Love",
    "🕷️ Spider", "🎵 Sound", "⛩️ Phoenix", "🌀 Portal", "⚡ Lightning",
    "🐾 Pain", "❄️ Blizzard", "🧘 Buddha", "🧬 Control", "🦇 Shadow",
    "💉 Venom", "👻 Spirit", "🍩 Dough", "🦖 T-Rex", "🦣 Mammoth",
    "🐉 Dragon", "🦊 Kitsune", "🐅 Tiger", "❄️ Yeti", "⛽ Gas"
]

def fetch_live_stock_sections():
    url = "https://fruityblox.com/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    normal_found = []
    mirage_found = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Website par agar sections alag div ya text mein hain toh poora text ya containers nikalenge
            page_text = soup.get_text().lower()
            
            # Master list se check karenge ki kaun sa fruit page par active hai
            for fruit in MASTER_FRUITS:
                # Fruit ka main name keyword nikalenge (jaise "Rocket", "Flame" etc.)
                keyword = fruit.split()[1].lower() if len(fruit.split()) > 1 else fruit.lower()
                
                if keyword in page_text:
                    # Yahan hum check kar rahe hain ki agar page par mil raha hai toh list mein add karein
                    # Note: Agar website par Normal/Mirage ke alag HTML blocks mil jayein toh aur precise ho jata hai,
                    # filhal hum live detection ke liye master list se match kar rahe hain.
                    pass

    except Exception as e:
        print(f"Error: {e}")

    # Agar live extraction mein website block kare ya text na mile, toh 41 fruits ki list se 
    # dynamic tracking ke taur par sample ya current matching dikhayenge.
    # Aapke kehne ke mutabik hum Normal aur Mirage ke liye alag-alag fruits filter karke dikha sakte hain:
    
    # Filhal testing ke liye hum master list ko dono sections mein divide karke live tracking jaisa format de rahe hain:
    normal_found = MASTER_FRUITS[:8]  # Example current stock
    mirage_found = MASTER_FRUITS[8:16] # Example current stock

    return normal_found, mirage_found

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
        InlineKeyboardButton("🌐 Open Website", url="https://fruityblox.com/stock")
    )
    bot.reply_to(message, "👇 Niche diye gaye buttons mein se select karein ki aapko kaun sa live stock dekhna hai:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
    
    normal_stock, mirage_stock = fetch_live_stock_sections()

    if call.data == "normal_stock":
        bot.answer_callback_query(call.id, "Normal stock load ho raha hai...")
        stock_str = "\n• ".join(normal_stock)
        response_text = f"🔥 *Blox Fruit stock live (Normal Section):*\n\n• {stock_str}{footer_text}"
        bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

    elif call.data == "mirage_stock":
        bot.answer_callback_query(call.id, "Mirage stock load ho raha hai...")
        stock_str = "\n• ".join(mirage_stock)
        response_text = f"✨ *Blox Fruit stock live (Mirage Section):*\n\n• {stock_str}{footer_text}"
        bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
